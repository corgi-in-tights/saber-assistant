from .base import SaberClassifier


class RegexClassifier(SaberClassifier):
    """
    Classifier that uses regular expressions to match intents.
    This is a simple classifier that can be used for basic intent recognition.
    """

    async def classify(self, sentence: str, contexts: dict) -> list[dict]:
        """
        Classify the given sentence using regex patterns.
        Returns a list of matched intents with confidence scores.
        """
        # Placeholder implementation
        return [{"intent": "regex_matched", "confidence": 0.8, "sentence": sentence}]
