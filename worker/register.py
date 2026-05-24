import mlflow
from settings import settings
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def reg_model():
    mlflow.set_tracking_uri(settings.MLFLOW_REGISTER_URI)

    model = AutoModelForSequenceClassification.from_pretrained("fklska/bert-imdb")
    tokenizer = AutoTokenizer.from_pretrained("fklska/bert-imdb")

    transformers_model = {"model": model, "tokenizer": tokenizer}

    transformers_model["model"].config.id2label = {0: "NEGATIVE", 1: "POSTIVE"}
    transformers_model["model"].config.label2id = {"NEGATIVE": 0, "POSTIVE": 1}

    with mlflow.start_run():
        model_info = mlflow.transformers.log_model(
            transformers_model=transformers_model,
            name="bert-classifier",
            task="text-classification",
            registered_model_name="bert-imdb",
        )

    model_version = model_info.registered_model_version

    client = mlflow.MlflowClient()
    client.set_registered_model_alias(name="bert-imdb", alias="prod", version=str(model_version))


reg_model()
