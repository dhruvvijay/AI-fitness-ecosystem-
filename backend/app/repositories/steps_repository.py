"""
Steps repository — daily/hourly step tracking and statistics.
"""

from datetime import date, timedelta
from typing import Optional, Sequence
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.models.fitness import StepsDaily, StepsHourly


class StepsRepository(BaseRepository[StepsDaily]):
    def __init__(self, db: AsyncSession):
        super().__init__(StepsDaily, db)

    async def get_by_user_date(self, user_id: int, target_date: date) -> Optional[StepsDaily]:
        result = await self.db.execute(
            select(StepsDaily).where(
                StepsDaily.user_id == user_id, StepsDaily.date == target_date
            )
        )
        return result.scalar_one_or_none()

    async def upsert_daily_steps(
        self, user_id: int, target_date: date, steps: int, **kwargs
    ) -> StepsDaily:
        """Create or update daily step record (prevent duplicates)."""
        existing = await self.get_by_user_date(user_id, target_date)
        if existing:
            existing.total_steps = steps
            for k, v in kwargs.items():
                if hasattr(existing, k):
                    setattr(existing, k, v)
            existing.goal_completed = steps >= existing.goal_steps
            await self.db.flush()
            await self.db.refresh(existing)
            return existing
        record = StepsDaily(
            user_id=user_id, date=target_date, total_steps=steps,
            goal_completed=steps >= kwargs.get("goal_steps", 10000),
            **kwargs,
        )
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def get_range(
        self, user_id: int, start_date: date, end_date: date
    ) -> Sequence[StepsDaily]:
        result = await self.db.execute(
            select(StepsDaily)
            .where(
                StepsDaily.user_id == user_id,
                StepsDaily.date >= start_date,
                StepsDaily.date <= end_date,
            )
            .order_by(StepsDaily.date)
        )
        return result.scalars().all()

    async def get_statistics(self, user_id: int, days: int = 30) -> dict:
        start = date.today() - timedelta(days=days)
        result = await self.db.execute(
            select(
                func.coalesce(func.sum(StepsDaily.total_steps), 0).label("total"),
                func.coalesce(func.avg(StepsDaily.total_steps), 0).label("avg"),
                func.coalesce(func.max(StepsDaily.total_steps), 0).label("max"),
                func.coalesce(func.min(StepsDaily.total_steps), 0).label("min"),
                func.count(StepsDaily.id).label("days_tracked"),
                func.sum(func.cast(StepsDaily.goal_completed, type_=func.integer_types[0] if hasattr(func, 'integer_types') else StepsDaily.goal_completed.type)).label("goals_met"),
            ).where(StepsDaily.user_id == user_id, StepsDaily.date >= start)
        )
        row = result.one()
        return {
            "total_steps": int(row.total),
            "avg_steps": round(float(row.avg)),
            "max_steps": int(row.max),
            "min_steps": int(row.min),
            "days_tracked": int(row.days_tracked),
            "period_days": days,
        }

    async def get_streak(self, user_id: int) -> int:
        """Calculate consecutive days with goal completed, ending today."""
        streak = 0
        current_date = date.today()
        while True:
            record = await self.get_by_user_date(user_id, current_date)
            if record and record.goal_completed:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        return streak
