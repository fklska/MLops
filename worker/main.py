import mlflow
from celery import Celery
from settings import settings
from transformers import AutoModelForSequenceClassification, AutoTokenizer

celery_app = Celery("worker", broker=settings.RABBIT_MQ_URL, include=["tasks"])
mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)


def load_model():
    model_name = "bert-imdb-classifier"
    model_uri = f"models:/{model_name}/Production"

    print(f"Загрузка модели {model_uri}...")
    model = mlflow.pytorch.load_model(model_uri)
    return model


classifier = AutoModelForSequenceClassification.from_pretrained("./models/")
tokenizer = AutoTokenizer.from_pretrained("./models/")

celery_app = Celery("worker", broker="amqp://guest:guest@localhost:5672//", include=["tasks"])
celery_app.conf.update(task_track_started=True, task_serializer="json")
