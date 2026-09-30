"""
User repository — data access for users and profiles.
"""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.repositories.base import BaseRepository
from app.models.user import User, UserProfile, UserSettings


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.profile))
            .where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_with_profile(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.profile), selectinload(User.settings))
            .where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_user(
        self, email: str, hashed_password: str, full_name: str, role: str = "user"
    ) -> User:
        user = await self.create(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
        )
        return user

    async def create_profile(self, user_id: int, **kwargs) -> UserProfile:
        profile = UserProfile(user_id=user_id, **kwargs)
        self.db.add(profile)
        await self.db.flush()
        await self.db.refresh(profile)
        return profile

    async def update_profile(self, user_id: int, **kwargs) -> Optional[UserProfile]:
        result = await self.db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()
        if not profile:
            return await self.create_profile(user_id, **kwargs)
        for key, value in kwargs.items():
            if hasattr(profile, key) and value is not None:
                setattr(profile, key, value)
        await self.db.flush()
        await self.db.refresh(profile)
        return profile

    async def get_or_create_settings(self, user_id: int) -> UserSettings:
        result = await self.db.execute(
            select(UserSettings).where(UserSettings.user_id == user_id)
        )
        settings = result.scalar_one_or_none()
        if not settings:
            settings = UserSettings(user_id=user_id)
            self.db.add(settings)
            await self.db.flush()
            await self.db.refresh(settings)
        return settings
