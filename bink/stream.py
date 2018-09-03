from bink.endian import Endian
from bink.parse import (parse_int8, parse_int16, parse_int32, parse_int64,
    parse_uint8, parse_uint16, parse_uint32, parse_uint64,
    parse_float32, parse_float64, parse_bool, dump_int8, dump_int16,
    dump_int32, dump_int64, dump_uint8, dump_uint16, dump_uint32, dump_uint64,
    dump_float32, dump_float64, dump_bool)


class BinaryStream:
    def __init__(self, _bytes, endianness=None):
        if endianness is None:
            endianness = Endian.NATIVE
        self._bytes = _bytes
        self.endianness = endianness
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
    def __init__(self, _bytes, endianness=None):
        super().__init__(_bytes, endianness)

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

    def read_int8(self, count=1):
        return self._read_values(parse_int8, 1, count, False)

    def read_int16(self, count=1):
        return self._read_values(parse_int16, 2, count)

    def read_int32(self, count=1):
        return self._read_values(parse_int32, 4, count)

    def read_int64(self, count=1):
        return self._read_values(parse_int64, 8, count)

    def read_uint8(self, count=1):
        return self._read_values(parse_uint8, 1, count, False)

    def read_uint16(self, count=1):
        return self._read_values(parse_uint16, 2, count)

    def read_uint32(self, count=1):
        return self._read_values(parse_uint32, 4, count)

    def read_uint64(self, count=1):
        return self._read_values(parse_uint64, 8, count)

    def read_float32(self, count=1):
        return self._read_values(parse_float32, 4, count)

    def read_float64(self, count=1):
        return self._read_values(parse_float64, 8, count)

    def read_bool(self, count=1):
        return self._read_values(parse_bool, 1, count, False)

    def _read_values(self, parse_func, length, count, endian=True):
        assert length > 0
        assert count > 0
        _values = []
        for i in range(count):
            if endian:
                _values.append(
                    parse_func(self.strict_read(length), self.endianness))
            else:
                _values.append(parse_func(self.strict_read(length)))
        if len(_values) == 1:
            return _values[0]
        else:
            return _values


class BinaryWriter(BinaryStream):
    def __init__(self, endianness=None):
        super().__init__(bytes(), endianness)

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

    def _to_collection(self, value):
        if isinstance(value, (list, tuple)):
            return value
        else:
            return tuple([value])
