from celery import Celery
from transformers import AutoModelForSequenceClassification, AutoTokenizer

classifier = AutoModelForSequenceClassification.from_pretrained("./models/")
tokenizer = AutoTokenizer.from_pretrained("./models/")

celery_app = Celery("worker", broker="amqp://guest:guest@localhost:5672//", include=["tasks"])
celery_app.conf.update(task_track_started=True, task_serializer="json")
