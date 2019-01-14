import sys
from enum import Enum


class ByteOrder(Enum):
    """
    Enumeration of byte orders.
    """
    # Represents a little endian byte order.
    LITTLE = 1

    # Represents a big endian byte order.
    BIG = 2

    # Represents the native byte order of the system running the code.
    NATIVE = LITTLE if sys.byteorder == "little" else BIG
