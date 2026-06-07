import os

import boto3
import mlflow
from core.db import ID_2_LABEL, LABEL_2_ID
from settings import settings
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def check_or_create_bucket():
    s3_client = boto3.client(
        "s3",
        endpoint_url=settings.MLFLOW_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    try:
        s3_client.create_bucket(Bucket="mlops")
        print("Bucket mlops created successfully!")
    except Exception as e:
        print(f"Error creating bucket: {e}")


def reg_model():
    check_or_create_bucket()

    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

    model = AutoModelForSequenceClassification.from_pretrained("fklska/bert-imdb", cache_dir="model/")
    tokenizer = AutoTokenizer.from_pretrained("fklska/bert-imdb", cache_dir="model/")

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

    os.removedirs("model/")


def debug():
    client = mlflow.MlflowClient()
    exp = client.get_experiment_by_name("Default")
    print(exp)


reg_model()
# debug()
