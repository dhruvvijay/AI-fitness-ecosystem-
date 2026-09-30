"""
Admin API — system stats, user management, analytics.
Protected with admin role requirement.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.api.deps import require_admin
from app.models.user import User
from app.models.nutrition import Meal, Food
from app.models.workout import WorkoutSession, Exercise
from app.models.fitness import StepsDaily
from app.core.responses import success_response, paginated_response

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
async def get_system_stats(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get system-wide statistics."""
    total_users = (await db.execute(select(func.count(User.id)))).scalar() or 0
    total_foods = (await db.execute(select(func.count(Food.id)))).scalar() or 0
    total_exercises = (await db.execute(select(func.count(Exercise.id)))).scalar() or 0
    total_workouts = (await db.execute(select(func.count(WorkoutSession.id)))).scalar() or 0
    total_meals = (await db.execute(select(func.count(Meal.id)))).scalar() or 0

    return success_response(data={
        "total_users": total_users,
        "total_foods": total_foods,
        "total_exercises": total_exercises,
        "total_workouts": total_workouts,
        "total_meals": total_meals,
    })


@router.get("/users")
async def list_users(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all users with pagination."""
    offset = (page - 1) * limit
    total = (await db.execute(select(func.count(User.id)))).scalar() or 0
    result = await db.execute(
        select(User).order_by(User.created_at.desc()).offset(offset).limit(limit)
    )
    users = [
        {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at.isoformat() if u.created_at else None,
            "last_login": u.last_login,
        }
        for u in result.scalars().all()
    ]
    return paginated_response(users, total, page, limit)


@router.put("/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Activate/deactivate a user."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("User", user_id)
    user.is_active = not user.is_active
    await db.flush()
    return success_response(
        data={"id": user.id, "is_active": user.is_active},
        message=f"User {'activated' if user.is_active else 'deactivated'}",
    )
