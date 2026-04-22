from bert import classify
from core.db import update_review_label
from main import celery_app


@celery_app.task(name="inference")
def run_inference(review_id: int, data: dict):
    text = data.get("description", "")

    result = classify(text)

    update_review_label(review_id, result["label"])
    return result["label"]
