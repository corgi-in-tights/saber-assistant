class SaberResponse:
    """
    Base class for Saber responses.
    Responses should inherit from this class and implement the `send` method.
    """

    def __init__(self, response_type, value):
        self.response_type = response_type
        self.value = value
        self.additional_data = {}

    def send(self):
        """
        Send the response.
        This method should be overridden by subclasses to implement actual sending logic.
        """
        msg = "Subclasses must implement the send method."
        raise NotImplementedError(msg)

    def to_dict(self):
        return {
            "response_type": self.response_type,
            "value": self.value,
            "additional_data": self.additional_data,
        }

def create_defer_response(message: str):
    """
    Create a defer response.
    """
    return SaberResponse("defer", message)

def create_message_response(message: str):
    """
    Create a message response.
    """
    return SaberResponse("message", message)

def create_buzzer_response():
    """
    Create an update response.
    """
    return SaberResponse("nonverbal", "buzzer")

