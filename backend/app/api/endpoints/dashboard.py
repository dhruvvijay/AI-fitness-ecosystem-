"""
Dashboard API — single endpoint returning all dashboard data.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.dashboard_service import DashboardService
from app.core.responses import success_response

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("")
async def get_dashboard(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get complete dashboard data in a single request.
    Returns steps, calories, nutrition, water, workouts, BMI, weight trend.
    """
    service = DashboardService(db)
    data = await service.get_dashboard(user.id)
    return success_response(data=data)
