import string
import enum

class MemoryErrorCodes(enum.Enum):
    OCCUPIED = 0
    ELEMENT_NOT_EXIST = 1

class MemoryError(Exception):
    """
    Klasa wyjątków związanych z wektorami bitowymi.
    """

    def __init__(self, message: string, code: MemoryErrorCodes):
        super().__init__(message)
        self.code = code
