"""
Auth API endpoints — register, login, refresh, profile.
All wired to AuthService → UserRepository → MySQL.
"""

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.auth_service import AuthService
from app.core.responses import success_response

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ── Schemas ──────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=255)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class ProfileUpdateRequest(BaseModel):
    full_name: str | None = None
    height_cm: float | None = None
    weight_kg: float | None = None
    target_weight_kg: float | None = None
    date_of_birth: str | None = None  # ISO format
    gender: str | None = None
    activity_level: str | None = None
    fitness_goal: str | None = None
    diet_preference: str | None = None
    daily_calorie_target: int | None = None
    daily_protein_target: int | None = None
    daily_water_target_ml: int | None = None
    daily_step_target: int | None = None


# ── Endpoints ────────────────────────────────────────────────────

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Register a new user account."""
    service = AuthService(db)
    result = await service.register(
        email=body.email, password=body.password, full_name=body.full_name
    )
    return success_response(data=result, message="Registration successful", status_code=201)


@router.post("/login")
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticate and receive JWT tokens."""
    service = AuthService(db)
    result = await service.login(email=body.email, password=body.password)
    return success_response(data=result, message="Login successful")


@router.post("/refresh")
async def refresh_token(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    """Exchange a refresh token for a new access token."""
    service = AuthService(db)
    result = await service.refresh_token(body.refresh_token)
    return success_response(data=result, message="Token refreshed")


@router.get("/me")
async def get_me(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current authenticated user with profile."""
    service = AuthService(db)
    result = await service.get_current_user(user.id)
    return success_response(data=result)


@router.put("/me/profile")
async def update_profile(
    body: ProfileUpdateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update user profile."""
    service = AuthService(db)
    update_data = body.model_dump(exclude_none=True)
    # Convert date_of_birth string to date object
    if "date_of_birth" in update_data:
        from datetime import date
        update_data["date_of_birth"] = date.fromisoformat(update_data["date_of_birth"])
    result = await service.update_profile(user.id, **update_data)
    return success_response(data=result, message="Profile updated")


@router.post("/logout")
async def logout(user: User = Depends(get_current_user)):
    """Logout (client should discard tokens)."""
    return success_response(message="Logged out successfully")
