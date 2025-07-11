from .base import SaberClassifier


class CategoryFilteredExternalClassifier(SaberClassifier):
    """
    Classifier that uses an external service to classify intents.
    This classifier sends the sentence to an external URL and expects a JSON response.
    """

    async def classify(self, sentence: str, contexts: dict) -> list[dict]:
        # Placeholder implementation
        return [{"intent": "regex_matched", "confidence": 0.8, "sentence": sentence}]
