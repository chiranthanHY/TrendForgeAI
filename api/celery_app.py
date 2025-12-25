"""
Celery configuration for TrendForgeAI
Handles async background tasks like content generation
"""

from celery import Celery
from celery.result import AsyncResult
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create Celery app
celery_app = Celery(
    "trendforge",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max per task
    task_soft_time_limit=240,  # 4 minutes soft limit
)

# Import tasks
from api.tasks import content_tasks

# Auto-discover tasks
celery_app.autodiscover_tasks(['api.tasks'])

if __name__ == '__main__':
    celery_app.start()
