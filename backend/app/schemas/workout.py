"""
Pydantic schemas for workouts and exercises.
"""

from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ── Exercise ─────────────────────────────────────────────────────

class ExerciseResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: str
    difficulty: str
    equipment: Optional[str]
    primary_muscle: str
    secondary_muscles: Optional[List[str]]
    instructions: Optional[List[str]]
    tips: Optional[List[str]]
    common_mistakes: Optional[List[str]]
    calories_per_minute: float
    image_url: Optional[str]
    animation_url: Optional[str]
    default_sets: int
    default_reps: int
    default_rest_seconds: int
    is_compound: bool
    videos: Optional[List[Dict[str, Any]]] = None
    model_config = {"from_attributes": True}

class ExerciseSearchRequest(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    equipment: Optional[str] = None
    muscle: Optional[str] = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


# ── Workout Plan ─────────────────────────────────────────────────

class WorkoutPlanExerciseRequest(BaseModel):
    exercise_id: int
    day: str
    order_index: int = 0
    sets: int = Field(default=3, ge=1, le=20)
    reps: str = "8-12"
    rest_seconds: int = Field(default=60, ge=0, le=600)
    weight_kg: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None

class CreateWorkoutPlanRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    plan_type: str  # "ppl", "upper_lower", "bro_split", "full_body"
    goal: str  # "strength", "hypertrophy", "fat_loss", "cardio"
    difficulty: str  # "beginner", "intermediate", "advanced"
    location: str = "gym"
    days_per_week: int = Field(default=4, ge=1, le=7)
    duration_weeks: int = Field(default=8, ge=1, le=52)
    exercises: List[WorkoutPlanExerciseRequest]

class WorkoutPlanResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    plan_type: str
    goal: str
    difficulty: str
    location: str
    days_per_week: int
    duration_weeks: int
    is_ai_generated: bool
    is_active: bool
    schedule: Optional[Dict[str, str]]
    exercises: List[Dict[str, Any]]
    model_config = {"from_attributes": True}

class GenerateWorkoutPlanRequest(BaseModel):
    goal: str = "hypertrophy"
    difficulty: str = "intermediate"
    location: str = "gym"
    plan_type: str = "ppl"
    days_per_week: int = Field(default=4, ge=1, le=7)
    duration_weeks: int = Field(default=8, ge=1, le=52)
    focus_muscles: Optional[List[str]] = None
    available_equipment: Optional[List[str]] = None
    session_duration_minutes: int = Field(default=60, ge=20, le=180)


# ── Workout Session ──────────────────────────────────────────────

class SessionExerciseSetData(BaseModel):
    set_number: int
    reps: int = Field(..., ge=0, le=500)
    weight_kg: float = Field(default=0, ge=0)
    is_completed: bool = True
    notes: Optional[str] = None

class SessionExerciseRequest(BaseModel):
    exercise_id: int
    order_index: int = 0
    sets_data: List[SessionExerciseSetData]
    notes: Optional[str] = None

class CreateWorkoutSessionRequest(BaseModel):
    plan_id: Optional[int] = None
    date: date
    name: Optional[str] = None
    workout_type: Optional[str] = None
    duration_minutes: int = Field(..., ge=0, le=600)
    avg_heart_rate: Optional[int] = Field(None, ge=30, le=250)
    max_heart_rate: Optional[int] = Field(None, ge=30, le=250)
    notes: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    exercises: List[SessionExerciseRequest]

class WorkoutSessionResponse(BaseModel):
    id: int
    date: date
    name: Optional[str]
    workout_type: Optional[str]
    duration_minutes: int
    total_calories_burned: float
    total_volume_kg: float
    avg_heart_rate: Optional[int]
    max_heart_rate: Optional[int]
    rating: Optional[int]
    is_completed: bool
    exercises: List[Dict[str, Any]]
    model_config = {"from_attributes": True}
