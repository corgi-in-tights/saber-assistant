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

class SaberIntentTemplate:
    def __init__(self, name: str, slot_templates: dict, skill: SaberSkill = None):
        self.name = name
        self.slot_templates = slot_templates
        self.skill = skill

    def to_intent(self, confidence: float = 1.0) -> SaberIntent:
        """
        Convert this template into a SaberIntent with the given confidence.
        """
        return SaberIntent(
            name=self.name,
            confidence=confidence,
            skill=self.skill,
            slots=self.slot_templates,
        )
