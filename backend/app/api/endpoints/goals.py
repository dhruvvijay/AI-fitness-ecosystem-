"""
Goals & BMI API — BMI calculation, goal tracking, achievements.
"""

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.goal_service import GoalService, AchievementService
from app.core.responses import success_response

router = APIRouter(prefix="/goals", tags=["Goals & BMI"])


class BMIRequest(BaseModel):
    weight_kg: float = Field(ge=20, le=500)
    height_cm: float = Field(ge=50, le=300)


@router.post("/bmi")
async def calculate_bmi(
    body: BMIRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Calculate BMI/BMR/TDEE and save to history."""
    service = GoalService(db)
    data = await service.calculate_bmi(user.id, body.weight_kg, body.height_cm)
    return success_response(data=data)


@router.get("/bmi/history")
async def bmi_history(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get BMI history."""
    service = GoalService(db)
    data = await service.get_bmi_history(user.id)
    return success_response(data=data)


@router.get("/weight-progress")
async def weight_progress(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get weight goal progress."""
    service = GoalService(db)
    data = await service.get_weight_progress(user.id)
    return success_response(data=data)


@router.get("/achievements")
async def get_achievements(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all achievements with user's earned status."""
    service = AchievementService(db)
    all_achievements = await service.get_all_achievements()
    earned = await service.get_user_achievements(user.id)
    earned_ids = {a["id"] for a in earned}

    for ach in all_achievements:
        ach["earned"] = ach["id"] in earned_ids

    return success_response(data={
        "achievements": all_achievements,
        "earned_count": len(earned),
        "total_count": len(all_achievements),
    })
