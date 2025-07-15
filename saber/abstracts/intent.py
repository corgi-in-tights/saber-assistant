from .skill import SaberSkill


class SaberIntent:
    def __init__(self, name: str, confidence: float, skill: SaberSkill, slots: dict):
        self.name = name
        self.confidence = confidence
        self.skill = skill
        self.slots = slots

    async def convert_slot_types(self):
        pass

    async def run_skill(self, *args, **kwargs):
        """
        Run the skill associated with this intent.
        This method calls the execute method of the skill.
        """
        if not self.skill:
            return None

        return await self.skill.execute(
            *args,
            name=self.name,
            slots=self.slots,
            **kwargs,
        )
