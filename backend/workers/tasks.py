"""
Celery background tasks for the AI Fitness Ecosystem.
"""

import asyncio
from datetime import date, timedelta
from loguru import logger

from workers.celery_app import celery_app


def run_async(coro):
    """Run async coroutine in sync Celery task context."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="workers.tasks.generate_daily_summaries")
def generate_daily_summaries():
    """Generate daily fitness summaries for all active users."""
    async def _run():
        from app.db.base import async_session_factory
        from sqlalchemy import select
        from app.models.user import User
        from app.services.notification_service import NotificationService

        async with async_session_factory() as db:
            result = await db.execute(
                select(User).where(User.is_active == True)
            )
            users = result.scalars().all()
            notif_service = NotificationService(db)

            for user in users:
                try:
                    await notif_service.create(
                        user_id=user.id,
                        title="Daily Summary 📊",
                        message="Your daily fitness summary is ready! Check your dashboard.",
                        notification_type="daily_summary",
                    )
                except Exception as e:
                    logger.error(f"Failed to create summary for user {user.id}: {e}")

            await db.commit()
            logger.info(f"Generated daily summaries for {len(users)} users")

    run_async(_run())


@celery_app.task(name="workers.tasks.check_all_achievements")
def check_all_achievements():
    """Check and award achievements for all users."""
    async def _run():
        from app.db.base import async_session_factory
        from sqlalchemy import select
        from app.models.user import User
        from app.models.fitness import StepsDaily
        from app.services.goal_service import AchievementService
        from sqlalchemy import func

        async with async_session_factory() as db:
            result = await db.execute(
                select(User).where(User.is_active == True)
            )
            users = result.scalars().all()
            ach_service = AchievementService(db)
            total_awarded = 0

            for user in users:
                try:
                    # Check step achievements based on max daily steps
                    step_result = await db.execute(
                        select(func.max(StepsDaily.total_steps))
                        .where(StepsDaily.user_id == user.id)
                    )
                    max_steps = step_result.scalar() or 0
                    newly_earned = await ach_service.check_and_award(user.id, "steps", max_steps)
                    total_awarded += len(newly_earned)
                except Exception as e:
                    logger.error(f"Achievement check failed for user {user.id}: {e}")

            await db.commit()
            logger.info(f"Achievement check complete: {total_awarded} new awards")

    run_async(_run())


@celery_app.task(name="workers.tasks.send_morning_reminders")
def send_morning_reminders():
    """Send morning workout and step reminders."""
    async def _run():
        from app.db.base import async_session_factory
        from sqlalchemy import select
        from app.models.user import User
        from app.services.notification_service import NotificationService

        async with async_session_factory() as db:
            result = await db.execute(
                select(User).where(User.is_active == True)
            )
            users = result.scalars().all()
            notif_service = NotificationService(db)

            for user in users:
                try:
                    await notif_service.create(
                        user_id=user.id,
                        title="Good Morning! ☀️",
                        message="Time to start your day strong! Check your workout plan.",
                        notification_type="reminder",
                    )
                except Exception as e:
                    logger.error(f"Reminder failed for user {user.id}: {e}")

            await db.commit()
            logger.info(f"Sent morning reminders to {len(users)} users")

    run_async(_run())


@celery_app.task(name="workers.tasks.cleanup_old_notifications")
def cleanup_old_notifications():
    """Delete read notifications older than 30 days."""
    async def _run():
        from app.db.base import async_session_factory
        from sqlalchemy import delete
        from app.models.social import Notification

        cutoff = date.today() - timedelta(days=30)

        async with async_session_factory() as db:
            result = await db.execute(
                delete(Notification).where(
                    Notification.is_read == True,
                    Notification.created_at < cutoff,
                )
            )
            await db.commit()
            logger.info(f"Cleaned up {result.rowcount} old notifications")

    run_async(_run())
