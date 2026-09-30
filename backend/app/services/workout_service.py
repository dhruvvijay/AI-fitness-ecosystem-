"""
Workout service — session management, plan creation, and exercise library.
"""

from datetime import date, datetime, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.workout_repository import (
    WorkoutRepository, WorkoutPlanRepository, ExerciseRepository,
)
from app.core.exceptions import NotFoundException


class WorkoutService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.workout_repo = WorkoutRepository(db)
        self.plan_repo = WorkoutPlanRepository(db)
        self.exercise_repo = ExerciseRepository(db)

    # ── Exercise Library ─────────────────────────────────────────

    async def search_exercises(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        muscle: Optional[str] = None,
        equipment: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> dict:
        offset = (page - 1) * limit
        exercises, total = await self.exercise_repo.search(
            query=query, category=category, difficulty=difficulty,
            muscle=muscle, equipment=equipment, offset=offset, limit=limit,
        )
        return {
            "items": [self._exercise_to_dict(e) for e in exercises],
            "total": total,
            "page": page,
            "limit": limit,
        }

    async def get_exercise(self, exercise_id: int) -> dict:
        exercise = await self.exercise_repo.get_by_id(exercise_id)
        if not exercise:
            raise NotFoundException("Exercise", exercise_id)
        return self._exercise_to_dict(exercise)

    # ── Workout Sessions ─────────────────────────────────────────

    async def start_workout(
        self, user_id: int, name: str = "Workout", workout_type: str = "general", plan_id: Optional[int] = None
    ) -> dict:
        session = await self.workout_repo.create_session(
            user_id=user_id, name=name, workout_type=workout_type,
            plan_id=plan_id, started_at=datetime.now(timezone.utc),
        )
        return self._session_to_dict(session)

    async def complete_workout(self, user_id: int, session_id: int, **kwargs) -> dict:
        session = await self.workout_repo.get_session_with_exercises(session_id)
        if not session or session.user_id != user_id:
            raise NotFoundException("Workout Session", session_id)

        session.is_completed = True
        session.ended_at = datetime.now(timezone.utc)
        if session.started_at:
            session.duration_minutes = int(
                (session.ended_at - session.started_at).total_seconds() / 60
            )
        for k, v in kwargs.items():
            if hasattr(session, k):
                setattr(session, k, v)
        await self.db.flush()
        await self.db.refresh(session)
        return self._session_to_dict(session)

    async def log_exercise_set(
        self, user_id: int, session_id: int, exercise_id: int, sets_data: list[dict]
    ) -> dict:
        session = await self.workout_repo.get_by_id(session_id)
        if not session or session.user_id != user_id:
            raise NotFoundException("Workout Session", session_id)

        total_reps = sum(s.get("reps", 0) for s in sets_data)
        total_weight = sum(s.get("reps", 0) * s.get("weight_kg", 0) for s in sets_data)

        entry = await self.workout_repo.add_exercise_to_session(
            session_id=session_id,
            exercise_id=exercise_id,
            sets_data=sets_data,
            total_sets=len(sets_data),
            total_reps=total_reps,
            total_weight_kg=total_weight,
            is_completed=True,
        )
        return {"id": entry.id, "exercise_id": exercise_id, "total_sets": len(sets_data), "total_reps": total_reps}

    async def get_user_sessions(self, user_id: int, days: int = 30) -> list[dict]:
        from datetime import timedelta
        start = date.today() - timedelta(days=days)
        sessions = await self.workout_repo.get_user_sessions(user_id, start, date.today())
        return [self._session_to_dict(s) for s in sessions]

    async def get_workout_stats(self, user_id: int, days: int = 30) -> dict:
        return await self.workout_repo.get_workout_stats(user_id, days)

    # ── Workout Plans ────────────────────────────────────────────

    async def get_user_plans(self, user_id: int) -> list[dict]:
        plans = await self.plan_repo.get_user_plans(user_id)
        return [self._plan_to_dict(p) for p in plans]

    async def get_active_plan(self, user_id: int) -> Optional[dict]:
        plan = await self.plan_repo.get_active_plan(user_id)
        return self._plan_to_dict(plan) if plan else None

    # ── Serializers ──────────────────────────────────────────────

    @staticmethod
    def _exercise_to_dict(e) -> dict:
        return {
            "id": e.id,
            "name": e.name,
            "description": e.description,
            "category": e.category,
            "difficulty": e.difficulty,
            "equipment": e.equipment,
            "primary_muscle": e.primary_muscle,
            "secondary_muscles": e.secondary_muscles,
            "instructions": e.instructions,
            "tips": e.tips,
            "common_mistakes": e.common_mistakes,
            "calories_per_minute": e.calories_per_minute,
            "image_url": e.image_url,
            "default_sets": e.default_sets,
            "default_reps": e.default_reps,
            "default_rest_seconds": e.default_rest_seconds,
            "met_value": e.met_value,
        }

    @staticmethod
    def _session_to_dict(s) -> dict:
        return {
            "id": s.id,
            "date": s.date.isoformat(),
            "name": s.name,
            "workout_type": s.workout_type,
            "duration_minutes": s.duration_minutes,
            "calories_burned": s.total_calories_burned,
            "total_volume_kg": s.total_volume_kg,
            "is_completed": s.is_completed,
            "rating": s.rating,
            "exercises": [
                {
                    "id": ex.id,
                    "exercise_id": ex.exercise_id,
                    "sets_data": ex.sets_data,
                    "total_sets": ex.total_sets,
                    "total_reps": ex.total_reps,
                    "total_weight_kg": ex.total_weight_kg,
                    "is_completed": ex.is_completed,
                }
                for ex in (s.exercises or [])
            ],
        }

    @staticmethod
    def _plan_to_dict(p) -> dict:
        return {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "plan_type": p.plan_type,
            "goal": p.goal,
            "difficulty": p.difficulty,
            "days_per_week": p.days_per_week,
            "duration_weeks": p.duration_weeks,
            "is_active": p.is_active,
            "schedule": p.schedule,
        }
