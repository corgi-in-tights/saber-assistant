from .device import Device

# needs more work

class DeviceGroup:
    """
    Represents a group of devices that can be controlled together.
    """

    def __init__(self, group_id: str, name: str, devices: list[Device]):
        self.group_id = group_id
        self.name = name
        self.devices = devices


    def add_device(self, device: Device):
        """
        Adds a device to the group.

        :param device: The device to add.
        """
        self.devices.append(device)


    def remove_device(self, device: Device) -> bool | None:
        """
        Removes a device from the group. Return if the device was removed.

        :param device: The device to remove.
        """
        if device in self.devices:
            self.devices.remove(device)
            return True
        return False

