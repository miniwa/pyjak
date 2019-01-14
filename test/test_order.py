import sys
from bink.order import ByteOrder


class TestByteOrder:
    def test_native(self):
        if sys.byteorder == "little":
            assert ByteOrder.NATIVE == ByteOrder.LITTLE
            assert ByteOrder.NATIVE != ByteOrder.BIG
        else:
            assert ByteOrder.NATIVE != ByteOrder.LITTLE
            assert ByteOrder.NATIVE == ByteOrder.BIG
