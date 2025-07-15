class SaberSkill:
    """
    Base class for Saber skills.
    Skills should inherit from this class and implement the `execute` method.
    """

    async def execute(self, name, slots, **kwargs):
        """
        Execute the skill logic.
        This method should be overridden by subclasses.
        """
        msg = "Subclasses must implement the execute method."
        raise NotImplementedError(msg)
