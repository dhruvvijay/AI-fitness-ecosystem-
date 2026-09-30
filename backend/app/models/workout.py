"""
Workout and Exercise models.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Date, DateTime, Text,
    ForeignKey, JSON, Enum as SAEnum,
)
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class Exercise(TimestampMixin, Base):
    __tablename__ = "exercises"

    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)  # "strength", "cardio", "flexibility", "hiit"
    difficulty = Column(SAEnum("beginner", "intermediate", "advanced", name="difficulty_level"), nullable=False)
    equipment = Column(String(255), nullable=True)  # "barbell", "dumbbell", "bodyweight", etc.
    primary_muscle = Column(String(100), nullable=False)
    secondary_muscles = Column(JSON, nullable=True)
    instructions = Column(JSON, nullable=True)  # List of step strings
    tips = Column(JSON, nullable=True)
    common_mistakes = Column(JSON, nullable=True)
    calories_per_minute = Column(Float, default=5.0)
    image_url = Column(String(500), nullable=True)
    animation_url = Column(String(500), nullable=True)
    default_sets = Column(Integer, default=3)
    default_reps = Column(Integer, default=10)
    default_rest_seconds = Column(Integer, default=60)
    is_compound = Column(Boolean, default=False)
    met_value = Column(Float, default=5.0)  # Metabolic Equivalent of Task

    videos = relationship("ExerciseVideo", back_populates="exercise", cascade="all, delete-orphan")
    muscles = relationship("ExerciseMuscle", back_populates="exercise", cascade="all, delete-orphan")


class ExerciseVideo(TimestampMixin, Base):
    __tablename__ = "exercise_videos"

    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False, index=True)
    youtube_id = Column(String(20), nullable=False)
    title = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    is_primary = Column(Boolean, default=False)

    exercise = relationship("Exercise", back_populates="videos")


class ExerciseMuscle(TimestampMixin, Base):
    __tablename__ = "exercise_muscles"

    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False, index=True)
    muscle_name = Column(String(100), nullable=False)
    involvement = Column(SAEnum("primary", "secondary", "stabilizer", name="muscle_involvement"), nullable=False)


    exercise = relationship("Exercise", back_populates="muscles")


class WorkoutPlan(TimestampMixin, Base):
    __tablename__ = "workout_plans"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    plan_type = Column(String(50), nullable=False)  # "ppl", "upper_lower", "bro_split", "full_body"
    goal = Column(String(50), nullable=False)  # "strength", "hypertrophy", "fat_loss", "cardio"
    difficulty = Column(SAEnum("beginner", "intermediate", "advanced", name="plan_difficulty"), nullable=False)
    location = Column(SAEnum("home", "gym", "outdoor", name="workout_location"), default="gym")
    days_per_week = Column(Integer, default=4)
    duration_weeks = Column(Integer, default=8)
    is_ai_generated = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    schedule = Column(JSON, nullable=True)  # {"monday": "push", "tuesday": "pull", ...}

    user = relationship("User", back_populates="workout_plans")
    exercises = relationship("WorkoutPlanExercise", back_populates="plan", cascade="all, delete-orphan")


class WorkoutPlanExercise(TimestampMixin, Base):
    __tablename__ = "workout_plan_exercises"

    plan_id = Column(Integer, ForeignKey("workout_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False, index=True)
    day = Column(String(20), nullable=False)  # "monday", "push", "day_1"
    order_index = Column(Integer, default=0)
    sets = Column(Integer, default=3)
    reps = Column(String(20), default="8-12")
    rest_seconds = Column(Integer, default=60)
    weight_kg = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    superset_group = Column(Integer, nullable=True)

    plan = relationship("WorkoutPlan", back_populates="exercises")
    exercise = relationship("Exercise")


class WorkoutSession(TimestampMixin, Base):
    __tablename__ = "workout_sessions"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("workout_plans.id"), nullable=True, index=True)
    date = Column(Date, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    workout_type = Column(String(50), nullable=True)
    duration_minutes = Column(Integer, default=0)
    total_calories_burned = Column(Float, default=0.0)
    total_volume_kg = Column(Float, default=0.0)  # Total weight × reps
    avg_heart_rate = Column(Integer, nullable=True)
    max_heart_rate = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 user satisfaction
    is_completed = Column(Boolean, default=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="workout_sessions")
    exercises = relationship("WorkoutSessionExercise", back_populates="session", cascade="all, delete-orphan")


class WorkoutSessionExercise(TimestampMixin, Base):
    __tablename__ = "workout_session_exercises"

    session_id = Column(Integer, ForeignKey("workout_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False, index=True)
    order_index = Column(Integer, default=0)
    sets_data = Column(JSON, nullable=True)  # [{"set": 1, "reps": 10, "weight_kg": 50}, ...]
    total_sets = Column(Integer, default=0)
    total_reps = Column(Integer, default=0)
    total_weight_kg = Column(Float, default=0.0)
    calories_burned = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)

    session = relationship("WorkoutSession", back_populates="exercises")
    exercise = relationship("Exercise")
