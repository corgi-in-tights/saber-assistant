from typing import Any


class SaberDeviceManager:
    """
    A smart assistant-friendly abstraction for interacting with Home Assistant devices.
    Supports querying devices, entities, states, and issuing service calls.
    """

    def __init__(self, config: dict[str, Any]):
        """
        Initialize DeviceManager with connection info, tokens, etc.
        """
        self.base_url = config.get("base_url")
        self.auth_token = config.get("auth_token")
        self.headers = {"Authorization": f"Bearer {self.auth_token}", "Content-Type": "application/json"}

    # ───────────────────────────────
    # 🔍 DEVICE/ENTITY ENUMERATION
    # ───────────────────────────────

    def get_all_entities(self) -> list[dict[str, Any]]:
        """Return metadata for all entities registered in Home Assistant."""
        raise NotImplementedError

    def get_entities_by_domain(self, domain: str) -> list[dict[str, Any]]:
        """Filter entities by type/domain (e.g., 'light', 'sensor', 'switch')."""
        raise NotImplementedError

    def get_devices(self) -> list[dict[str, Any]]:
        """Return a list of devices (requires WebSocket API)."""
        raise NotImplementedError

    def get_device_entities(self, device_id: str) -> list[dict[str, Any]]:
        """Return all entities attached to a given device."""
        raise NotImplementedError

    # ───────────────────────────────
    # 📊 ENTITY STATES AND ATTRIBUTES
    # ───────────────────────────────

    def get_entity_state(self, entity_id: str) -> dict[str, Any] | None:
        """Get current state and attributes of an entity (light, sensor, etc.)."""
        raise NotImplementedError

    def get_all_entity_states(self) -> list[dict[str, Any]]:
        """Get current states for all entities."""
        raise NotImplementedError

    def is_entity_on(self, entity_id: str) -> bool:
        """Check if a given entity (light, switch, etc.) is on."""
        raise NotImplementedError

    def get_entity_attributes(self, entity_id: str) -> dict[str, Any]:
        """Return just the attributes dict from an entity."""
        raise NotImplementedError

    def get_device_class(self, entity_id: str) -> str | None:
        """Return device class (e.g., 'motion', 'battery') for a sensor."""
        raise NotImplementedError

    def get_device_by_name(self, name: str) -> dict[str, Any] | None:
        """
        Get device metadata by user-friendly name.
        E.g., "kitchen light" → {"id": "light.kitchen", "name": "Kitchen Light", ...}
        """
        raise NotImplementedError

    # ───────────────────────────────
    # ⚙️ ENTITY CONTROL / SERVICE CALLS
    # ───────────────────────────────

    def call_service(self, domain: str, service: str, entity_id: str, data: dict[str, Any] | None = None) -> bool:
        """
        Call a Home Assistant service (e.g. 'light.turn_on').
        """
        raise NotImplementedError

    def set_attribute(self, entity_id: str, domain: str, attr_data: dict[str, Any]) -> bool:
        """Set custom attributes on a device (e.g., brightness, color)."""
        raise NotImplementedError

    # ───────────────────────────────
    # 🧠 SMART RESOLUTION
    # ───────────────────────────────

    def resolve_friendly_name(self, name: str) -> str | None:
        """
        Convert user-friendly name to entity_id using fuzzy or alias matching.
        E.g., "kitchen light" → "light.kitchen"
        """
        raise NotImplementedError

    def resolve_my_devices(self, user_id: str, domain: str | None = None) -> list[str]:
        """
        Resolve what 'my lights' or 'my switches' means for a given user.
        E.g., map user_id → bedroom light entity
        """
        raise NotImplementedError

    def get_user_default_room(self, user_id: str) -> str | None:
        """
        Get a default room (e.g., 'bedroom') for a user from stored preferences.
        """
        raise NotImplementedError
