"""
Food repository — food database search and CRUD.
"""

from typing import Optional, Sequence
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.models.nutrition import Food


class FoodRepository(BaseRepository[Food]):
    def __init__(self, db: AsyncSession):
        super().__init__(Food, db)

    async def search(
        self,
        query: str,
        category: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Food], int]:
        """Full-text search on food name with optional category filter."""
        stmt = select(Food).where(
            or_(
                Food.name.ilike(f"%{query}%"),
                Food.category.ilike(f"%{query}%"),
            )
        )
        count_stmt = select(func.count(Food.id)).where(
            or_(
                Food.name.ilike(f"%{query}%"),
                Food.category.ilike(f"%{query}%"),
            )
        )
        if category:
            stmt = stmt.where(Food.category == category)
            count_stmt = count_stmt.where(Food.category == category)

        total = (await self.db.execute(count_stmt)).scalar() or 0
        result = await self.db.execute(
            stmt.order_by(Food.name).offset(offset).limit(limit)
        )
        return list(result.scalars().all()), total

    async def get_by_name(self, name: str) -> Optional[Food]:
        result = await self.db.execute(
            select(Food).where(func.lower(Food.name) == name.lower())
        )
        return result.scalar_one_or_none()

    async def get_by_barcode(self, barcode: str) -> Optional[Food]:
        return await self.get_by_field("barcode", barcode)

    async def bulk_create(self, foods_data: list[dict]) -> list[Food]:
        foods = [Food(**data) for data in foods_data]
        self.db.add_all(foods)
        await self.db.flush()
        return foods
