class Device:
    def __init__(self, entity_id: str, name: str, device_type: str, location: str):
        self.entity_id = entity_id
        self.name = name
        self.state = False  # Default state is False (off)
        self.device_type = device_type
        self.location = location
        self.device_attributes = {}

        self.linked_devices = []  # really just imagining like, a hub connected to an independant speaker
        self.intergrations = []  # in-built speaker?

    def __repr__(self):
        return f"Device(entity_id={self.entity_id}, type={self.device_type}, state={self.state})"

    def to_dict(self):
        return {
            "name": self.name,
            "device_type": self.device_type,
            "location": self.location,
            "state": self.state,
            "device_attributes": self.device_attributes,
        }

    def get_device_attribute(self, attr_name: str) -> any | None:
        """
        Get the value of a specific attribute.

        :param attr_name: The name of the attribute to retrieve.
        :return: The value of the attribute or None if it does not exist.
        """
        return self.attributes.get(attr_name, None)


    def get_device_attribute_or_error(self, attr_name: str) -> any:
        """
        Get the value of a specific attribute or raise an error if it does not exist.

        :param attr_name: The name of the attribute to retrieve.
        :raises AttributeDoesNotExist: If the attribute does not exist.
        :return: The value of the attribute.
        """
        if attr_name not in self.attributes:
            msg = f"Device attribute '{attr_name}' does not exist on device '{self.name}'."
            raise AttributeError(msg)
        return self.attributes[attr_name]


    def set_device_attributes(self, **kwargs):
        """
        Add attributes to the device.

        :param args: Attribute names to add.
        """
        for k, v in kwargs:
            self.device_attributes[k] = v


# some commonly used device types as classes for convenience
# hub device needs a lot more work
# need to do more research on the current home assistant likes to figure out how to handle intergrations
# like a speaker or a light intergration, etc.
class HubDevice(Device):
    def __init__(self, entity_id: str, name: str, location: str):
        super().__init__(entity_id, name, "hub", location)
        self.set_device_attributes(bound_users=[], volume=50)

    def __repr__(self):
        return f"HubDevice(entity_id={self.entity_id}, state={self.state})"


class LightDevice(Device):
    def __init__(self, entity_id: str, name: str, location: str):
        super().__init__(entity_id, name, "light", location)
        self.set_device_attributes(brightness=100, color="white")

    def __repr__(self):
        return f"LightDevice(entity_id={self.entity_id}, state={self.state})"


class AdjustableDevice(Device):
    def __init__(self, entity_id: str, name: str, location: str):
        super().__init__(entity_id, name, "adjustable", location)
        self.set_device_attributes(value=100, mode="default")

    def __repr__(self):
        return f"AdjustableDevice(entity_id={self.entity_id}, state={self.state})"

