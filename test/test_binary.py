import struct
import sys
import pytest
from bink import (Endian, parse_int32, parse_uint32, dump_int32,
dump_uint32, BinaryStream, BinaryReader, BinaryWriter)


_int = -255
_int_bytes = struct.pack("=i", _int)
_int_bytes_little = struct.pack("<i", _int)
_int_bytes_big = struct.pack(">i", _int)


_uint = 255
_uint_bytes = struct.pack("=I", _uint)
_uint_bytes_little = struct.pack("<I", _uint)
_uint_bytes_big = struct.pack(">I", _uint)


class TestEndian:
    def test_native(self):
        if sys.byteorder == "little":
            assert Endian.native() == Endian.LITTLE
        else:
            assert Endian.native() == Endian.BIG


class TestParse:
    def test_parse_int32(self):
        assert parse_int32(_int_bytes) == _int

    def test_parse_int32_little(self):
        assert parse_int32(_int_bytes_little, Endian.LITTLE) == _int

    def test_parse_int32_big(self):
        assert parse_int32(_int_bytes_big, Endian.BIG) == _int

    def test_parse_uint32(self):
        assert parse_uint32(_uint_bytes) == _uint

    def test_parse_uint32_little(self):
        assert parse_uint32(_uint_bytes_little, Endian.LITTLE) == _uint

    def test_parse_uint32_big(self):
        assert parse_uint32(_uint_bytes_big, Endian.BIG) == _uint


class TestDump:
    def test_dump_int32(self):
        assert dump_int32(_int) == _int_bytes

    def test_dump_int32_little(self):
        assert dump_int32(_int, Endian.LITTLE) == _int_bytes_little

    def test_dump_int32_big(self):
        assert dump_int32(_int, Endian.BIG) == _int_bytes_big

    def test_dump_uint32(self):
        assert dump_uint32(_uint) == _uint_bytes

    def test_dump_uint32_little(self):
        assert dump_uint32(_uint, Endian.LITTLE) == _uint_bytes_little

    def test_dump_uint32_big(self):
        assert dump_uint32(_uint, Endian.BIG) == _uint_bytes_big


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
        reader = BinaryReader(_int_bytes_little)
        assert reader.read_int32(Endian.LITTLE) == _int
        assert reader.pos() == 4

    def test_read_int32_big(self):
        reader = BinaryReader(_int_bytes_big)
        assert reader.read_int32(Endian.BIG) == _int
        assert reader.pos() == 4

    def test_read_uint32(self):
        reader = BinaryReader(_uint_bytes)
        assert reader.read_uint32() == _uint
        assert reader.pos() == 4

    def test_read_uint32_little(self):
        reader = BinaryReader(_uint_bytes_little)
        assert reader.read_uint32(Endian.LITTLE) == _uint
        assert reader.pos() == 4

    def test_read_uint32_big(self):
        reader = BinaryReader(_uint_bytes_big)
        assert reader.read_uint32(Endian.BIG) == _uint
        assert reader.pos() == 4

    def test_read_string(self):
        reader = BinaryReader(b"Hello")
        assert reader.read_string(5) == "Hello"


class TestBinaryWriter:
    def setup_method(self):
        self.writer = BinaryWriter(Endian.native())
        self.little_writer = BinaryWriter(Endian.LITTLE)
        self.big_writer = BinaryWriter(Endian.BIG)

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

    def test_write_string(self):
        self.writer.write_string("Hello")
        assert self.writer.to_bytes() == b"Hello"

    def test_write_string_uint32(self):
        self.writer.write_string_uint32("Hello")
        reader = BinaryReader(self.writer.to_bytes())
        assert reader.read_prefixed_string_uint32() == "Hello"
