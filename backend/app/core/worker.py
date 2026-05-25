from celery import Celery

from .config import settings

celery_client = Celery(broker=settings.RABBITMQ_URI)
