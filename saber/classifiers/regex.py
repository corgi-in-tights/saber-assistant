from saber.utils import load_json_file

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


def basic_sentence_reformatter(sentence: str) -> str:
    """
    A basic sentence reformatter that can be used to preprocess sentences.
    """
    return sentence.strip().lower()


class DepthRegexClassifier(RegexClassifier):
    """
    Classifier that uses regular expressions with depth control.
    This classifier can handle more complex regex patterns and contexts.
    """
    def __init__(self, depth_provider: str, depths: list[list[str]], **kwargs):
        super().__init__()
        self.depth_provider = load_json_file(depth_provider)
        self.depths = depths
        self.default_depth = kwargs.get("default_depth", 0)
        self.sentence_reformatter = kwargs.get("sentence_reformatter", basic_sentence_reformatter)

    async def classify(
        self,
        sentence: str,
        contexts: dict,
    ) -> list[dict]:

        # Implement depth-based classification logic here
        return await super().classify(sentence, contexts)
