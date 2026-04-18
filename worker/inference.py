from main import celery_app


@celery_app.task(name="inference")
def run_inference(review_id: int, data: dict):
    text = data.get("text", "")
    print(review_id, data)

    is_positive = "bad" not in text.lower()
    sentiment = "positive" if is_positive else "negative"
    return sentiment
