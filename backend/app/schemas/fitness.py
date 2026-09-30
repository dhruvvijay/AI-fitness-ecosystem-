"""
Pydantic schemas for fitness tracking: steps, calories, water, BMI, body measurements.
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# ── Steps ────────────────────────────────────────────────────────

class StepLogRequest(BaseModel):
    date: date
    total_steps: int = Field(..., ge=0, le=200000)
    distance_km: Optional[float] = Field(None, ge=0)
    walking_minutes: Optional[int] = Field(None, ge=0)
    running_minutes: Optional[int] = Field(None, ge=0)
    source: str = "manual"

class StepResponse(BaseModel):
    id: int
    date: date
    total_steps: int
    distance_km: float
    calories_burned: float
    walking_minutes: int
    running_minutes: int
    goal_steps: int
    goal_completed: bool
    source: str
    model_config = {"from_attributes": True}

class StepSummary(BaseModel):
    period: str  # "daily", "weekly", "monthly"
    total_steps: int
    avg_daily_steps: int
    total_distance_km: float
    total_calories_burned: float
    goal_completion_rate: float
    best_day: Optional[date] = None
    best_day_steps: Optional[int] = None


# ── Calories ─────────────────────────────────────────────────────

class CalorieLogRequest(BaseModel):
    date: date
    log_type: str = Field(..., pattern="^(consumed|burned)$")
    amount: float = Field(..., ge=0, le=50000)
    source: Optional[str] = None
    notes: Optional[str] = None

class CalorieResponse(BaseModel):
    id: int
    date: date
    log_type: str
    amount: float
    source: Optional[str]
    notes: Optional[str]
    model_config = {"from_attributes": True}

class CalorieSummary(BaseModel):
    date: date
    consumed: float
    burned: float
    net: float
    bmr: float
    tdee: float
    target: float
    remaining: float
    deficit_surplus: float


# ── Water ────────────────────────────────────────────────────────

class WaterLogRequest(BaseModel):
    date: date
    amount_ml: int = Field(..., ge=0, le=10000)

class WaterResponse(BaseModel):
    id: int
    date: date
    amount_ml: int
    model_config = {"from_attributes": True}

class WaterSummary(BaseModel):
    date: date
    total_ml: int
    target_ml: int
    percentage: float
    glasses: float  # 1 glass = 250ml


# ── BMI ──────────────────────────────────────────────────────────

class BMIRequest(BaseModel):
    weight_kg: float = Field(..., ge=20, le=500)
    height_cm: float = Field(..., ge=50, le=300)
    age: Optional[int] = Field(None, ge=1, le=150)
    gender: Optional[str] = None
    activity_level: Optional[str] = None
    body_fat_percentage: Optional[float] = Field(None, ge=1, le=70)

class BMIResponse(BaseModel):
    bmi: float
    category: str
    healthy_weight_range: dict
    ideal_weight: float
    bmr: float
    tdee: float
    maintenance_calories: float
    recommended_calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    water_ml: int
    lean_body_mass: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    recommended_goal: str


# ── Body Measurements ────────────────────────────────────────────

class BodyMeasurementRequest(BaseModel):
    date: date
    weight_kg: Optional[float] = Field(None, ge=20, le=500)
    chest_cm: Optional[float] = Field(None, ge=30, le=200)
    waist_cm: Optional[float] = Field(None, ge=30, le=200)
    hips_cm: Optional[float] = Field(None, ge=30, le=200)
    bicep_left_cm: Optional[float] = Field(None, ge=10, le=80)
    bicep_right_cm: Optional[float] = Field(None, ge=10, le=80)
    thigh_left_cm: Optional[float] = Field(None, ge=20, le=100)
    thigh_right_cm: Optional[float] = Field(None, ge=20, le=100)
    calf_left_cm: Optional[float] = Field(None, ge=10, le=80)
    calf_right_cm: Optional[float] = Field(None, ge=10, le=80)
    neck_cm: Optional[float] = Field(None, ge=20, le=70)
    forearm_cm: Optional[float] = Field(None, ge=10, le=60)
    shoulder_cm: Optional[float] = Field(None, ge=30, le=180)
    body_fat_percentage: Optional[float] = Field(None, ge=1, le=70)
    notes: Optional[str] = None

class BodyMeasurementResponse(BaseModel):
    id: int
    date: date
    weight_kg: Optional[float]
    chest_cm: Optional[float]
    waist_cm: Optional[float]
    hips_cm: Optional[float]
    bicep_left_cm: Optional[float]
    bicep_right_cm: Optional[float]
    thigh_left_cm: Optional[float]
    thigh_right_cm: Optional[float]
    body_fat_percentage: Optional[float]
    model_config = {"from_attributes": True}


# ── Goals ────────────────────────────────────────────────────────

class GoalRequest(BaseModel):
    goal_type: str  # "weight", "calories", "protein", "water", "steps", "workout", "running", "sleep"
    target_value: float = Field(..., ge=0)
    target_unit: str
    start_date: date
    end_date: Optional[date] = None

class GoalResponse(BaseModel):
    goal_type: str
    target_value: float
    current_value: float
    target_unit: str
    progress_percentage: float
    start_date: date
    end_date: Optional[date]
    expected_completion_date: Optional[date]
    on_track: bool


# ── Dashboard ────────────────────────────────────────────────────

class DashboardSummary(BaseModel):
    today_steps: int
    today_calories_consumed: float
    today_calories_burned: float
    remaining_calories: float
    workout_time_minutes: int
    heart_rate: Optional[int] = None
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    water_ml: int
    water_target_ml: int
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None
    body_fat: Optional[float] = None
    workout_streak: int
    daily_goal_progress: float
    weekly_goal_progress: float
    monthly_goal_progress: float
    achievements_count: int
    sleep_hours: Optional[float] = None
    distance_km: float
    exercise_minutes: int
