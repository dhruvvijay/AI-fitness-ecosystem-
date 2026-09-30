"""
Steps service — step tracking, statistics, and streak management.
"""

from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.steps_repository import StepsRepository
from app.repositories.user_repository import UserRepository
from app.utils.calculations import steps_to_distance_km, steps_to_calories
from app.utils.validators import validate_steps


class StepsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.steps_repo = StepsRepository(db)
        self.user_repo = UserRepository(db)

    async def log_steps(
        self, user_id: int, steps: int, target_date: date = None, source: str = "manual"
    ) -> dict:
        target_date = target_date or date.today()
        steps = validate_steps(steps)

        # Get user profile for distance/calorie calculations
        user = await self.user_repo.get_with_profile(user_id)
        profile = user.profile if user else None
        height = profile.height_cm if profile else 170
        weight = profile.weight_kg if profile else 70
        goal = profile.daily_step_target if profile else 10000

        distance = steps_to_distance_km(steps, height)
        calories = steps_to_calories(steps, weight)

        record = await self.steps_repo.upsert_daily_steps(
            user_id=user_id,
            target_date=target_date,
            steps=steps,
            distance_km=distance,
            calories_burned=calories,
            source=source,
            goal_steps=goal,
        )

        return self._record_to_dict(record)

    async def get_today(self, user_id: int) -> dict:
        record = await self.steps_repo.get_by_user_date(user_id, date.today())
        if not record:
            return {"date": date.today().isoformat(), "steps": 0, "distance_km": 0, "calories_burned": 0, "goal_steps": 10000, "goal_completed": False}
        return self._record_to_dict(record)

    async def get_week(self, user_id: int) -> list[dict]:
        today = date.today()
        start = today - timedelta(days=6)
        records = await self.steps_repo.get_range(user_id, start, today)
        records_by_date = {r.date: r for r in records}

        result = []
        for i in range(7):
            d = start + timedelta(days=i)
            r = records_by_date.get(d)
            result.append({
                "date": d.isoformat(),
                "day": d.strftime("%a"),
                "steps": r.total_steps if r else 0,
                "distance_km": r.distance_km if r else 0,
                "calories_burned": r.calories_burned if r else 0,
                "goal_completed": r.goal_completed if r else False,
            })
        return result

    async def get_month(self, user_id: int) -> list[dict]:
        today = date.today()
        start = today - timedelta(days=29)
        records = await self.steps_repo.get_range(user_id, start, today)
        records_by_date = {r.date: r for r in records}

        result = []
        for i in range(30):
            d = start + timedelta(days=i)
            r = records_by_date.get(d)
            result.append({
                "date": d.isoformat(),
                "steps": r.total_steps if r else 0,
            })
        return result

    async def get_statistics(self, user_id: int, days: int = 30) -> dict:
        stats = await self.steps_repo.get_statistics(user_id, days)
        stats["streak"] = await self.steps_repo.get_streak(user_id)
        return stats

    @staticmethod
    def _record_to_dict(record) -> dict:
        return {
            "id": record.id,
            "date": record.date.isoformat(),
            "steps": record.total_steps,
            "distance_km": record.distance_km,
            "calories_burned": record.calories_burned,
            "walking_minutes": record.walking_minutes,
            "running_minutes": record.running_minutes,
            "goal_steps": record.goal_steps,
            "goal_completed": record.goal_completed,
            "source": record.source,
        }
