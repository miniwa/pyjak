import sys
import struct


class Endian:
    LITTLE = 1
    BIG = 2
    NATIVE = LITTLE if sys.byteorder == "little" else BIG


def parse_from_format(frmt, _bytes, endianess=None):
    if endianess is None:
        endianess = Endian.NATIVE
    endian_str = "<" if endianess == Endian.LITTLE else ">"
    combined_format = endian_str + frmt

    calced_size = struct.calcsize(combined_format)
    _len = len(_bytes)
    if struct.calcsize(combined_format) != len(_bytes):
        raise ValueError("Length of byte buffer was {0}, expected {1}."
            .format(_len, calced_size))
    return struct.unpack(combined_format, _bytes)[0]


def dump_from_format(frmt, value, endianess=None):
    if endianess is None:
        endianess = Endian.native()
    endian_str = "<" if endianess == Endian.LITTLE else ">"
    combined_format = endian_str + frmt
    return struct.pack(combined_format, value)


INT8_FORMAT = "b"
INT16_FORMAT = "h"
INT32_FORMAT = "i"
INT64_FORMAT = "q"

UINT8_FORMAT = "B"
UINT16_FORMAT = "H"
UINT32_FORMAT = "I"
UINT64_FORMAT = "Q"

FLOAT32_FORMAT = "f"
FLOAT64_FORMAT = "d"


def parse_int8(byte):
    return parse_from_format(INT8_FORMAT, byte)


def parse_int16(_bytes, endianness=None):
    return parse_from_format(INT16_FORMAT, _bytes, endianness)


def parse_int32(_bytes, endianness=None):
    return parse_from_format(INT32_FORMAT, _bytes, endianness)


def parse_int64(_bytes, endianness=None):
    return parse_from_format(INT64_FORMAT, _bytes, endianness)


def parse_uint8(byte):
    return parse_from_format(UINT8_FORMAT, byte)


def parse_uint16(_bytes, endianness=None):
    return parse_from_format(UINT16_FORMAT, _bytes, endianness)


def parse_uint32(_bytes, endianness=None):
    return parse_from_format(UINT32_FORMAT, _bytes, endianness)


def parse_uint64(_bytes, endianness=None):
    return parse_from_format(UINT64_FORMAT, _bytes, endianness)


def parse_float32(_bytes, endianness=None):
    return parse_from_format(FLOAT32_FORMAT, _bytes, endianness)


def parse_float64(_bytes, endianness=None):
    return parse_from_format(FLOAT64_FORMAT, _bytes, endianness)


def parse_bool(byte):
    return parse_uint8(byte) != 0


def dump_int8(value):
    return dump_from_format(INT8_FORMAT, value, None)


def dump_int16(value, endianness=None):
    return dump_from_format(INT16_FORMAT, value, endianness)


def dump_int32(value, endianness=None):
    return dump_from_format(INT32_FORMAT, value, endianness)


def dump_int64(value, endianness=None):
    return dump_from_format(INT64_FORMAT, value, endianness)


def dump_uint8(value):
    return dump_from_format(UINT8_FORMAT, value, None)


def dump_uint16(value, endianness=None):
    return dump_from_format(UINT16_FORMAT, value, endianness)


def dump_uint32(value, endianness=None):
    return dump_from_format(UINT32_FORMAT, value, endianness)


def dump_uint64(value, endianness=None):
    return dump_from_format(UINT64_FORMAT, value, endianness)


def dump_float32(value, endianness=None):
    return dump_from_format(FLOAT32_FORMAT, value, endianness)


def dump_float64(value, endianness=None):
    return dump_from_format(FLOAT64_FORMAT, value, endianness)


def dump_bool(value):
    return dump_uint8(int(value))


class BinaryStream:
    def __init__(self, _bytes):
        self._bytes = _bytes
        self._index = 0

    def length(self):
        return len(self._bytes)

    def pos(self):
        return self._index

    def remaining(self):
        return self.length() - self._index

    def seek(self, index):
        if index < 0 or index > self.length():
            raise IndexError("Index out of bounds.")
        self._index = index

    def move(self, offset):
        self.seek(self._index + offset)


