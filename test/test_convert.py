import pytest
import re
import struct
from pyjak import (
    BinaryError, BinarySizeMismatch, parse_int8, parse_int16, parse_int32,
    parse_int64, parse_uint8, parse_uint16, parse_uint32, parse_uint64,
    parse_float32, parse_float64, parse_bool, dump_int8, dump_int16,
    dump_int32, dump_int64, dump_uint8, dump_uint16, dump_uint32, dump_uint64,
    dump_float32, dump_float64, dump_bool, ByteOrder)

_INT8_MIN = -128
_INT8_MAX = 127
_INT8_MIN_BYTES = struct.pack("=b", _INT8_MIN)
_INT8_MAX_BYTES = struct.pack("=b", _INT8_MAX)

_UINT8_MIN = 0
_UINT8_MAX = 255
_UINT8_MIN_BYTES = struct.pack("=B", _UINT8_MIN)
_UINT8_MAX_BYTES = struct.pack("=B", _UINT8_MAX)

_INT16_MIN = -32768
_INT16_MAX = 32767
_INT16_MIN_BYTES = struct.pack("=h", _INT16_MIN)
_INT16_MAX_BYTES = struct.pack("=h", _INT16_MAX)
_INT16_MAX_BYTES_LITTLE = struct.pack("<h", _INT16_MAX)
_INT16_MAX_BYTES_BIG = struct.pack(">h", _INT16_MAX)

_UINT16_MIN = 0
_UINT16_MAX = 65535
_UINT16_MIN_BYTES = struct.pack("=H", _UINT16_MIN)
_UINT16_MAX_BYTES = struct.pack("=H", _UINT16_MAX)
_UINT16_MAX_BYTES_LITTLE = struct.pack("<H", _UINT16_MAX)
_UINT16_MAX_BYTES_BIG = struct.pack(">H", _UINT16_MAX)

_INT32_MIN = -2147483648
_INT32_MAX = 2147483647
_INT32_MIN_BYTES = struct.pack("=i", _INT32_MIN)
_INT32_MAX_BYTES = struct.pack("=i", _INT32_MAX)
_INT32_MAX_BYTES_LITTLE = struct.pack("<i", _INT32_MAX)
_INT32_MAX_BYTES_BIG = struct.pack(">i", _INT32_MAX)

_UINT32_MIN = 0
_UINT32_MAX = 4294967295
_UINT32_MIN_BYTES = struct.pack("=I", _UINT32_MIN)
_UINT32_MAX_BYTES = struct.pack("=I", _UINT32_MAX)
_UINT32_MAX_BYTES_LITTLE = struct.pack("<I", _UINT32_MAX)
_UINT32_MAX_BYTES_BIG = struct.pack(">I", _UINT32_MAX)

_INT64_MIN = -9223372036854775808
_INT64_MAX = 9223372036854775807
_INT64_MIN_BYTES = struct.pack("=q", _INT64_MIN)
_INT64_MAX_BYTES = struct.pack("=q", _INT64_MAX)
_INT64_MAX_BYTES_LITTLE = struct.pack("<q", _INT64_MAX)
_INT64_MAX_BYTES_BIG = struct.pack(">q", _INT64_MAX)

_UINT64_MIN = 0
_UINT64_MAX = 18446744073709551615
_UINT64_MIN_BYTES = struct.pack("=Q", _UINT64_MIN)
_UINT64_MAX_BYTES = struct.pack("=Q", _UINT64_MAX)
_UINT64_MAX_BYTES_LITTLE = struct.pack("<Q", _UINT64_MAX)
_UINT64_MAX_BYTES_BIG = struct.pack(">Q", _UINT64_MAX)

_FLOAT32 = 1000.135
_FLOAT32_BYTES = struct.pack("=f", _FLOAT32)
_FLOAT32_BYTES_LITTLE = struct.pack("<f", _FLOAT32)
_FLOAT32_BYTES_BIG = struct.pack(">f", _FLOAT32)

_FLOAT64 = 10000000000.135
_FLOAT64_BYTES = struct.pack("=d", _FLOAT64)
_FLOAT64_BYTES_LITTLE = struct.pack("<d", _FLOAT64)
_FLOAT64_BYTES_BIG = struct.pack(">d", _FLOAT64)

_BOOL_TRUE_BYTES = struct.pack("=b", 1)
_BOOL_FALSE_BYTES = struct.pack("=b", 0)

