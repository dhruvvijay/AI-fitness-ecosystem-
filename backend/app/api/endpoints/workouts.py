"""
Workouts API — sessions, exercise library, plans.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.workout_service import WorkoutService
from app.core.responses import success_response

router = APIRouter(prefix="/workouts", tags=["Workouts"])


# ── Schemas ──────────────────────────────────────────────────────

class StartWorkoutRequest(BaseModel):
    name: str = "Workout"
    workout_type: str = "general"
    plan_id: Optional[int] = None

class LogExerciseSetRequest(BaseModel):
    exercise_id: int
    sets_data: list[dict]  # [{"set": 1, "reps": 10, "weight_kg": 50}, ...]

class CompleteWorkoutRequest(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None
    total_calories_burned: Optional[float] = None


# ── Endpoints ────────────────────────────────────────────────────

@router.get("/sessions")
async def get_sessions(
    days: int = Query(default=30, ge=1, le=365),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get workout sessions for the last N days."""
    service = WorkoutService(db)
    data = await service.get_user_sessions(user.id, days)
    return success_response(data=data)


@router.post("/sessions")
async def start_workout(
    body: StartWorkoutRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Start a new workout session."""
    service = WorkoutService(db)
    data = await service.start_workout(user.id, body.name, body.workout_type, body.plan_id)
    return success_response(data=data, message="Workout started")


@router.post("/sessions/{session_id}/exercises")
async def log_exercise(
    session_id: int,
    body: LogExerciseSetRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Log exercise sets in a workout session."""
    service = WorkoutService(db)
    data = await service.log_exercise_set(user.id, session_id, body.exercise_id, body.sets_data)
    return success_response(data=data, message="Exercise logged")


@router.put("/sessions/{session_id}/complete")
async def complete_workout(
    session_id: int,
    body: CompleteWorkoutRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Complete a workout session."""
    service = WorkoutService(db)
    kwargs = body.model_dump(exclude_none=True)
    data = await service.complete_workout(user.id, session_id, **kwargs)
    return success_response(data=data, message="Workout completed")


@router.get("/stats")
async def get_stats(
    days: int = Query(default=30, ge=7, le=365),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get workout statistics for the period."""
    service = WorkoutService(db)
    data = await service.get_workout_stats(user.id, days)
    return success_response(data=data)


@router.get("/plans")
async def get_plans(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's workout plans."""
    service = WorkoutService(db)
    data = await service.get_user_plans(user.id)
    return success_response(data=data)


# ── Exercise Library ─────────────────────────────────────────────

@router.get("/exercises")
async def search_exercises(
    q: Optional[str] = None,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    muscle: Optional[str] = None,
    equipment: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Search the exercise library with filters."""
    service = WorkoutService(db)
    data = await service.search_exercises(
        query=q, category=category, difficulty=difficulty,
        muscle=muscle, equipment=equipment, page=page, limit=limit,
    )
    return success_response(data=data)


@router.get("/exercises/{exercise_id}")
async def get_exercise(exercise_id: int, db: AsyncSession = Depends(get_db)):
    """Get exercise details."""
    service = WorkoutService(db)
    data = await service.get_exercise(exercise_id)
    return success_response(data=data)
