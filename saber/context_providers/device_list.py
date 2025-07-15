from saber import SaberContextProvider
from saber.devices import get_device_manager


class DeviceListContextProvider(SaberContextProvider):
    """
    Context provider for device list management.
    This class is responsible for providing context related to device lists in the Saber logic layer.
    """

    async def get_context(self, input_data: dict, intent_template: dict):
        """
        Get the context for device list management.
        This method should be overridden by subclasses to provide specific context.
        """
        # devices = await get_device_manager().get_devices()
        # device_list = [
        #     {
        #         "id": device["id"],
        #         "name": device["name"],
        #         "model": device.get("model", "Unknown"),
        #         "manufacturer": device.get("manufacturer", "Unknown"),
        #         "entities": await get_device_manager().get_device_entities(device["id"]),
        #     }
        #     for device in devices
        # ]
        return {
            "device_list": [],
        }

