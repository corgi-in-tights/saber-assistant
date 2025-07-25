class SaberContextProvider:
    """
    Context provider for Saber logic.
    This class is responsible for providing context to the Saber logic layer.
    """

    async def get_context(self, contexts: dict, input_data: dict, intent_template: dict):
        """
        Get the context for the Saber logic layer.
        This method should be overridden by subclasses to provide specific context.
        """
        msg = "Subclasses must implement this method."
        raise NotImplementedError(msg)
