"""
Fitness tracking models: steps, calories, water, BMI, body measurements, progress photos.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime, Text,
    ForeignKey, Boolean, JSON,
)
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class StepsDaily(TimestampMixin, Base):
    __tablename__ = "steps_daily"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    total_steps = Column(Integer, default=0, nullable=False)
    distance_km = Column(Float, default=0.0)
    calories_burned = Column(Float, default=0.0)
    walking_minutes = Column(Integer, default=0)
    running_minutes = Column(Integer, default=0)
    goal_steps = Column(Integer, default=10000)
    goal_completed = Column(Boolean, default=False)
    source = Column(String(50), default="manual")  # "manual", "device", "google_fit"

    user = relationship("User", back_populates="steps")

    class Meta:
        unique_together = ("user_id", "date")


class StepsHourly(TimestampMixin, Base):
    __tablename__ = "steps_hourly"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    hour = Column(Integer, nullable=False)  # 0-23
    steps = Column(Integer, default=0, nullable=False)
    distance_km = Column(Float, default=0.0)
    calories_burned = Column(Float, default=0.0)


class CalorieLog(TimestampMixin, Base):
    __tablename__ = "calorie_logs"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    log_type = Column(String(20), nullable=False)  # "consumed" or "burned"
    amount = Column(Float, nullable=False)
    source = Column(String(100), nullable=True)  # "meal", "workout", "steps", "manual"
    source_id = Column(Integer, nullable=True)  # FK to meal or workout session
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="calorie_logs")


class WaterLog(TimestampMixin, Base):
    __tablename__ = "water_logs"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    amount_ml = Column(Integer, nullable=False)
    time_logged = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="water_logs")


class BMIRecord(TimestampMixin, Base):
    __tablename__ = "bmi_records"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    weight_kg = Column(Float, nullable=False)
    height_cm = Column(Float, nullable=False)
    bmi = Column(Float, nullable=False)
    body_fat_percentage = Column(Float, nullable=True)
    lean_body_mass = Column(Float, nullable=True)
    bmr = Column(Float, nullable=True)
    tdee = Column(Float, nullable=True)
    category = Column(String(50), nullable=True)  # "underweight", "normal", "overweight", "obese"
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="bmi_records")


class BodyMeasurement(TimestampMixin, Base):
    __tablename__ = "body_measurements"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    weight_kg = Column(Float, nullable=True)
    chest_cm = Column(Float, nullable=True)
    waist_cm = Column(Float, nullable=True)
    hips_cm = Column(Float, nullable=True)
    bicep_left_cm = Column(Float, nullable=True)
    bicep_right_cm = Column(Float, nullable=True)
    thigh_left_cm = Column(Float, nullable=True)
    thigh_right_cm = Column(Float, nullable=True)
    calf_left_cm = Column(Float, nullable=True)
    calf_right_cm = Column(Float, nullable=True)
    neck_cm = Column(Float, nullable=True)
    forearm_cm = Column(Float, nullable=True)
    shoulder_cm = Column(Float, nullable=True)
    body_fat_percentage = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="body_measurements")


class ProgressPhoto(TimestampMixin, Base):
    __tablename__ = "progress_photos"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    photo_url = Column(String(500), nullable=False)
    photo_type = Column(String(20), default="front")  # "front", "side", "back"
    weight_kg = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="progress_photos")
