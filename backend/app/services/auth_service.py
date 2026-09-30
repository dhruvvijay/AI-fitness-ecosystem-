"""
Authentication service — registration, login, JWT management, password reset.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import (
    ConflictException, UnauthorizedException, NotFoundException, ValidationException,
)
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def register(
        self, email: str, password: str, full_name: str
    ) -> dict:
        """Register a new user. Returns user data + tokens."""
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise ConflictException("A user with this email already exists")

        if len(password) < 8:
            raise ValidationException("Password must be at least 8 characters")

        hashed = hash_password(password)
        user = await self.user_repo.create_user(
            email=email, hashed_password=hashed, full_name=full_name
        )

        # Create default profile
        await self.user_repo.create_profile(user.id)
        await self.user_repo.get_or_create_settings(user.id)

        tokens = self._generate_tokens(user.id, user.role)
        logger.info(f"User registered: {email} (id={user.id})")

        return {
            "user": self._user_to_dict(user),
            "tokens": tokens,
        }

    async def login(self, email: str, password: str) -> dict:
        """Authenticate user and return tokens."""
        user = await self.user_repo.get_by_email(email)
        if not user or not user.hashed_password:
            raise UnauthorizedException("Invalid email or password")

        if not verify_password(password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")

        if not user.is_active:
            raise UnauthorizedException("Account is deactivated")

        # Update last login
        user.last_login = datetime.now(timezone.utc).isoformat()
        await self.db.flush()

        tokens = self._generate_tokens(user.id, user.role)
        logger.info(f"User logged in: {email}")

        return {
            "user": self._user_to_dict(user),
            "tokens": tokens,
        }

    async def refresh_token(self, refresh_token: str) -> dict:
        """Generate new access token from valid refresh token."""
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid or expired refresh token")

        user_id = payload.get("sub")
        user = await self.user_repo.get_by_id(int(user_id))
        if not user or not user.is_active:
            raise UnauthorizedException("User not found or inactive")

        tokens = self._generate_tokens(user.id, user.role)
        return {"tokens": tokens}

    async def get_current_user(self, user_id: int) -> dict:
        """Get current user with profile."""
        user = await self.user_repo.get_with_profile(user_id)
        if not user:
            raise NotFoundException("User", user_id)
        return self._user_to_dict(user, include_profile=True)

    async def update_profile(self, user_id: int, **kwargs) -> dict:
        """Update user profile fields."""
        profile = await self.user_repo.update_profile(user_id, **kwargs)
        user = await self.user_repo.get_with_profile(user_id)
        return self._user_to_dict(user, include_profile=True)

    def _generate_tokens(self, user_id: int, role: str) -> dict:
        access_token = create_access_token(
            data={"sub": str(user_id), "role": role, "type": "access"}
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user_id), "role": role, "type": "refresh"}
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    @staticmethod
    def _user_to_dict(user, include_profile: bool = False) -> dict:
        data = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "avatar_url": user.avatar_url,
        }
        if include_profile and user.profile:
            p = user.profile
            data["profile"] = {
                "height_cm": p.height_cm,
                "weight_kg": p.weight_kg,
                "target_weight_kg": p.target_weight_kg,
                "activity_level": p.activity_level,
                "fitness_goal": p.fitness_goal,
                "diet_preference": p.diet_preference,
                "date_of_birth": p.date_of_birth.isoformat() if p.date_of_birth else None,
                "gender": p.gender,
                "body_fat_percentage": p.body_fat_percentage,
                "daily_calorie_target": p.daily_calorie_target,
                "daily_protein_target": p.daily_protein_target,
                "daily_water_target_ml": p.daily_water_target_ml,
                "daily_step_target": p.daily_step_target,
                "timezone": p.timezone,
            }
        return data
