import csv
import math
import os

from core.bert import classify
from core.db import LABEL_2_ID, update_review_label
from main import celery_app, tokenizer
from metrics import (
    INFERENCE_TIME,
    LOW_CONFIDENCE_TOTAL,
    PREDICTION_CONFIDENCE,
    PREDICTION_CONFIDENCE_SUMMARY,
    PREDICTION_COUNTER,
    PREDICTION_ENTROPY,
    REVIEW_TEXT_LENGTH,
    TOKEN_COUNT,
)

log_file = "/app/logs/current_production.csv"
file_exists = os.path.isfile(log_file)
os.makedirs(os.path.dirname(log_file), exist_ok=True)


@celery_app.task(name="inference")
@INFERENCE_TIME.time()
def run_inference(review_id: int, data: dict):
    text = data.get("description", "")

    result = classify(text)
    label = result["label"]
    prob = result["probability"]
    all_probs = result["probabilities"]

    REVIEW_TEXT_LENGTH.observe(len(text))
    encoded = tokenizer(text, add_special_tokens=True, return_attention_mask=False)
    TOKEN_COUNT.observe(len(encoded["input_ids"]))

    PREDICTION_CONFIDENCE.observe(prob)
    PREDICTION_CONFIDENCE_SUMMARY.observe(prob)

    entropy = -sum(p * math.log(p) for p in all_probs.values() if p > 0)
    PREDICTION_ENTROPY.observe(entropy)

    if prob < 0.6:
        LOW_CONFIDENCE_TOTAL.inc()

    PREDICTION_COUNTER.labels(label=label).inc()
    update_review_label(review_id, label, prob)

    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["text", "target"])
        writer.writerow([text, LABEL_2_ID[label]])

    return label
