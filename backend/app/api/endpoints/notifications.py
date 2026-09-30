"""
Notifications API — list, mark read, unread count.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.notification_service import NotificationService
from app.core.responses import success_response

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("")
async def get_notifications(
    unread_only: bool = Query(default=False),
    limit: int = Query(default=50, ge=1, le=200),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user notifications."""
    service = NotificationService(db)
    data = await service.get_user_notifications(user.id, unread_only, limit)
    unread_count = await service.get_unread_count(user.id)
    return success_response(data={"notifications": data, "unread_count": unread_count})


@router.put("/{notification_id}/read")
async def mark_read(
    notification_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a notification as read."""
    service = NotificationService(db)
    await service.mark_read(user.id, notification_id)
    return success_response(message="Notification marked as read")


@router.put("/read-all")
async def mark_all_read(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark all notifications as read."""
    service = NotificationService(db)
    count = await service.mark_all_read(user.id)
    return success_response(data={"marked_count": count}, message="All notifications marked as read")
