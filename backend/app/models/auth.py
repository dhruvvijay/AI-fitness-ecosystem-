"""
Authentication-related models: tokens, OTP codes, password resets.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class AuthToken(TimestampMixin, Base):
    __tablename__ = "auth_tokens"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(512), nullable=False)
    token_type = Column(String(20), nullable=False)  # "access" or "refresh"
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    device_info = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)

    user = relationship("User", back_populates="auth_tokens")


class OTPCode(TimestampMixin, Base):
    __tablename__ = "otp_codes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    code = Column(String(10), nullable=False)
    purpose = Column(String(50), nullable=False)  # "verification", "password_reset", "login"
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    attempts = Column(Integer, default=0, nullable=False)


class PasswordReset(TimestampMixin, Base):
    __tablename__ = "password_resets"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
