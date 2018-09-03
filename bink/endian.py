import sys
from enum import Enum


class Endian(Enum):
    LITTLE = 1
    BIG = 2
    NATIVE = LITTLE if sys.byteorder == "little" else BIG
