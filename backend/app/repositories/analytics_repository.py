"""
Progress & analytics repository — aggregated fitness data queries.
"""

from datetime import date, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fitness import StepsDaily, CalorieLog, WaterLog, BMIRecord
from app.models.nutrition import Meal
from app.models.workout import WorkoutSession


class AnalyticsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_daily_summary(self, user_id: int, target_date: date) -> dict:
        """Aggregate all fitness data for a single day."""
        # Steps
        steps_result = await self.db.execute(
            select(StepsDaily.total_steps, StepsDaily.calories_burned, StepsDaily.distance_km)
            .where(StepsDaily.user_id == user_id, StepsDaily.date == target_date)
        )
        steps_row = steps_result.first()

        # Calories consumed (from meals)
        meal_result = await self.db.execute(
            select(
                func.coalesce(func.sum(Meal.total_calories), 0),
                func.coalesce(func.sum(Meal.total_protein), 0),
                func.coalesce(func.sum(Meal.total_carbs), 0),
                func.coalesce(func.sum(Meal.total_fat), 0),
            ).where(Meal.user_id == user_id, Meal.date == target_date)
        )
        meal_row = meal_result.one()

        # Water
        water_result = await self.db.execute(
            select(func.coalesce(func.sum(WaterLog.amount_ml), 0))
            .where(WaterLog.user_id == user_id, WaterLog.date == target_date)
        )
        water_ml = water_result.scalar() or 0

        # Workouts
        workout_result = await self.db.execute(
            select(
                func.count(WorkoutSession.id),
                func.coalesce(func.sum(WorkoutSession.duration_minutes), 0),
                func.coalesce(func.sum(WorkoutSession.total_calories_burned), 0),
            ).where(
                WorkoutSession.user_id == user_id,
                WorkoutSession.date == target_date,
            )
        )
        workout_row = workout_result.one()

        return {
            "date": target_date.isoformat(),
            "steps": {
                "total": steps_row[0] if steps_row else 0,
                "calories_burned": float(steps_row[1]) if steps_row else 0,
                "distance_km": float(steps_row[2]) if steps_row else 0,
            },
            "nutrition": {
                "calories_consumed": float(meal_row[0]),
                "protein_g": float(meal_row[1]),
                "carbs_g": float(meal_row[2]),
                "fat_g": float(meal_row[3]),
            },
            "water_ml": int(water_ml),
            "workouts": {
                "count": int(workout_row[0]),
                "duration_minutes": int(workout_row[1]),
                "calories_burned": float(workout_row[2]),
            },
        }

    async def get_weekly_summary(self, user_id: int) -> list[dict]:
        """Get daily summaries for the last 7 days."""
        today = date.today()
        results = []
        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            summary = await self.get_daily_summary(user_id, d)
            results.append(summary)
        return results

    async def get_weight_history(self, user_id: int, days: int = 90) -> list[dict]:
        start = date.today() - timedelta(days=days)
        result = await self.db.execute(
            select(BMIRecord.date, BMIRecord.weight_kg, BMIRecord.bmi)
            .where(BMIRecord.user_id == user_id, BMIRecord.date >= start)
            .order_by(BMIRecord.date)
        )
        return [
            {"date": row[0].isoformat(), "weight_kg": float(row[1]), "bmi": float(row[2])}
            for row in result.all()
        ]
