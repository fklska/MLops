from main import classifier


def classify(text: str):
    result = classifier(text)
    print(result)
    return result[0]
