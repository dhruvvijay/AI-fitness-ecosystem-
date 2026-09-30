"""
Celery worker application for background tasks.
Handles: daily summaries, achievement checks, notifications, analytics.
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "fitness_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max per task
    task_soft_time_limit=240,
    worker_max_tasks_per_child=100,
    worker_prefetch_multiplier=1,
)

# Periodic tasks schedule
celery_app.conf.beat_schedule = {
    "daily-summary-midnight": {
        "task": "workers.tasks.generate_daily_summaries",
        "schedule": crontab(hour=0, minute=5),  # 12:05 AM
    },
    "check-achievements-hourly": {
        "task": "workers.tasks.check_all_achievements",
        "schedule": crontab(minute=30),  # Every hour at :30
    },
    "send-reminders-morning": {
        "task": "workers.tasks.send_morning_reminders",
        "schedule": crontab(hour=7, minute=0),  # 7:00 AM
    },
    "cleanup-old-notifications": {
        "task": "workers.tasks.cleanup_old_notifications",
        "schedule": crontab(hour=3, minute=0, day_of_week=0),  # Sunday 3 AM
    },
}
