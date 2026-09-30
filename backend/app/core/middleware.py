"""
FastAPI middleware: request logging, timing, correlation IDs, exception handling.
"""

import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from loguru import logger
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log every request with timing and correlation ID."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id
        start = time.perf_counter()

        # Skip logging for health checks and static files
        path = request.url.path
        skip_log = path in ("/health", "/favicon.ico", "/openapi.json")

        if not skip_log:
            logger.info(
                f"[{request_id}] → {request.method} {path}"
            )

        try:
            response = await call_next(request)
        except Exception as exc:
            elapsed = (time.perf_counter() - start) * 1000
            logger.error(f"[{request_id}] ✗ {request.method} {path} | {elapsed:.0f}ms | {exc}")
            raise

        elapsed = (time.perf_counter() - start) * 1000
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{elapsed:.0f}ms"

        if not skip_log:
            log_fn = logger.info if response.status_code < 400 else logger.warning
            log_fn(
                f"[{request_id}] ← {response.status_code} {request.method} {path} | {elapsed:.0f}ms"
            )

        return response


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers for AppException and fallback."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    **({"details": exc.details} if exc.details else {}),
                },
            },
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": {"code": "VALIDATION_ERROR", "message": str(exc)},
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f"Unhandled exception: {type(exc).__name__}: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {"code": "INTERNAL_ERROR", "message": "An internal server error occurred"},
            },
        )
