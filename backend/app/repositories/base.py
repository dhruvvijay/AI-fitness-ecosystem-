"""
Base repository with generic CRUD operations for SQLAlchemy async models.
All repositories inherit from this to avoid code duplication.
"""

from typing import Any, Generic, Optional, Sequence, Type, TypeVar
from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic async CRUD repository."""

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 20,
        order_by: Any = None,
    ) -> Sequence[ModelType]:
        stmt = select(self.model)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        else:
            stmt = stmt.order_by(self.model.id.desc())
        stmt = stmt.offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def count(self, *filters) -> int:
        stmt = select(func.count(self.model.id))
        for f in filters:
            stmt = stmt.where(f)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def update_by_id(self, id: int, **kwargs) -> Optional[ModelType]:
        instance = await self.get_by_id(id)
        if instance is None:
            return None
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def delete_by_id(self, id: int) -> bool:
        instance = await self.get_by_id(id)
        if instance is None:
            return False
        await self.db.delete(instance)
        await self.db.flush()
        return True

    async def get_by_field(self, field_name: str, value: Any) -> Optional[ModelType]:
        column = getattr(self.model, field_name)
        result = await self.db.execute(select(self.model).where(column == value))
        return result.scalar_one_or_none()

    async def get_all_by_field(
        self, field_name: str, value: Any, offset: int = 0, limit: int = 100
    ) -> Sequence[ModelType]:
        column = getattr(self.model, field_name)
        stmt = (
            select(self.model)
            .where(column == value)
            .order_by(self.model.id.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
