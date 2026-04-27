import mlflow
import mlflow.pytorch
from settings import settings
from transformers import AutoModelForSequenceClassification

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

model = AutoModelForSequenceClassification.from_pretrained("models/")


with mlflow.start_run():
    mlflow.pytorch.log_model(pytorch_model=model, artifact_path="bert-classifier", registered_model_name="bert-imdb")
