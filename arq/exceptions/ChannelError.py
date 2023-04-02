import string
import enum

class ChannelErrorCodes(enum.Enum):
    CHANNEL_IS_BUSY = 0

class ChannelError(Exception):
    """
    Klasa wyjątków związanych z wektorami bitowymi.
    """

    def __init__(self, message: string, code: ChannelErrorCodes):
        super().__init__(message)
        self.code = code
