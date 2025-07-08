from .base import SaberContextProvider


class IntentGroupContextProvider(SaberContextProvider):
    """
    Context provider for intent group management.
    This class is responsible for providing context related to intent groups in the Saber logic layer.
    """

    async def get_context(self, input_data: dict, intent_template: dict):
        """
        Get the context for device list management.
        This method should be overridden by subclasses to provide specific context.
        """

    async def get_prompt(self, context: dict):
        return f"Here is the list of devices available in your system. {context['device_list']}"
