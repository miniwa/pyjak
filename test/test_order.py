import sys
from pyjak import ByteOrder


class TestByteOrder:
    def test_native(self):
        if sys.byteorder == "little":
            assert ByteOrder.NATIVE == ByteOrder.LITTLE
            assert ByteOrder.NATIVE != ByteOrder.BIG
        else:
            assert ByteOrder.NATIVE != ByteOrder.LITTLE
            assert ByteOrder.NATIVE == ByteOrder.BIG
