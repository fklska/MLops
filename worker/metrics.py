from prometheus_client import Counter, Histogram, Summary, start_http_server

start_http_server(8088)


INFERENCE_TIME = Histogram(
    "bert_inference_seconds", "Time spent on inference", buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
)

PREDICTION_COUNTER = Counter("bert_predictions_total", "Total predictions per class", ["label"])

REVIEW_TEXT_LENGTH = Histogram(
    "review_text_length_chars", "Length of input review text in characters", buckets=(20, 50, 100, 200, 500, 1000, 2000)
)

TOKEN_COUNT = Histogram(
    "review_token_count", "Number of tokens after BERT tokenization", buckets=(10, 20, 30, 50, 100, 200, 500)
)

PREDICTION_CONFIDENCE = Histogram(
    "prediction_confidence",
    "Maximum predicted probability",
    buckets=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99),
)

PREDICTION_CONFIDENCE_SUMMARY = Summary("prediction_confidence_summary", "Summary of max probability")

PREDICTION_ENTROPY = Histogram(
    "prediction_entropy",
    "Entropy of predicted probability distribution",
    buckets=(0.01, 0.1, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0),
)

LOW_CONFIDENCE_TOTAL = Counter("low_confidence_predictions_total", "Predictions where max probability < threshold")
