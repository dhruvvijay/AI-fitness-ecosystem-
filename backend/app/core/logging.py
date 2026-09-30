"""
Structured logging configuration using loguru.
Replaces default Python logging with structured, colored output.
"""

import sys
import logging
from loguru import logger

from app.core.config import settings


class InterceptHandler(logging.Handler):
    """Redirect standard logging to loguru."""
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging() -> None:
    """Configure loguru as the primary logging backend."""
    # Remove default handler
    logger.remove()

    # Console handler
    log_level = "DEBUG" if settings.DEBUG else "INFO"
    logger.add(
        sys.stdout,
        level=log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    # File handler for production
    if settings.ENVIRONMENT != "development":
        logger.add(
            "logs/app.log",
            rotation="10 MB",
            retention="30 days",
            compression="gz",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        )

    # Redirect standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    for name in ["uvicorn", "uvicorn.access", "uvicorn.error", "sqlalchemy.engine"]:
        logging.getLogger(name).handlers = [InterceptHandler()]

    logger.info(f"Logging configured: level={log_level}, env={settings.ENVIRONMENT}")
