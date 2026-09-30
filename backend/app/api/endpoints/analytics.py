"""
Analytics API — daily/weekly/monthly stats, weight history, fitness score.
"""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.analytics_service import AnalyticsService
from app.core.responses import success_response

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/daily")
async def get_daily(
    date_str: Optional[str] = Query(None, alias="date"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get daily fitness summary."""
    service = AnalyticsService(db)
    target = date.fromisoformat(date_str) if date_str else None
    data = await service.get_daily(user.id, target)
    return success_response(data=data)


@router.get("/weekly")
async def get_weekly(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get weekly fitness summary with daily breakdown."""
    service = AnalyticsService(db)
    data = await service.get_weekly(user.id)
    return success_response(data=data)


@router.get("/monthly")
async def get_monthly(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get monthly fitness statistics."""
    service = AnalyticsService(db)
    data = await service.get_monthly(user.id)
    return success_response(data=data)


@router.get("/weight")
async def get_weight_history(
    days: int = Query(default=90, ge=7, le=365),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get weight trend over time."""
    service = AnalyticsService(db)
    data = await service.get_weight_history(user.id, days)
    return success_response(data=data)


@router.get("/fitness-score")
async def get_fitness_score(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get composite fitness score (0-100)."""
    service = AnalyticsService(db)
    data = await service.get_fitness_score(user.id)
    return success_response(data=data)
