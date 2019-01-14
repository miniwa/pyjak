import struct
import pytest
from bink.order import ByteOrder
from bink.stream import BinaryStream, BinaryReader, BinaryWriter


_int = -255
_int_bytes = struct.pack("=i", _int)
_int_bytes_little = struct.pack("<i", _int)
_int_bytes_big = struct.pack(">i", _int)


_uint = 255
_uint_bytes = struct.pack("=I", _uint)
_uint_bytes_little = struct.pack("<I", _uint)
_uint_bytes_big = struct.pack(">I", _uint)


class TestBinaryStream:
    def setup_method(self):
        self._stream = BinaryStream(bytes(10))

    def test_length(self):
        assert self._stream.length() == 10

    def test_pos(self):
        assert self._stream.pos() == 0

    def test_remaining(self):
        assert self._stream.remaining() == 10

    def test_seek(self):
        self._stream.seek(5)
        assert self._stream.pos() == 5
        assert self._stream.remaining() == 5

    def test_move(self):
        self._stream.move(2)
        assert self._stream.pos() == 2

        self._stream.move(-2)
        assert self._stream.pos() == 0

    def test_seek_throws_on_invalid_index(self):
        with pytest.raises(IndexError):
            self._stream.seek(-1)
        with pytest.raises(IndexError):
            self._stream.seek(11)


class TestBinaryReader:
    def setup_method(self):
        self._reader = BinaryReader(bytes(10))

    def test_read(self):
        _bytes = self._reader.read(4)
        assert len(_bytes) == 4
        assert self._reader.pos() == 4

    def test_read_returns_empty_bytes_if_reached_eof(self):
        self._reader.seek(10)
        _bytes = self._reader.read(1)
        assert len(_bytes) == 0
        assert self._reader.pos() == 10

    def test_read_int32(self):
        reader = BinaryReader(_int_bytes)
        assert reader.read_int32() == _int
        assert reader.pos() == 4

    def test_read_int32_little(self):
        reader = BinaryReader(_int_bytes_little, ByteOrder.LITTLE)
        assert reader.read_int32() == _int
        assert reader.pos() == 4

    def test_read_int32_big(self):
        reader = BinaryReader(_int_bytes_big, ByteOrder.BIG)
        assert reader.read_int32() == _int
        assert reader.pos() == 4

    def test_read_uint32(self):
        reader = BinaryReader(_uint_bytes)
        assert reader.read_uint32() == _uint
        assert reader.pos() == 4

    def test_read_uint32_little(self):
        reader = BinaryReader(_uint_bytes_little, ByteOrder.LITTLE)
        assert reader.read_uint32() == _uint
        assert reader.pos() == 4

    def test_read_uint32_big(self):
        reader = BinaryReader(_uint_bytes_big, ByteOrder.BIG)
        assert reader.read_uint32() == _uint
        assert reader.pos() == 4


class TestBinaryWriter:
    def setup_method(self):
        self.writer = BinaryWriter(ByteOrder.NATIVE)
        self.little_writer = BinaryWriter(ByteOrder.LITTLE)
        self.big_writer = BinaryWriter(ByteOrder.BIG)

    def test_write_bytes(self):
        self.writer.write_bytes(bytes(4))
        assert self.writer.length() == 4
        assert self.writer.pos() == 4

    def test_write_bytes_out_of_position(self):
        self.writer.write_bytes(bytes(10))
        assert self.writer.length() == 10
        assert self.writer.pos() == 10

        self.writer.seek(8)
        self.writer.write_bytes(bytes(4))
        assert self.writer.length() == 12
        assert self.writer.pos() == 12

    def test_clear(self):
        self.writer.write_bytes(bytes(10))
        self.writer.clear()
        assert self.writer.length() == 0
        assert self.writer.pos() == 0

    def test_write_int32(self):
        self.writer.write_int32(_int)
        assert self.writer.to_bytes() == _int_bytes

    def test_write_int32_little(self):
        self.little_writer.write_int32(_int)
        assert self.little_writer.to_bytes() == _int_bytes_little

    def test_write_int32_big(self):
        self.big_writer.write_int32(_int)
        assert self.big_writer.to_bytes() == _int_bytes_big

    def test_write_uint32(self):
        self.writer.write_uint32(_uint)
        assert self.writer.to_bytes() == _uint_bytes

    def test_write_uint32_little(self):
        self.little_writer.write_uint32(_uint)
        assert self.little_writer.to_bytes() == _uint_bytes_little

    def test_write_uint32_big(self):
        self.big_writer.write_uint32(_uint)
        assert self.big_writer.to_bytes() == _uint_bytes_big