class BinaryReader(BinaryStream):
    def __init__(self, _bytes):
        super().__init__(_bytes)

    def read(self, count):
        to_read = min(count, self.remaining())
        if to_read == 0:
            return bytes()
        else:
            _read = self._bytes[self.pos():self.pos() + to_read]
            self.move(to_read)
            return _read

    def strict_read(self, count):
        if self.remaining() < count:
            msg = "Attempted to read {0} bytes but only {1} are available."\
                .format(count, self.remaining())
            raise ValueError(msg)
        _read = self.read(count)
        _read_count = len(_read)
        if _read_count != count:
            msg = "Attempted to read {0} bytes but only {1} were read."\
                .format(count, _read_count)
            raise ValueError(msg)
        return _read

    def read_int8(self):
        return parse_int8(self.strict_read(1))

    def read_int16(self, endianness=None):
        return parse_int16(self.strict_read(2), endianness)

    def read_int32(self, endianness=None):
        return parse_int32(self.strict_read(4), endianness)

    def read_int64(self, endianness=None):
        return parse_int64(self.strict_read(8), endianness)

    def read_uint8(self):
        return parse_uint8(self.strict_read(1))

    def read_uint16(self, endianness=None):
        return parse_uint16(self.strict_read(2), endianness)

    def read_uint32(self, endianness=None):
        return parse_uint32(self.strict_read(4), endianness)

    def read_uint64(self, endianness=None):
        return parse_uint64(self.strict_read(8), endianness)

    def read_float32(self, endianness=None):
        return parse_float32(self.strict_read(4), endianness)

    def read_float64(self, endianness=None):
        return parse_float64(self.strict_read(8), endianness)

    def read_bool(self):
        return parse_bool(self.strict_read(1))

    def read_size_prefixed_int8(self):
        count = self.read_int8()
        return self.strict_read(count)

    def read_size_prefixed_int16(self, endianness=None):
        return self._read_size_prefixed(self.read_int16, endianness)

    def read_size_prefixed_int32(self, endianness=None):
        return self._read_size_prefixed(self.read_int32, endianness)

    def read_size_prefixed_int64(self, endianness=None):
        return self._read_size_prefixed(self.read_int64, endianness)

    def read_size_prefixed_uint8(self):
        count = self.read_uint8()
        return self.strict_read(count)

    def read_size_prefixed_uint16(self, endianness=None):
        return self._read_size_prefixed(self.read_uint16, endianness)

    def read_size_prefixed_uint32(self, endianness=None):
        return self._read_size_prefixed(self.read_uint32, endianness)

    def read_size_prefixed_uint64(self, endianness=None):
        return self._read_size_prefixed(self.read_uint64, endianness)

    def _read_size_prefixed(self, read_func, endianness):
        count = read_func(endianness)
        return self.strict_read(count)

    def read_string(self, length, encoding=None):
        if encoding is None:
            encoding = "utf-8"
        return self.strict_read(length).decode(encoding)

    def read_prefixed_string_int8(self, encoding=None):
        length = self.read_int8()
        return self.read_string(length, encoding)

    def read_prefixed_string_int16(self, endianness=None, encoding=None):
        return self._read_prefixed_string(self.read_int16,
            endianness, encoding)

    def read_prefixed_string_int32(self, endianness=None, encoding=None):
        return self._read_prefixed_string(self.read_int32,
            endianness, encoding)

    def read_prefixed_string_int64(self, endianness=None, encoding=None):
        return self._read_prefixed_string(self.read_int64,
            endianness, encoding)

    def read_prefixed_string_uint8(self, encoding=None):
        length = self.read_uint8()
        return self.read_string(length, encoding)

    def read_prefixed_string_uint16(self, endianness=None, encoding=None):
        return self._read_prefixed_string(self.read_uint16,
            endianness, encoding)

    def read_prefixed_string_uint32(self, endianness=None, encoding=None):
        return self._read_prefixed_string(self.read_uint32,
            endianness, encoding)

    def read_prefixed_string_uint64(self, endianness=None, encoding=None):
        return self._read_prefixed_string(self.read_uint64,
            endianness, encoding)

    def _read_prefixed_string(self, read_func, endianness, encoding):
        length = read_func(endianness)
        return self.read_string(length, encoding)


