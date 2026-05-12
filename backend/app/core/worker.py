from celery import Celery

celery_client = Celery(broker="amqp://guest:guest@rabbitmq:5672//")
