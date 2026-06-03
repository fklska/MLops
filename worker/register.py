import mlflow
from core.db import ID_2_LABEL, LABEL_2_ID

# from settings import settings
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def reg_model():
    mlflow.set_tracking_uri("http://127.0.0.1:42804")

    model = AutoModelForSequenceClassification.from_pretrained("fklska/bert-imdb")
    tokenizer = AutoTokenizer.from_pretrained("fklska/bert-imdb")

    transformers_model = {"model": model, "tokenizer": tokenizer}

    transformers_model["model"].config.id2label = ID_2_LABEL
    transformers_model["model"].config.label2id = LABEL_2_ID

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


def debug():
    client = mlflow.MlflowClient()
    exp = client.get_experiment_by_name("Default")
    print(exp)


reg_model()
# debug()