class BinaryWriter(BinaryStream):
    def __init__(self, endianness=Endian.native()):
        self.endianness = endianness
        super().__init__(bytes())

    def _to_collection(self, value):
        if isinstance(value, (list, tuple)):
            return value
        else:
            return tuple([value])

    def clear(self):
        self.seek(0)
        self._bytes = bytes()

    def to_bytes(self):
        return self._bytes

    def write_bytes(self, _bytes):
        prefix_bytes = self._bytes[:self.pos()]
        suffix_bytes = self._bytes[self.pos() + len(_bytes):]
        self._bytes = prefix_bytes + _bytes + suffix_bytes
        self.move(len(_bytes))

    def write_int8(self, numbers):
        self._write_non_endian_values(numbers, dump_int8)

    def write_int16(self, numbers):
        self._write_values(numbers, dump_int16)

    def write_int32(self, numbers):
        self._write_values(numbers, dump_int32)

    def write_int64(self, numbers):
        self._write_values(numbers, dump_int64)

    def write_uint8(self, numbers):
        self._write_non_endian_values(numbers, dump_uint8)

    def write_uint16(self, numbers):
        self._write_values(numbers, dump_uint16)

    def write_uint32(self, numbers):
        self._write_values(numbers, dump_uint32)

    def write_uint64(self, numbers):
        self._write_values(numbers, dump_uint64)

    def write_float32(self, numbers):
        self._write_values(numbers, dump_float32)

    def write_float64(self, numbers):
        self._write_values(numbers, dump_float64)

    def write_bool(self, values):
        self._write_non_endian_values(values, dump_bool)

    def _write_non_endian_values(self, values, dump_func):
        converted_values = self._to_collection(values)
        for value in converted_values:
            self.write_bytes(dump_func(value))

    def _write_values(self, values, dump_func):
        converted_values = self._to_collection(values)
        for value in converted_values:
            self.write_bytes(dump_func(value, self.endianness))

    def write_bytes_int8(self, bytes_collection):
        self._write_prefixed_bytes(bytes_collection, self.write_int8)

    def write_bytes_int16(self, bytes_collection):
        self._write_prefixed_bytes(bytes_collection, self.write_int16)

    def write_bytes_int32(self, bytes_collection):
        self._write_prefixed_bytes(bytes_collection, self.write_int32)

    def write_bytes_int64(self, bytes_collection):
        self._write_prefixed_bytes(bytes_collection, self.write_int64)

    def write_bytes_uint8(self, bytes_collection):
        self._write_prefixed_bytes(bytes_collection, self.write_uint8)

    def write_bytes_uint16(self, bytes_collection):
        self._write_prefixed_bytes(bytes_collection, self.write_uint16)

    def write_bytes_uint32(self, bytes_collection):
        self._write_prefixed_bytes(bytes_collection, self.write_uint32)

    def write_bytes_uint64(self, bytes_collection):
        self._write_prefixed_bytes(bytes_collection, self.write_uint64)

    def _write_prefixed_bytes(self, bytes_collection, write_func):
        converted_bytes = self._to_collection(bytes_collection)
        for _bytes in converted_bytes:
            write_func(len(_bytes))
            self.write_bytes(_bytes)

    def write_string(self, strings, encoding="utf-8"):
        converted_strings = self._to_collection(strings)
        for _string in converted_strings:
            self.write_bytes(_string.encode(encoding=encoding))

    def write_string_int8(self, strings, encoding="utf-8"):
        self._write_prefixed_strings(strings, self.write_bytes_int8, encoding)

    def write_string_int16(self, strings, encoding="utf-8"):
        self._write_prefixed_strings(strings, self.write_bytes_int16, encoding)

    def write_string_int32(self, strings, encoding="utf-8"):
        self._write_prefixed_strings(strings, self.write_bytes_int32, encoding)

    def write_string_int64(self, strings, encoding="utf-8"):
        self._write_prefixed_strings(strings, self.write_bytes_int64, encoding)

    def write_string_uint8(self, strings, encoding="utf-8"):
        self._write_prefixed_strings(strings, self.write_bytes_uint8, encoding)

    def write_string_uint16(self, strings, encoding="utf-8"):
        self._write_prefixed_strings(strings, self.write_bytes_uint16,
            encoding)

    def write_string_uint32(self, strings, encoding="utf-8"):
        self._write_prefixed_strings(strings, self.write_bytes_uint32,
            encoding)

    def write_string_uint64(self, strings, encoding="utf-8"):
        self._write_prefixed_strings(strings, self.write_bytes_uint64,
            encoding)

    def _write_prefixed_strings(self, strings, write_prefixed_func,
    encoding="utf-8"):
        converted_strings = self._to_collection(strings)
        for _string in converted_strings:
            write_prefixed_func(_string.encode(encoding=encoding))