_INVALID = "invalid"
_MISMATCH_BYTES = bytes(10)
_MISMATCH_PARSE_REGEX = re.compile(
    "Length of byte array is 10, expected \d.")
_MISMATCH_DUMP_REGEX = re.compile(
    "Number -?(\d+|\d+\.\d+e\+\d+) requires a different sign or " +
    "more than \d bytes to store.")
_TYPE_ERROR_PARSE_REGEX = re.compile(
    "Expected object of bytes-like type, not '\w+'.")
_TYPE_ERROR_DUMP_REGEX = re.compile(
    "Expected object of number-like type, not '\w+'.")
_TYPE_ERROR_DUMP_BOOL_REGEX = re.compile(
    "Expected object of bool-like type, not '\w+'.")


class ParseBase:
    _PARSE_FUNC = None
    _VALUE_MIN = None
    _VALUE_MAX = None
    _VALUE_MIN_BYTES = None
    _VALUE_MAX_BYTES = None

    def setup_method(self, method):
        self.parse_func = self.__class__._PARSE_FUNC
        self.value_min = self.__class__._VALUE_MIN
        self.value_max = self.__class__._VALUE_MAX
        self.value_min_bytes = self.__class__._VALUE_MIN_BYTES
        self.value_max_bytes = self.__class__._VALUE_MAX_BYTES

    def test_parse(self):
        assert self.parse_func(self.value_min_bytes) == self.value_min
        assert self.parse_func(self.value_max_bytes) == self.value_max

    def test_parse_raises_type_error_on_none(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            self.parse_func(None)

    def test_parse_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            self.parse_func(_INVALID)

    def test_parse_raises_mismatch_error_on_mismatch(self):
        with pytest.raises(BinarySizeMismatch, match=_MISMATCH_PARSE_REGEX):
            self.parse_func(_MISMATCH_BYTES)


class ParseByteOrderBase(ParseBase):
    _VALUE_MAX_BYTES_LITTLE = None
    _VALUE_MAX_BYTES_BIG = None

    def setup_method(self, method):
        self.parse_func = self.__class__._PARSE_FUNC
        self.value_min = self.__class__._VALUE_MIN
        self.value_max = self.__class__._VALUE_MAX
        self.value_min_bytes = self.__class__._VALUE_MIN_BYTES
        self.value_max_bytes = self.__class__._VALUE_MAX_BYTES
        self.value_max_bytes_little = self.__class__._VALUE_MAX_BYTES_LITTLE
        self.value_max_bytes_big = self.__class__._VALUE_MAX_BYTES_BIG

    def test_parse_little(self):
        assert self.parse_func(
            self.value_max_bytes_little, ByteOrder.LITTLE) == self.value_max

    def test_parse_big(self):
        assert self.parse_func(
            self.value_max_bytes_big, ByteOrder.BIG) == self.value_max


class TestParseInt8(ParseBase):
    _PARSE_FUNC = parse_int8
    _VALUE_MIN = _INT8_MIN
    _VALUE_MAX = _INT8_MAX
    _VALUE_MIN_BYTES = _INT8_MIN_BYTES
    _VALUE_MAX_BYTES = _INT8_MAX_BYTES


class TestParseUInt8(ParseBase):
    _PARSE_FUNC = parse_uint8
    _VALUE_MIN = _UINT8_MIN
    _VALUE_MAX = _UINT8_MAX
    _VALUE_MIN_BYTES = _UINT8_MIN_BYTES
    _VALUE_MAX_BYTES = _UINT8_MAX_BYTES


class TestParseInt16(ParseByteOrderBase):
    _PARSE_FUNC = parse_int16
    _VALUE_MIN = _INT16_MIN
    _VALUE_MAX = _INT16_MAX
    _VALUE_MIN_BYTES = _INT16_MIN_BYTES
    _VALUE_MAX_BYTES = _INT16_MAX_BYTES
    _VALUE_MAX_BYTES_LITTLE = _INT16_MAX_BYTES_LITTLE
    _VALUE_MAX_BYTES_BIG = _INT16_MAX_BYTES_BIG


class TestParseUInt16(ParseByteOrderBase):
    _PARSE_FUNC = parse_uint16
    _VALUE_MIN = _UINT16_MIN
    _VALUE_MAX = _UINT16_MAX
    _VALUE_MIN_BYTES = _UINT16_MIN_BYTES
    _VALUE_MAX_BYTES = _UINT16_MAX_BYTES
    _VALUE_MAX_BYTES_LITTLE = _UINT16_MAX_BYTES_LITTLE
    _VALUE_MAX_BYTES_BIG = _UINT16_MAX_BYTES_BIG


class TestParseInt32(ParseByteOrderBase):
    _PARSE_FUNC = parse_int32
    _VALUE_MIN = _INT32_MIN
    _VALUE_MAX = _INT32_MAX
    _VALUE_MIN_BYTES = _INT32_MIN_BYTES
    _VALUE_MAX_BYTES = _INT32_MAX_BYTES
    _VALUE_MAX_BYTES_LITTLE = _INT32_MAX_BYTES_LITTLE
    _VALUE_MAX_BYTES_BIG = _INT32_MAX_BYTES_BIG


class TestParseUInt32(ParseByteOrderBase):
    _PARSE_FUNC = parse_uint32
    _VALUE_MIN = _UINT32_MIN
    _VALUE_MAX = _UINT32_MAX
    _VALUE_MIN_BYTES = _UINT32_MIN_BYTES
    _VALUE_MAX_BYTES = _UINT32_MAX_BYTES
    _VALUE_MAX_BYTES_LITTLE = _UINT32_MAX_BYTES_LITTLE
    _VALUE_MAX_BYTES_BIG = _UINT32_MAX_BYTES_BIG


class TestParseInt64(ParseByteOrderBase):
    _PARSE_FUNC = parse_int64
    _VALUE_MIN = _INT64_MIN
    _VALUE_MAX = _INT64_MAX
    _VALUE_MIN_BYTES = _INT64_MIN_BYTES
    _VALUE_MAX_BYTES = _INT64_MAX_BYTES
    _VALUE_MAX_BYTES_LITTLE = _INT64_MAX_BYTES_LITTLE
    _VALUE_MAX_BYTES_BIG = _INT64_MAX_BYTES_BIG


class TestParseUInt64(ParseByteOrderBase):
    _PARSE_FUNC = parse_uint64
    _VALUE_MIN = _UINT64_MIN
    _VALUE_MAX = _UINT64_MAX
    _VALUE_MIN_BYTES = _UINT64_MIN_BYTES
    _VALUE_MAX_BYTES = _UINT64_MAX_BYTES
    _VALUE_MAX_BYTES_LITTLE = _UINT64_MAX_BYTES_LITTLE
    _VALUE_MAX_BYTES_BIG = _UINT64_MAX_BYTES_BIG


class TestParseFloat32:
    def test_parse_float32(self):
        assert parse_float32(_FLOAT32_BYTES) == pytest.approx(_FLOAT32)

    def test_parse_float32_little(self):
        assert parse_float32(
            _FLOAT32_BYTES_LITTLE, ByteOrder.LITTLE) == pytest.approx(_FLOAT32)

    def test_parse_float32_big(self):
        assert parse_float32(
            _FLOAT32_BYTES_BIG, ByteOrder.BIG) == pytest.approx(_FLOAT32)

    def test_parse_float32_raises_type_error_on_none(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_float32(None)

    def test_parse_float32_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_float32(_INVALID)

    def test_parse_float32_raises_mismatch_error_on_mismatch(self):
        with pytest.raises(BinaryError, match=_MISMATCH_PARSE_REGEX):
            parse_float32(_MISMATCH_BYTES)


class TestParseFloat64:
    def test_parse_float64(self):
        assert parse_float64(_FLOAT64_BYTES) == pytest.approx(_FLOAT64)

    def test_parse_float64_little(self):
        assert parse_float64(
            _FLOAT64_BYTES_LITTLE, ByteOrder.LITTLE) == pytest.approx(_FLOAT64)

    def test_parse_float64_big(self):
        assert parse_float64(
            _FLOAT64_BYTES_BIG, ByteOrder.BIG) == pytest.approx(_FLOAT64)

    def test_parse_float64_raises_type_error_on_none(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_float64(None)

    def test_parse_float64_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_float64(_INVALID)

    def test_parse_float64_raises_mismatch_error_on_mismatch(self):
        with pytest.raises(BinaryError, match=_MISMATCH_PARSE_REGEX):
            parse_float64(_MISMATCH_BYTES)


class TestParseBool:
    def test_parse_bool_true(self):
        assert parse_bool(_BOOL_TRUE_BYTES)

    def test_parse_bool_false(self):
        assert parse_bool(_BOOL_FALSE_BYTES) is False

    def test_parse_bool_raises_type_error_on_none(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_bool(None)

    def test_parse_bool_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_bool(_INVALID)

    def test_parse_bool_raises_mismatch_error_on_mismatch(self):
        with pytest.raises(BinaryError, match=_MISMATCH_PARSE_REGEX):
            parse_bool(_MISMATCH_BYTES)


class DumpBase:
    _DUMP_FUNC = None
    _VALUE_MIN = None
    _VALUE_MAX = None
    _VALUE_MIN_BYTES = None
    _VALUE_MAX_BYTES = None

    def setup_method(self, method):
        self.dump_func = self.__class__._DUMP_FUNC
        self.value_min = self.__class__._VALUE_MIN
        self.value_max = self.__class__._VALUE_MAX
        self.value_min_bytes = self.__class__._VALUE_MIN_BYTES
        self.value_max_bytes = self.__class__._VALUE_MAX_BYTES

    def test_dump(self):
        assert self.dump_func(self.value_min) == self.value_min_bytes
        assert self.dump_func(self.value_max) == self.value_max_bytes

    def test_dump_raises_type_error_on_none(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            self.dump_func(None)

    def test_dump_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            self.dump_func(_INVALID)

    def test_dump_raises_mismatch_error_on_mismatch(self):
        with pytest.raises(BinarySizeMismatch, match=_MISMATCH_DUMP_REGEX):
            self.dump_func(self.value_min - 1)
        with pytest.raises(BinarySizeMismatch, match=_MISMATCH_DUMP_REGEX):
            self.dump_func(self.value_max + 1)


class DumpByteOrderBase(DumpBase):
    _VALUE_MAX_BYTES_LITTLE = None
    _VALUE_MAX_BYTES_BIG = None

    def setup_method(self, method):
        self.dump_func = self.__class__._DUMP_FUNC
        self.value_min = self.__class__._VALUE_MIN
        self.value_max = self.__class__._VALUE_MAX
        self.value_min_bytes = self.__class__._VALUE_MIN_BYTES
        self.value_max_bytes = self.__class__._VALUE_MAX_BYTES
        self.value_max_bytes_little = self.__class__._VALUE_MAX_BYTES_LITTLE
        self.value_max_bytes_big = self.__class__._VALUE_MAX_BYTES_BIG

    def test_dump_little(self):
        assert self.dump_func(
            self.value_max, ByteOrder.LITTLE) == self.value_max_bytes_little

    def test_dump_big(self):
        assert self.dump_func(
            self.value_max, ByteOrder.BIG) == self.value_max_bytes_big


class TestDumpInt8(DumpBase):
    _DUMP_FUNC = dump_int8
    _VALUE_MIN = _INT8_MIN
    _VALUE_MAX = _INT8_MAX
    _VALUE_MIN_BYTES = _INT8_MIN_BYTES
    _VALUE_MAX_BYTES = _INT8_MAX_BYTES


class TestDumpUInt8(DumpBase):
    _DUMP_FUNC = dump_uint8
    _VALUE_MIN = _UINT8_MIN
    _VALUE_MAX = _UINT8_MAX
    _VALUE_MIN_BYTES = _UINT8_MIN_BYTES
    _VALUE_MAX_BYTES = _UINT8_MAX_BYTES


class TestDumpInt16(DumpByteOrderBase):
    _DUMP_FUNC = dump_int16
    _VALUE_MIN = _INT16_MIN
    _VALUE_MAX = _INT16_MAX
    _VALUE_MIN_BYTES = _INT16_MIN_BYTES
    _VALUE_MAX_BYTES = _INT16_MAX_BYTES
    _VALUE_MAX_BYTES_LITTLE = _INT16_MAX_BYTES_LITTLE
    _VALUE_MAX_BYTES_BIG = _INT16_MAX_BYTES_BIG


class TestDumpUInt16(DumpByteOrderBase):
    _DUMP_FUNC = dump_uint16
    _VALUE_MIN = _UINT16_MIN
    _VALUE_MAX = _UINT16_MAX
    _VALUE_MIN_BYTES = _UINT16_MIN_BYTES
    _VALUE_MAX_BYTES = _UINT16_MAX_BYTES
    _VALUE_MAX_BYTES_LITTLE = _UINT16_MAX_BYTES_LITTLE
    _VALUE_MAX_BYTES_BIG = _UINT16_MAX_BYTES_BIG


class TestDumpInt32(DumpByteOrderBase):
    _DUMP_FUNC = dump_int32
    _VALUE_MIN = _INT32_MIN
    _VALUE_MAX = _INT32_MAX
    _VALUE_MIN_BYTES = _INT32_MIN_BYTES
    _VALUE_MAX_BYTES = _INT32_MAX_BYTES
    _VALUE_MAX_BYTES_LITTLE = _INT32_MAX_BYTES_LITTLE
    _VALUE_MAX_BYTES_BIG = _INT32_MAX_BYTES_BIG


class TestDumpUInt32(DumpByteOrderBase):
    _DUMP_FUNC = dump_uint32
    _VALUE_MIN = _UINT32_MIN
    _VALUE_MAX = _UINT32_MAX
    _VALUE_MIN_BYTES = _UINT32_MIN_BYTES
    _VALUE_MAX_BYTES = _UINT32_MAX_BYTES
    _VALUE_MAX_BYTES_LITTLE = _UINT32_MAX_BYTES_LITTLE
    _VALUE_MAX_BYTES_BIG = _UINT32_MAX_BYTES_BIG


class TestDumpInt64(DumpByteOrderBase):
    _DUMP_FUNC = dump_int64
    _VALUE_MIN = _INT64_MIN
    _VALUE_MAX = _INT64_MAX
    _VALUE_MIN_BYTES = _INT64_MIN_BYTES
    _VALUE_MAX_BYTES = _INT64_MAX_BYTES
    _VALUE_MAX_BYTES_LITTLE = _INT64_MAX_BYTES_LITTLE
    _VALUE_MAX_BYTES_BIG = _INT64_MAX_BYTES_BIG


class TestDumpUInt64(DumpByteOrderBase):
    _DUMP_FUNC = dump_uint64
    _VALUE_MIN = _UINT64_MIN
    _VALUE_MAX = _UINT64_MAX
    _VALUE_MIN_BYTES = _UINT64_MIN_BYTES
    _VALUE_MAX_BYTES = _UINT64_MAX_BYTES
    _VALUE_MAX_BYTES_LITTLE = _UINT64_MAX_BYTES_LITTLE
    _VALUE_MAX_BYTES_BIG = _UINT64_MAX_BYTES_BIG


class TestDumpFloat32:
    def test_dump_float32(self):
        assert dump_float32(_FLOAT32) == _FLOAT32_BYTES

    def test_dump_float32_little(self):
        assert dump_float32(
            _FLOAT32, ByteOrder.LITTLE) == _FLOAT32_BYTES_LITTLE

    def test_dump_float32_big(self):
        assert dump_float32(_FLOAT32, ByteOrder.BIG) == _FLOAT32_BYTES_BIG

    def test_dump_float32_raises_type_error_on_none(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            dump_float32(None)

    def test_dump_float32_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            dump_float32(_INVALID)

    def test_dump_float32_raises_mismatch_error_on_mismatch(self):
        with pytest.raises(BinarySizeMismatch, match=_MISMATCH_DUMP_REGEX):
            dump_float32(3.4e39)
        with pytest.raises(BinarySizeMismatch, match=_MISMATCH_DUMP_REGEX):
            dump_float32(-3.4e39)


class TestDumpFloat64:
    def test_dump_float64(self):
        assert dump_float64(_FLOAT64) == _FLOAT64_BYTES

    def test_dump_float64_little(self):
        assert dump_float64(
            _FLOAT64, ByteOrder.LITTLE) == _FLOAT64_BYTES_LITTLE

    def test_dump_float64_big(self):
        assert dump_float64(_FLOAT64, ByteOrder.BIG) == _FLOAT64_BYTES_BIG

    def test_dump_float64_raises_type_error_on_none(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            dump_float64(None)

    def test_dump_float64_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            dump_float64(_INVALID)


class TestDumpBool:
    def test_dump_bool_true(self):
        assert dump_bool(True) == _BOOL_TRUE_BYTES

    def test_dump_bool_false(self):
        assert dump_bool(False) == _BOOL_FALSE_BYTES

    def test_dump_bool_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_BOOL_REGEX):
            dump_bool(_INVALID)
