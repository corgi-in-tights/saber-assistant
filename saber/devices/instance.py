from saber.devices.device_manager import SaberDeviceManager


def get_device_manager() -> SaberDeviceManager:
    """
    Get the instance of the SaberDeviceManager.
    This function is used to access the device manager for interacting with devices.
    """
    return SaberDeviceManager()
