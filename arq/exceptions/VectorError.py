import string
import enum

import numpy


class VectorErrorCodes(enum.Enum):
    EMPTY = 0
    NON_BINARY = 1


class VectorError(Exception):
    """
    Klasa wyjątków związanych z wektorami bitowymi.
    """

    def __init__(self, message: string, code: VectorErrorCodes):
        super().__init__(message)
        self.code = code
