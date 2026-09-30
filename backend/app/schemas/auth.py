"""
Pydantic schemas for authentication requests and responses.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


# ── Request Schemas ──────────────────────────────────────────────

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=255)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class GoogleAuthRequest(BaseModel):
    token: str  # Google ID token


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        return v


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6)
    purpose: str = Field(default="verification")


class UpdateProfileRequest(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = Field(None, ge=50, le=300)
    weight_kg: Optional[float] = Field(None, ge=20, le=500)
    target_weight_kg: Optional[float] = Field(None, ge=20, le=500)
    activity_level: Optional[str] = None
    fitness_goal: Optional[str] = None
    diet_preference: Optional[str] = None
    daily_calorie_target: Optional[int] = Field(None, ge=500, le=10000)
    daily_protein_target: Optional[int] = Field(None, ge=10, le=500)
    daily_water_target_ml: Optional[int] = Field(None, ge=500, le=10000)
    daily_step_target: Optional[int] = Field(None, ge=1000, le=100000)
    bio: Optional[str] = None


# ── Response Schemas ─────────────────────────────────────────────

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    is_verified: bool
    auth_provider: str
    avatar_url: Optional[str] = None

    model_config = {"from_attributes": True}


class UserProfileResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    avatar_url: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    target_weight_kg: Optional[float] = None
    activity_level: Optional[str] = None
    fitness_goal: Optional[str] = None
    diet_preference: Optional[str] = None
    body_fat_percentage: Optional[float] = None
    daily_calorie_target: Optional[int] = None
    daily_protein_target: Optional[int] = None
    daily_water_target_ml: Optional[int] = None
    daily_step_target: Optional[int] = None

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    user: UserResponse
    tokens: TokenResponse


class MessageResponse(BaseModel):
    message: str
    success: bool = True
