"""
Progress repository — weight tracking and body composition over time.
"""

from datetime import date, timedelta
from typing import Sequence
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fitness import BMIRecord, BodyMeasurement, CalorieLog, WaterLog


class ProgressRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_weight_trend(self, user_id: int, days: int = 90) -> list[dict]:
        start = date.today() - timedelta(days=days)
        result = await self.db.execute(
            select(BMIRecord.date, BMIRecord.weight_kg, BMIRecord.bmi, BMIRecord.body_fat_percentage)
            .where(BMIRecord.user_id == user_id, BMIRecord.date >= start)
            .order_by(BMIRecord.date)
        )
        return [
            {
                "date": r[0].isoformat(),
                "weight_kg": float(r[1]),
                "bmi": float(r[2]),
                "body_fat": float(r[3]) if r[3] else None,
            }
            for r in result.all()
        ]

    async def get_water_today(self, user_id: int) -> int:
        result = await self.db.execute(
            select(func.coalesce(func.sum(WaterLog.amount_ml), 0))
            .where(WaterLog.user_id == user_id, WaterLog.date == date.today())
        )
        return result.scalar() or 0

    async def log_water(self, user_id: int, amount_ml: int) -> WaterLog:
        log = WaterLog(user_id=user_id, date=date.today(), amount_ml=amount_ml)
        self.db.add(log)
        await self.db.flush()
        await self.db.refresh(log)
        return log

    async def get_calorie_logs(
        self, user_id: int, target_date: date
    ) -> list[CalorieLog]:
        result = await self.db.execute(
            select(CalorieLog)
            .where(CalorieLog.user_id == user_id, CalorieLog.date == target_date)
            .order_by(CalorieLog.created_at)
        )
        return list(result.scalars().all())

    async def log_calories(self, user_id: int, **kwargs) -> CalorieLog:
        log = CalorieLog(user_id=user_id, date=date.today(), **kwargs)
        self.db.add(log)
        await self.db.flush()
        await self.db.refresh(log)
        return log
