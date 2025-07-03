class SaberClassifier:
    """
    Base class for all Saber classifiers.
    This class provides a common interface for all classifiers in the Saber framework.
    """

    def classify(self, sentence: str, contexts: dict) -> list[dict]:
        msg = "This method should be overridden by subclasses."
        raise NotImplementedError(msg)
