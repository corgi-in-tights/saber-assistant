import logging

from saber import SaberIntent

from .base import SaberClassifier

logger = logging.getLogger("saber")


class CategoryFilteredExternalClassifier(SaberClassifier):
    """
    Classifier that uses an external service to classify intents.
    This classifier sends the sentence to an external URL and expects a JSON response.
    """
    async def _get_intent_names(self, item: dict) -> list[str]:
        return []

    async def _get_intent_data(self, item: dict, templates: list) -> list[str]:
        return [{"name": "intent_name", "slots": {"slot_name": "value"}}]

    async def classify(self, item: dict, contexts: dict) -> list[dict]:
        # self.open_session

        intent_names = await self._get_intent_names(item)

        # fetch intent template by name
        templates = []
        for name in intent_names:
            # append template
            logger.debug("intent: %s", name)

        intents_data = await self._get_intent_data(item, templates)

        # convert templates into SaberIntent objects
        return [
            SaberIntent(
                name=d["name"],
                slots=d["slots"],
                skill=d.get("skill", None),
                confidence=0.8,
            )
            for d in intents_data
        ]
