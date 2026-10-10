"""
AI Fitness Ecosystem — FastAPI Application Entry Point.

Production-ready ASGI application with middleware stack, route registration,
WebSocket support, and comprehensive API documentation.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from loguru import logger
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import RequestLoggingMiddleware, register_exception_handlers
from app.core.responses import success_response

# Import all route modules
from app.api.endpoints import (
    auth, dashboard, nutrition, workouts, ai_endpoints, admin,
    steps, goals, analytics, notifications, devices,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    setup_logging()
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"📊 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🗄️  Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

    # Auto-create tables if they don't exist
    try:
        from app.db.base import engine, Base
        import app.models  # noqa: F401 — triggers __init__.py which imports all models
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database tables verified/created")
    except Exception as e:
        logger.error(f"❌ Database table creation failed: {e}")

    yield
    logger.info("👋 Shutting down gracefully...")


def create_app() -> FastAPI:
    """Application factory — creates and configures the FastAPI instance."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "AI-powered fitness ecosystem API providing workout planning, "
            "nutrition tracking, AI food scanning, progress analytics, "
            "and intelligent coaching. All data persisted in MySQL."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ── Middleware Stack ─────────────────────────────────────────

    # CORS — build dynamic origins list
    cors_origins = list(settings.BACKEND_CORS_ORIGINS)
    if settings.FRONTEND_URL and settings.FRONTEND_URL not in cors_origins:
        cors_origins.append(settings.FRONTEND_URL)
    # Also allow common Railway patterns
    import os
    railway_public = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
    if railway_public:
        cors_origins.append(f"https://{railway_public}")
    logger.info(f"🌐 CORS origins: {cors_origins}")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Gzip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Request logging
    app.add_middleware(RequestLoggingMiddleware)

    # Rate limiting
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Custom exception handlers
    register_exception_handlers(app)

    # ── Route Registration ───────────────────────────────────────

    api_prefix = settings.API_V1_PREFIX

    # Core APIs
    app.include_router(auth.router, prefix=api_prefix)
    app.include_router(dashboard.router, prefix=api_prefix)
    app.include_router(steps.router, prefix=api_prefix)
    app.include_router(nutrition.router, prefix=api_prefix)
    app.include_router(workouts.router, prefix=api_prefix)
    app.include_router(goals.router, prefix=api_prefix)
    app.include_router(analytics.router, prefix=api_prefix)
    app.include_router(notifications.router, prefix=api_prefix)
    app.include_router(devices.router, prefix=api_prefix)
    app.include_router(ai_endpoints.router, prefix=api_prefix)

    # Admin (no prefix — already has /admin)
    app.include_router(admin.router, prefix=api_prefix)

    # ── Health Check ─────────────────────────────────────────────

    @app.get("/health", tags=["System"])
    async def health_check():
        """Check API and service status."""
        health = {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "services": {
                "api": "up",
                "database": "configured",
                "redis": "configured" if settings.REDIS_URL else "not configured",
                "ai": "configured" if (settings.OPENAI_API_KEY or settings.GEMINI_API_KEY) else "mock mode",
            },
        }
        # Test database connection
        try:
            from app.db.base import engine
            from sqlalchemy import text
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            health["services"]["database"] = "up"
        except Exception:
            health["services"]["database"] = "down"
            health["status"] = "degraded"

        return health

    @app.get("/", tags=["System"])
    async def root():
        return success_response(
            data={
                "name": settings.APP_NAME,
                "version": settings.APP_VERSION,
                "docs": "/docs",
                "health": "/health",
            },
            message=f"Welcome to {settings.APP_NAME} API",
        )

    return app


app = create_app()
