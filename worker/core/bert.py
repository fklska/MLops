from main import classifier


def classify(text: str):
    result = classifier(text)
    return result[0]
