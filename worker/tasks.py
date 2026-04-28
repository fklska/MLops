from core.bert import classify
from core.db import update_review_label
from main import celery_app


@celery_app.task(name="inference")
def run_inference(review_id: int, data: dict):
    text = data.get("description", "")

    result = classify(text)
    # PREDICTION_COUNTER.labels(label=result["label"]).inc()

    update_review_label(review_id, 0 if result["label"] == "LABEL_0" else 1)
    return result["label"]
