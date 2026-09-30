"""
Steps API — tracking, statistics, and history.
"""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.steps_service import StepsService
from app.core.responses import success_response

router = APIRouter(prefix="/steps", tags=["Steps"])


class LogStepsRequest(BaseModel):
    steps: int = Field(ge=0, le=200000)
    date: Optional[str] = None  # ISO date, defaults to today
    source: str = "manual"


@router.post("")
async def log_steps(
    body: LogStepsRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Log steps for a day (creates or updates)."""
    service = StepsService(db)
    target_date = date.fromisoformat(body.date) if body.date else None
    result = await service.log_steps(user.id, body.steps, target_date, body.source)
    return success_response(data=result, message="Steps logged")


@router.get("/today")
async def get_today(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get today's step data."""
    service = StepsService(db)
    data = await service.get_today(user.id)
    return success_response(data=data)


@router.get("/week")
async def get_week(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get last 7 days of step data."""
    service = StepsService(db)
    data = await service.get_week(user.id)
    return success_response(data=data)


@router.get("/month")
async def get_month(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get last 30 days of step data."""
    service = StepsService(db)
    data = await service.get_month(user.id)
    return success_response(data=data)


@router.get("/statistics")
async def get_statistics(
    days: int = Query(default=30, ge=7, le=365),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get step statistics for the given period."""
    service = StepsService(db)
    data = await service.get_statistics(user.id, days)
    return success_response(data=data)
