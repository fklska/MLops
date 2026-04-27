from core.db import update_review_label
from main import celery_app

from worker.core.bert import classify
from worker.prometheus.metrics import PREDICTION_COUNTER


@celery_app.task(name="inference")
def run_inference(review_id: int, data: dict):
    text = data.get("description", "")

    result = classify(text)
    PREDICTION_COUNTER.labels(label=result["label"]).inc()

    update_review_label(review_id, result["label"])
    return result["label"]
