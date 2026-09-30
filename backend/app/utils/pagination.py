"""
Pagination utilities for offset-based and cursor-based pagination.
"""

from typing import TypeVar, Generic, Sequence
from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = 1
    limit: int = 20

    @property
    def offset(self) -> int:
        return (max(1, self.page) - 1) * self.limit


class PaginatedResult(BaseModel):
    items: list
    total: int
    page: int
    limit: int
    pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(cls, items: list, total: int, page: int, limit: int) -> "PaginatedResult":
        pages = (total + limit - 1) // limit if limit > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        )
