from core.bert import classify
from core.db import update_review_label
from main import celery_app
from metrics import INFERENCE_TIME, PREDICTION_COUNTER


@celery_app.task(name="inference")
@INFERENCE_TIME.time()
def run_inference(review_id: int, data: dict):
    text = data.get("description", "")

    label, prob = classify(text).values()
    PREDICTION_COUNTER.labels(label=label).inc()
    update_review_label(review_id, label, prob)
    return label
