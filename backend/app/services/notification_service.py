"""
Notification service — create, list, and mark notifications.
"""

from typing import Optional
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.models.social import Notification


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self, user_id: int, title: str, message: str,
        notification_type: str = "system", action_url: Optional[str] = None,
    ) -> dict:
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            action_url=action_url,
        )
        self.db.add(notif)
        await self.db.flush()
        await self.db.refresh(notif)
        return self._to_dict(notif)

    async def get_user_notifications(
        self, user_id: int, unread_only: bool = False, limit: int = 50
    ) -> list[dict]:
        stmt = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            stmt = stmt.where(Notification.is_read == False)
        stmt = stmt.order_by(Notification.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return [self._to_dict(n) for n in result.scalars().all()]

    async def mark_read(self, user_id: int, notification_id: int) -> bool:
        result = await self.db.execute(
            select(Notification).where(
                Notification.id == notification_id, Notification.user_id == user_id
            )
        )
        notif = result.scalar_one_or_none()
        if notif:
            notif.is_read = True
            await self.db.flush()
            return True
        return False

    async def mark_all_read(self, user_id: int) -> int:
        result = await self.db.execute(
            update(Notification)
            .where(Notification.user_id == user_id, Notification.is_read == False)
            .values(is_read=True)
        )
        await self.db.flush()
        return result.rowcount

    async def get_unread_count(self, user_id: int) -> int:
        result = await self.db.execute(
            select(func.count(Notification.id)).where(
                Notification.user_id == user_id, Notification.is_read == False
            )
        )
        return result.scalar() or 0

    @staticmethod
    def _to_dict(n) -> dict:
        return {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "type": n.notification_type,
            "is_read": n.is_read,
            "action_url": n.action_url,
            "created_at": n.created_at.isoformat() if n.created_at else None,
        }
