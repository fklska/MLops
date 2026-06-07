import mlflow
from celery import Celery
from settings import settings

celery_app = Celery("worker", broker=settings.RABBIT_MQ_URL, include=["tasks"])
celery_app.conf.update(task_track_started=True, task_serializer="json")

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

classifier = mlflow.transformers.load_model(settings.MLFLOW_MODEL_URL)
