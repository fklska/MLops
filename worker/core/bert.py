from main import classifier


def classify(text: str):
    raw_results = classifier(text)
    scores = {r["label"]: r["score"] for r in raw_results}
    max_label = max(scores, key=scores.get)
    return {
        "label": max_label,
        "probability": scores[max_label],
        "probabilities": scores,
    }
