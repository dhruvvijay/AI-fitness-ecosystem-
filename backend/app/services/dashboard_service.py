"""
Dashboard service — aggregates all fitness data into a single efficient response.
"""

from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.analytics_repository import AnalyticsRepository
from app.repositories.steps_repository import StepsRepository
from app.repositories.progress_repository import ProgressRepository
from app.repositories.workout_repository import WorkoutRepository
from app.repositories.user_repository import UserRepository
from app.utils.calculations import calculate_bmi, bmi_category, calculate_bmr, calculate_tdee, calculate_age


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.analytics_repo = AnalyticsRepository(db)
        self.steps_repo = StepsRepository(db)
        self.progress_repo = ProgressRepository(db)
        self.workout_repo = WorkoutRepository(db)
        self.user_repo = UserRepository(db)

    async def get_dashboard(self, user_id: int) -> dict:
        """
        Single API call that returns everything the dashboard needs.
        Avoids N+1 frontend requests.
        """
        today = date.today()

        # Get user profile for targets
        user = await self.user_repo.get_with_profile(user_id)
        profile = user.profile if user else None

        # Daily summary (steps, nutrition, water, workouts)
        daily = await self.analytics_repo.get_daily_summary(user_id, today)

        # Step streak
        streak = await self.steps_repo.get_streak(user_id)

        # Water today
        water_today = await self.progress_repo.get_water_today(user_id)

        # Weekly steps for chart
        weekly_steps = []
        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            record = await self.steps_repo.get_by_user_date(user_id, d)
            weekly_steps.append({
                "date": d.isoformat(),
                "day": d.strftime("%a"),
                "steps": record.total_steps if record else 0,
            })

        # Workout stats (last 30 days)
        workout_stats = await self.workout_repo.get_workout_stats(user_id, days=30)

        # Weight trend (last 90 days)
        weight_trend = await self.analytics_repo.get_weight_history(user_id, days=90)

        # BMI if profile exists
        bmi_data = None
        if profile and profile.weight_kg and profile.height_cm:
            bmi_val = calculate_bmi(profile.weight_kg, profile.height_cm)
            bmi_data = {
                "value": bmi_val,
                "category": bmi_category(bmi_val),
                "weight_kg": profile.weight_kg,
                "height_cm": profile.height_cm,
            }

        # Targets
        targets = {
            "calories": profile.daily_calorie_target if profile else 2200,
            "protein_g": profile.daily_protein_target if profile else 150,
            "water_ml": profile.daily_water_target_ml if profile else 2500,
            "steps": profile.daily_step_target if profile else 10000,
        }

        return {
            "today": daily,
            "targets": targets,
            "steps": {
                "today": daily["steps"]["total"],
                "goal": targets["steps"],
                "streak": streak,
                "weekly": weekly_steps,
            },
            "calories": {
                "consumed": daily["nutrition"]["calories_consumed"],
                "burned": daily["steps"]["calories_burned"] + daily["workouts"]["calories_burned"],
                "target": targets["calories"],
                "remaining": max(0, targets["calories"] - daily["nutrition"]["calories_consumed"]),
            },
            "nutrition": {
                "protein_g": daily["nutrition"]["protein_g"],
                "carbs_g": daily["nutrition"]["carbs_g"],
                "fat_g": daily["nutrition"]["fat_g"],
            },
            "water": {
                "consumed_ml": water_today,
                "target_ml": targets["water_ml"],
            },
            "workouts": workout_stats,
            "bmi": bmi_data,
            "weight_trend": weight_trend[-10:] if weight_trend else [],
        }
