"""
Goal repository — CRUD and progress tracking for user goals.
"""

from datetime import date
from typing import Optional, Sequence
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.models.fitness import BMIRecord, BodyMeasurement, ProgressPhoto


class GoalRepository:
    """Goals are tracked via user_profiles and body_measurements for now.
    This repo handles BMI records, body measurements, and progress photos."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ── BMI Records ──────────────────────────────────────────────

    async def create_bmi_record(self, user_id: int, **kwargs) -> BMIRecord:
        record = BMIRecord(user_id=user_id, date=date.today(), **kwargs)
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def get_bmi_history(
        self, user_id: int, limit: int = 30
    ) -> Sequence[BMIRecord]:
        result = await self.db.execute(
            select(BMIRecord)
            .where(BMIRecord.user_id == user_id)
            .order_by(BMIRecord.date.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def get_latest_bmi(self, user_id: int) -> Optional[BMIRecord]:
        result = await self.db.execute(
            select(BMIRecord)
            .where(BMIRecord.user_id == user_id)
            .order_by(BMIRecord.date.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    # ── Body Measurements ────────────────────────────────────────

    async def create_measurement(self, user_id: int, **kwargs) -> BodyMeasurement:
        m = BodyMeasurement(user_id=user_id, date=date.today(), **kwargs)
        self.db.add(m)
        await self.db.flush()
        await self.db.refresh(m)
        return m

    async def get_measurement_history(
        self, user_id: int, limit: int = 30
    ) -> Sequence[BodyMeasurement]:
        result = await self.db.execute(
            select(BodyMeasurement)
            .where(BodyMeasurement.user_id == user_id)
            .order_by(BodyMeasurement.date.desc())
            .limit(limit)
        )
        return result.scalars().all()

    # ── Progress Photos ──────────────────────────────────────────

    async def add_progress_photo(self, user_id: int, **kwargs) -> ProgressPhoto:
        photo = ProgressPhoto(user_id=user_id, date=date.today(), **kwargs)
        self.db.add(photo)
        await self.db.flush()
        await self.db.refresh(photo)
        return photo

    async def get_progress_photos(
        self, user_id: int, limit: int = 50
    ) -> Sequence[ProgressPhoto]:
        result = await self.db.execute(
            select(ProgressPhoto)
            .where(ProgressPhoto.user_id == user_id)
            .order_by(ProgressPhoto.date.desc())
            .limit(limit)
        )
        return result.scalars().all()
