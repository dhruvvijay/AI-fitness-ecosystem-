"""
Nutrition API — meals, daily summary, food search.
"""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.nutrition_service import NutritionService
from app.repositories.food_repository import FoodRepository
from app.repositories.progress_repository import ProgressRepository
from app.core.responses import success_response, paginated_response

router = APIRouter(prefix="/nutrition", tags=["Nutrition"])


# ── Schemas ──────────────────────────────────────────────────────

class MealItemInput(BaseModel):
    food_id: int
    servings: float = 1.0
    custom_weight_g: Optional[float] = None

class CreateMealRequest(BaseModel):
    meal_type: str = Field(pattern="^(breakfast|lunch|dinner|snack)$")
    name: Optional[str] = None
    date: Optional[str] = None
    items: list[MealItemInput]

class LogWaterRequest(BaseModel):
    amount_ml: int = Field(ge=1, le=5000)


# ── Endpoints ────────────────────────────────────────────────────

@router.get("/today")
async def get_today(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get today's nutrition summary (macros, meal count)."""
    service = NutritionService(db)
    data = await service.get_today_summary(user.id)
    return success_response(data=data)


@router.get("/week")
async def get_week(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get last 7 days nutrition breakdown."""
    service = NutritionService(db)
    data = await service.get_weekly_summary(user.id)
    return success_response(data=data)


@router.get("/meals")
async def get_meals(
    date_str: str = Query(None, alias="date"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get meals for a specific date (defaults to today)."""
    service = NutritionService(db)
    target = date.fromisoformat(date_str) if date_str else date.today()
    data = await service.get_meals_by_date(user.id, target)
    return success_response(data=data)


@router.post("/meals")
async def create_meal(
    body: CreateMealRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a meal with food items."""
    service = NutritionService(db)
    target = date.fromisoformat(body.date) if body.date else None
    items = [i.model_dump() for i in body.items]
    data = await service.create_meal(
        user_id=user.id, meal_type=body.meal_type, name=body.name, items=items, meal_date=target
    )
    return success_response(data=data, message="Meal logged")


@router.delete("/meals/{meal_id}")
async def delete_meal(
    meal_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a meal."""
    service = NutritionService(db)
    await service.delete_meal(user.id, meal_id)
    return success_response(message="Meal deleted")


# ── Food Search ──────────────────────────────────────────────────

@router.get("/foods/search")
async def search_foods(
    q: str = Query(min_length=1),
    category: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Search the food database."""
    repo = FoodRepository(db)
    offset = (page - 1) * limit
    foods, total = await repo.search(q, category, offset, limit)
    items = [
        {
            "id": f.id,
            "name": f.name,
            "category": f.category,
            "calories": f.calories,
            "protein_g": f.protein_g,
            "carbs_g": f.carbs_g,
            "fat_g": f.fat_g,
            "fiber_g": f.fiber_g,
            "serving_size": f.serving_size,
            "serving_weight_g": f.serving_weight_g,
        }
        for f in foods
    ]
    return paginated_response(items, total, page, limit)


# ── Water ────────────────────────────────────────────────────────

@router.post("/water")
async def log_water(
    body: LogWaterRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Log water intake."""
    repo = ProgressRepository(db)
    await repo.log_water(user.id, body.amount_ml)
    total = await repo.get_water_today(user.id)
    return success_response(data={"logged_ml": body.amount_ml, "total_today_ml": total}, message="Water logged")


@router.get("/water/today")
async def get_water_today(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get today's water intake."""
    repo = ProgressRepository(db)
    total = await repo.get_water_today(user.id)
    return success_response(data={"total_ml": total})
