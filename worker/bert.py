import torch
from main import classifier, tokenizer


def classify(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = classifier(**inputs)

    logits = outputs.logits
    predicted_class_id = logits.argmax().item()
    probs = torch.softmax(logits, dim=-1)

    return {"label": predicted_class_id, "probs": probs}
