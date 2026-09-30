"""
Meal repository — meal and meal item CRUD, daily nutrition aggregation.
"""

from datetime import date
from typing import Optional, Sequence
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.repositories.base import BaseRepository
from app.models.nutrition import Meal, MealItem


class MealRepository(BaseRepository[Meal]):
    def __init__(self, db: AsyncSession):
        super().__init__(Meal, db)

    async def get_user_meals_by_date(self, user_id: int, meal_date: date) -> Sequence[Meal]:
        result = await self.db.execute(
            select(Meal)
            .options(selectinload(Meal.items))
            .where(Meal.user_id == user_id, Meal.date == meal_date)
            .order_by(Meal.created_at)
        )
        return result.scalars().all()

    async def get_user_meals_range(
        self, user_id: int, start_date: date, end_date: date
    ) -> Sequence[Meal]:
        result = await self.db.execute(
            select(Meal)
            .options(selectinload(Meal.items))
            .where(
                Meal.user_id == user_id,
                Meal.date >= start_date,
                Meal.date <= end_date,
            )
            .order_by(Meal.date, Meal.created_at)
        )
        return result.scalars().all()

    async def get_daily_nutrition_summary(self, user_id: int, target_date: date) -> dict:
        """Aggregate nutrition totals for a specific date."""
        result = await self.db.execute(
            select(
                func.coalesce(func.sum(Meal.total_calories), 0).label("calories"),
                func.coalesce(func.sum(Meal.total_protein), 0).label("protein"),
                func.coalesce(func.sum(Meal.total_carbs), 0).label("carbs"),
                func.coalesce(func.sum(Meal.total_fat), 0).label("fat"),
                func.coalesce(func.sum(Meal.total_fiber), 0).label("fiber"),
                func.count(Meal.id).label("meal_count"),
            ).where(Meal.user_id == user_id, Meal.date == target_date)
        )
        row = result.one()
        return {
            "calories": float(row.calories),
            "protein": float(row.protein),
            "carbs": float(row.carbs),
            "fat": float(row.fat),
            "fiber": float(row.fiber),
            "meal_count": int(row.meal_count),
        }

    async def create_meal_with_items(
        self,
        user_id: int,
        meal_date: date,
        meal_type: str,
        name: Optional[str],
        items_data: list[dict],
    ) -> Meal:
        """Create a meal and its items, auto-calculate totals."""
        total_cal = sum(i.get("calories", 0) for i in items_data)
        total_pro = sum(i.get("protein_g", 0) for i in items_data)
        total_carb = sum(i.get("carbs_g", 0) for i in items_data)
        total_fat = sum(i.get("fat_g", 0) for i in items_data)
        total_fiber = sum(i.get("fiber_g", 0) for i in items_data)

        meal = Meal(
            user_id=user_id,
            date=meal_date,
            meal_type=meal_type,
            name=name,
            total_calories=total_cal,
            total_protein=total_pro,
            total_carbs=total_carb,
            total_fat=total_fat,
            total_fiber=total_fiber,
        )
        self.db.add(meal)
        await self.db.flush()

        for item_data in items_data:
            item = MealItem(meal_id=meal.id, **item_data)
            self.db.add(item)

        await self.db.flush()
        await self.db.refresh(meal)
        return meal
