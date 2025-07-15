class SaberClassifier:
    """
    Base class for all Saber classifiers.
    This class provides a common interface for all classifiers in the Saber framework.
    """

    async def get_assumed_confidence(
        self,
        item: dict,
    ) -> float:
        """
        Get the confidence score for a given sentence.
        This method should be overridden by subclasses to provide specific classification logic.
        :param sentence: The input sentence to classify.
        :return: A confidence score between 0 and 1.
        """
        return 0.8

    async def assemble_context(self, item: dict, category_contexts: dict, global_contexts: dict) -> float:
        return {**global_contexts, **category_contexts}

    async def classify(self, item: dict, contexts: dict) -> list[dict]:
        msg = "This method should be overridden by subclasses."
        raise NotImplementedError(msg)
