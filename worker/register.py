import mlflow
from settings import settings
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def reg_model():
    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

    model = AutoModelForSequenceClassification.from_pretrained("fklska/bert-imdb")
    tokenizer = AutoTokenizer.from_pretrained("fklska/bert-imdb")

    transformers_model = {"model": model, "tokenizer": tokenizer}

    transformers_model["model"].config.id2label = {0: "NEGATIVE", 1: "POSTIVE"}
    transformers_model["model"].config.label2id = {"NEGATIVE": 0, "POSTIVE": 1}

    with mlflow.start_run():
        mlflow.transformers.log_model(
            transformers_model=transformers_model,
            name="bert-classifier",
            task="text-classification",
            registered_model_name="bert-imdb",
        )


reg_model()
