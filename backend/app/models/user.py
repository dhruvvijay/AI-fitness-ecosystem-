"""
User, Profile, and Settings SQLAlchemy models.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Date, Enum as SAEnum,
    Text, ForeignKey,
)
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth users
    full_name = Column(String(255), nullable=False)
    role = Column(
        SAEnum("admin", "trainer", "user", name="user_role"),
        default="user",
        nullable=False,
    )
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    auth_provider = Column(
        SAEnum("email", "google", name="auth_provider"),
        default="email",
        nullable=False,
    )
    google_id = Column(String(255), unique=True, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    last_login = Column(String(50), nullable=True)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    auth_tokens = relationship("AuthToken", back_populates="user", cascade="all, delete-orphan")
    steps = relationship("StepsDaily", back_populates="user", cascade="all, delete-orphan")
    calorie_logs = relationship("CalorieLog", back_populates="user", cascade="all, delete-orphan")
    water_logs = relationship("WaterLog", back_populates="user", cascade="all, delete-orphan")
    bmi_records = relationship("BMIRecord", back_populates="user", cascade="all, delete-orphan")
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")
    workout_plans = relationship("WorkoutPlan", back_populates="user", cascade="all, delete-orphan")
    workout_sessions = relationship("WorkoutSession", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    devices = relationship("Device", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    ai_chats = relationship("AIChatHistory", back_populates="user", cascade="all, delete-orphan")
    body_measurements = relationship("BodyMeasurement", back_populates="user", cascade="all, delete-orphan")
    progress_photos = relationship("ProgressPhoto", back_populates="user", cascade="all, delete-orphan")


class UserProfile(TimestampMixin, Base):
    __tablename__ = "user_profiles"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(SAEnum("male", "female", "other", name="gender_type"), nullable=True)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    target_weight_kg = Column(Float, nullable=True)
    activity_level = Column(
        SAEnum("sedentary", "light", "moderate", "active", "very_active", name="activity_level"),
        default="moderate",
    )
    fitness_goal = Column(
        SAEnum("lose_weight", "maintain", "gain_muscle", "improve_fitness", name="fitness_goal"),
        default="maintain",
    )
    diet_preference = Column(
        SAEnum("none", "vegetarian", "vegan", "keto", "high_protein", "indian", name="diet_preference"),
        default="none",
    )
    body_fat_percentage = Column(Float, nullable=True)
    daily_calorie_target = Column(Integer, nullable=True)
    daily_protein_target = Column(Integer, nullable=True)
    daily_water_target_ml = Column(Integer, default=2500)
    daily_step_target = Column(Integer, default=10000)
    workout_days_per_week = Column(Integer, default=4)
    timezone = Column(String(50), default="Asia/Kolkata")
    bio = Column(Text, nullable=True)

    user = relationship("User", back_populates="profile")


class UserSettings(TimestampMixin, Base):
    __tablename__ = "user_settings"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    theme = Column(SAEnum("dark", "light", "system", name="theme_type"), default="system")
    language = Column(String(10), default="en")
    units = Column(SAEnum("metric", "imperial", name="unit_type"), default="metric")
    notifications_enabled = Column(Boolean, default=True)
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    workout_reminders = Column(Boolean, default=True)
    meal_reminders = Column(Boolean, default=True)
    water_reminders = Column(Boolean, default=True)
    privacy_profile_public = Column(Boolean, default=False)
    privacy_show_on_leaderboard = Column(Boolean, default=True)

    user = relationship("User", back_populates="settings")
