from celery import Celery

celery_client = Celery(broker="amqp://guest:guest@localhost:5672//")
