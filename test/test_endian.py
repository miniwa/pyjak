import sys
from bink.endian import Endian


class TestEndian:
    def test_native(self):
        if sys.byteorder == "little":
            assert Endian.NATIVE == Endian.LITTLE
        else:
            assert Endian.NATIVE == Endian.BIG
