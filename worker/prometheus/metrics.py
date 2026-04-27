from prometheus_client import Counter, Histogram

INFERENCE_TIME = Histogram("bert_inference_seconds", "Time spent processing text by BERT")

PREDICTION_COUNTER = Counter("bert_predictions_total", "Total predictions by class", ["label"])
