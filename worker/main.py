from celery import Celery

celery_app = Celery("worker", broker="amqp://guest:guest@localhost:5672//", include=["inference"])

celery_app.conf.update(task_track_started=True, task_serializer="json")
