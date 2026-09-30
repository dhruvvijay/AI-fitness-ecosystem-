"""
Workout repository — sessions, plans, and exercise library queries.
"""

from datetime import date, timedelta
from typing import Optional, Sequence
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.repositories.base import BaseRepository
from app.models.workout import (
    Exercise, WorkoutPlan, WorkoutPlanExercise,
    WorkoutSession, WorkoutSessionExercise,
)


class ExerciseRepository(BaseRepository[Exercise]):
    def __init__(self, db: AsyncSession):
        super().__init__(Exercise, db)

    async def search(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        muscle: Optional[str] = None,
        equipment: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Exercise], int]:
        stmt = select(Exercise)
        count_stmt = select(func.count(Exercise.id))

        filters = []
        if query:
            filters.append(Exercise.name.ilike(f"%{query}%"))
        if category:
            filters.append(Exercise.category == category)
        if difficulty:
            filters.append(Exercise.difficulty == difficulty)
        if muscle:
            filters.append(Exercise.primary_muscle.ilike(f"%{muscle}%"))
        if equipment:
            filters.append(Exercise.equipment.ilike(f"%{equipment}%"))

        for f in filters:
            stmt = stmt.where(f)
            count_stmt = count_stmt.where(f)

        total = (await self.db.execute(count_stmt)).scalar() or 0
        result = await self.db.execute(
            stmt.order_by(Exercise.name).offset(offset).limit(limit)
        )
        return list(result.scalars().all()), total


class WorkoutRepository(BaseRepository[WorkoutSession]):
    def __init__(self, db: AsyncSession):
        super().__init__(WorkoutSession, db)

    async def get_user_sessions(
        self, user_id: int, start_date: date, end_date: date
    ) -> Sequence[WorkoutSession]:
        result = await self.db.execute(
            select(WorkoutSession)
            .options(selectinload(WorkoutSession.exercises))
            .where(
                WorkoutSession.user_id == user_id,
                WorkoutSession.date >= start_date,
                WorkoutSession.date <= end_date,
            )
            .order_by(WorkoutSession.date.desc())
        )
        return result.scalars().all()

    async def get_session_with_exercises(self, session_id: int) -> Optional[WorkoutSession]:
        result = await self.db.execute(
            select(WorkoutSession)
            .options(selectinload(WorkoutSession.exercises))
            .where(WorkoutSession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def create_session(self, user_id: int, **kwargs) -> WorkoutSession:
        session = WorkoutSession(user_id=user_id, date=date.today(), **kwargs)
        self.db.add(session)
        await self.db.flush()
        await self.db.refresh(session)
        return session

    async def add_exercise_to_session(
        self, session_id: int, exercise_id: int, **kwargs
    ) -> WorkoutSessionExercise:
        entry = WorkoutSessionExercise(
            session_id=session_id, exercise_id=exercise_id, **kwargs
        )
        self.db.add(entry)
        await self.db.flush()
        await self.db.refresh(entry)
        return entry

    async def get_workout_stats(self, user_id: int, days: int = 30) -> dict:
        start = date.today() - timedelta(days=days)
        result = await self.db.execute(
            select(
                func.count(WorkoutSession.id).label("total_workouts"),
                func.coalesce(func.sum(WorkoutSession.duration_minutes), 0).label("total_minutes"),
                func.coalesce(func.sum(WorkoutSession.total_calories_burned), 0).label("total_calories"),
                func.coalesce(func.sum(WorkoutSession.total_volume_kg), 0).label("total_volume"),
                func.coalesce(func.avg(WorkoutSession.duration_minutes), 0).label("avg_duration"),
            ).where(
                WorkoutSession.user_id == user_id,
                WorkoutSession.date >= start,
                WorkoutSession.is_completed == True,
            )
        )
        row = result.one()
        return {
            "total_workouts": int(row.total_workouts),
            "total_minutes": int(row.total_minutes),
            "total_calories_burned": float(row.total_calories),
            "total_volume_kg": float(row.total_volume),
            "avg_duration_minutes": round(float(row.avg_duration)),
            "period_days": days,
        }


class WorkoutPlanRepository(BaseRepository[WorkoutPlan]):
    def __init__(self, db: AsyncSession):
        super().__init__(WorkoutPlan, db)

    async def get_user_plans(self, user_id: int) -> Sequence[WorkoutPlan]:
        result = await self.db.execute(
            select(WorkoutPlan)
            .options(selectinload(WorkoutPlan.exercises))
            .where(WorkoutPlan.user_id == user_id)
            .order_by(WorkoutPlan.created_at.desc())
        )
        return result.scalars().all()

    async def get_active_plan(self, user_id: int) -> Optional[WorkoutPlan]:
        result = await self.db.execute(
            select(WorkoutPlan)
            .options(selectinload(WorkoutPlan.exercises))
            .where(WorkoutPlan.user_id == user_id, WorkoutPlan.is_active == True)
            .limit(1)
        )
        return result.scalar_one_or_none()
