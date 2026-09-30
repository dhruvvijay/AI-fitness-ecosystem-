"""
Analytics service — daily/weekly/monthly aggregation and fitness scoring.
"""

from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.analytics_repository import AnalyticsRepository
from app.repositories.steps_repository import StepsRepository
from app.repositories.workout_repository import WorkoutRepository


class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.analytics_repo = AnalyticsRepository(db)
        self.steps_repo = StepsRepository(db)
        self.workout_repo = WorkoutRepository(db)

    async def get_daily(self, user_id: int, target_date: date = None) -> dict:
        target_date = target_date or date.today()
        return await self.analytics_repo.get_daily_summary(user_id, target_date)

    async def get_weekly(self, user_id: int) -> dict:
        daily_summaries = await self.analytics_repo.get_weekly_summary(user_id)
        # Compute averages
        total_steps = sum(d["steps"]["total"] for d in daily_summaries)
        total_cal_consumed = sum(d["nutrition"]["calories_consumed"] for d in daily_summaries)
        total_water = sum(d["water_ml"] for d in daily_summaries)
        total_workouts = sum(d["workouts"]["count"] for d in daily_summaries)

        return {
            "days": daily_summaries,
            "averages": {
                "avg_steps": round(total_steps / 7),
                "avg_calories_consumed": round(total_cal_consumed / 7),
                "avg_water_ml": round(total_water / 7),
                "total_workouts": total_workouts,
            },
        }

    async def get_monthly(self, user_id: int) -> dict:
        today = date.today()
        step_stats = await self.steps_repo.get_statistics(user_id, days=30)
        workout_stats = await self.workout_repo.get_workout_stats(user_id, days=30)
        return {
            "steps": step_stats,
            "workouts": workout_stats,
        }

    async def get_weight_history(self, user_id: int, days: int = 90) -> list[dict]:
        return await self.analytics_repo.get_weight_history(user_id, days)

    async def get_fitness_score(self, user_id: int) -> dict:
        """
        Composite fitness score (0-100) based on:
        - Step consistency (25%)
        - Workout frequency (25%)
        - Nutrition adherence (25%)
        - Weight trend (25%)
        """
        step_stats = await self.steps_repo.get_statistics(user_id, days=30)
        workout_stats = await self.workout_repo.get_workout_stats(user_id, days=30)

        # Step score: avg_steps / 10000 * 100, capped at 100
        step_score = min(100, (step_stats.get("avg_steps", 0) / 10000) * 100)

        # Workout score: workouts_per_week / 4 * 100
        workouts_per_week = workout_stats.get("total_workouts", 0) / 4.3
        workout_score = min(100, (workouts_per_week / 4) * 100)

        # Combined (simplified — full version would include nutrition + weight)
        overall = round((step_score + workout_score) / 2)

        return {
            "overall": overall,
            "step_score": round(step_score),
            "workout_score": round(workout_score),
            "grade": "A" if overall >= 80 else "B" if overall >= 60 else "C" if overall >= 40 else "D",
        }
