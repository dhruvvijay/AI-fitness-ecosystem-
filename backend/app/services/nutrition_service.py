"""
Nutrition service — meal logging, daily summary, and nutrition tracking.
"""

from datetime import date, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.meal_repository import MealRepository
from app.repositories.food_repository import FoodRepository
from app.core.exceptions import NotFoundException


class NutritionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.meal_repo = MealRepository(db)
        self.food_repo = FoodRepository(db)

    async def get_today_summary(self, user_id: int) -> dict:
        return await self.meal_repo.get_daily_nutrition_summary(user_id, date.today())

    async def get_daily_summary(self, user_id: int, target_date: date) -> dict:
        return await self.meal_repo.get_daily_nutrition_summary(user_id, target_date)

    async def get_weekly_summary(self, user_id: int) -> list[dict]:
        today = date.today()
        results = []
        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            summary = await self.meal_repo.get_daily_nutrition_summary(user_id, d)
            summary["date"] = d.isoformat()
            summary["day"] = d.strftime("%a")
            results.append(summary)
        return results

    async def get_meals_by_date(self, user_id: int, target_date: date) -> list[dict]:
        meals = await self.meal_repo.get_user_meals_by_date(user_id, target_date)
        return [self._meal_to_dict(m) for m in meals]

    async def create_meal(
        self,
        user_id: int,
        meal_type: str,
        name: Optional[str],
        items: list[dict],
        meal_date: Optional[date] = None,
    ) -> dict:
        """
        Create a meal with items. Each item must have food_id, servings.
        Nutrition is auto-calculated from the food database.
        """
        target_date = meal_date or date.today()
        resolved_items = []

        for item in items:
            food_id = item.get("food_id")
            servings = item.get("servings", 1.0)
            custom_weight = item.get("custom_weight_g")

            food = await self.food_repo.get_by_id(food_id)
            if not food:
                raise NotFoundException("Food", food_id)

            # Calculate nutrition based on servings
            multiplier = servings
            if custom_weight and food.serving_weight_g:
                multiplier = custom_weight / food.serving_weight_g

            resolved_items.append({
                "food_id": food_id,
                "servings": servings,
                "custom_weight_g": custom_weight,
                "calories": round(food.calories * multiplier, 1),
                "protein_g": round(food.protein_g * multiplier, 1),
                "carbs_g": round(food.carbs_g * multiplier, 1),
                "fat_g": round(food.fat_g * multiplier, 1),
            })

        meal = await self.meal_repo.create_meal_with_items(
            user_id=user_id,
            meal_date=target_date,
            meal_type=meal_type,
            name=name,
            items_data=resolved_items,
        )
        return self._meal_to_dict(meal)

    async def delete_meal(self, user_id: int, meal_id: int) -> bool:
        meal = await self.meal_repo.get_by_id(meal_id)
        if not meal or meal.user_id != user_id:
            raise NotFoundException("Meal", meal_id)
        return await self.meal_repo.delete_by_id(meal_id)

    @staticmethod
    def _meal_to_dict(meal) -> dict:
        return {
            "id": meal.id,
            "date": meal.date.isoformat(),
            "meal_type": meal.meal_type,
            "name": meal.name,
            "total_calories": meal.total_calories,
            "total_protein": meal.total_protein,
            "total_carbs": meal.total_carbs,
            "total_fat": meal.total_fat,
            "total_fiber": meal.total_fiber,
            "items": [
                {
                    "id": item.id,
                    "food_id": item.food_id,
                    "servings": item.servings,
                    "calories": item.calories,
                    "protein_g": item.protein_g,
                    "carbs_g": item.carbs_g,
                    "fat_g": item.fat_g,
                }
                for item in (meal.items or [])
            ],
        }
