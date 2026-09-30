"""
Social features: Achievements, Challenges, Notifications, Devices.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Date, DateTime, Text,
    ForeignKey, JSON, Enum as SAEnum,
)
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class Achievement(TimestampMixin, Base):
    __tablename__ = "achievements"

    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)  # "steps", "workout", "nutrition", "streak", "milestone"
    icon = Column(String(100), nullable=True)
    badge_color = Column(String(20), nullable=True)
    requirement_type = Column(String(50), nullable=False)  # "count", "streak", "total"
    requirement_value = Column(Float, nullable=False)
    requirement_unit = Column(String(50), nullable=True)  # "steps", "days", "kg", "meals"
    xp_reward = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)

    user_achievements = relationship("UserAchievement", back_populates="achievement")


class UserAchievement(TimestampMixin, Base):
    __tablename__ = "user_achievements"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False, index=True)
    earned_at = Column(DateTime(timezone=True), nullable=False)
    progress = Column(Float, default=0.0)
    is_completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")


class Challenge(TimestampMixin, Base):
    __tablename__ = "challenges"

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    challenge_type = Column(SAEnum("daily", "weekly", "monthly", name="challenge_type"), nullable=False)
    category = Column(String(50), nullable=False)  # "steps", "workout", "nutrition", "water"
    target_value = Column(Float, nullable=False)
    target_unit = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    xp_reward = Column(Integer, default=50)
    is_active = Column(Boolean, default=True)
    icon = Column(String(100), nullable=True)

    participants = relationship("UserChallenge", back_populates="challenge")


class UserChallenge(TimestampMixin, Base):
    __tablename__ = "user_challenges"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False, index=True)
    progress = Column(Float, default=0.0)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    challenge = relationship("Challenge", back_populates="participants")


class Notification(TimestampMixin, Base):
    __tablename__ = "notifications"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # "achievement", "reminder", "system", "social"
    is_read = Column(Boolean, default=False)
    action_url = Column(String(500), nullable=True)
    data = Column(JSON, nullable=True)

    user = relationship("User", back_populates="notifications")


class Device(TimestampMixin, Base):
    __tablename__ = "devices"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    device_name = Column(String(255), nullable=False)
    device_type = Column(String(50), nullable=False)  # "fitness_band", "smart_watch", "heart_rate", "scale", "step_counter"
    bluetooth_id = Column(String(255), nullable=True)
    is_connected = Column(Boolean, default=False)
    last_sync_at = Column(DateTime(timezone=True), nullable=True)
    battery_level = Column(Integer, nullable=True)
    firmware_version = Column(String(50), nullable=True)

    user = relationship("User", back_populates="devices")
    sync_data = relationship("DeviceSyncData", back_populates="device", cascade="all, delete-orphan")


class DeviceSyncData(TimestampMixin, Base):
    __tablename__ = "device_sync_data"

    device_id = Column(Integer, ForeignKey("devices.id", ondelete="CASCADE"), nullable=False, index=True)
    sync_type = Column(String(50), nullable=False)  # "heart_rate", "steps", "calories", "sleep"
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=True)
    recorded_at = Column(DateTime(timezone=True), nullable=False)
    raw_data = Column(JSON, nullable=True)

    device = relationship("Device", back_populates="sync_data")
