"""
Database engine, session factory, and declarative base for SQLAlchemy async operations.
"""

from datetime import datetime, timezone
from typing import AsyncGenerator

from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# ── Async Engine ─────────────────────────────────────────────────

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)

# ── Session Factory ──────────────────────────────────────────────

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# ── Base Model ───────────────────────────────────────────────────

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models with common audit fields."""
    pass


class TimestampMixin:
    """Mixin that adds created_at and updated_at columns to models."""
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# ── Session Dependency ───────────────────────────────────────────

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async DB session, ensuring it's closed after use."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
