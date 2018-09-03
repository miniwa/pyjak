import pytest
import re
from constants import (
    _INT8, _INT8_BYTES, _INT16, _INT16_BYTES, _INT16_BYTES_LITTLE,
    _INT16_BYTES_BIG, _INT32, _INT32_BYTES, _INT32_BYTES_LITTLE,
    _INT32_BYTES_BIG, _INT64, _INT64_BYTES, _INT64_BYTES_LITTLE,
    _INT64_BYTES_BIG, _UINT8, _UINT8_BYTES, _UINT16, _UINT16_BYTES,
    _UINT16_BYTES_LITTLE, _UINT16_BYTES_BIG, _UINT32, _UINT32_BYTES,
    _UINT32_BYTES_LITTLE, _UINT32_BYTES_BIG, _UINT64, _UINT64_BYTES,
    _UINT64_BYTES_LITTLE, _UINT64_BYTES_BIG, _FLOAT32, _FLOAT32_BYTES,
    _FLOAT32_BYTES_LITTLE, _FLOAT32_BYTES_BIG, _FLOAT64, _FLOAT64_BYTES,
    _FLOAT64_BYTES_LITTLE, _FLOAT64_BYTES_BIG, _BOOL_TRUE_BYTES,
    _BOOL_FALSE_BYTES)
from bink.endian import Endian
from bink.parse import (
    BinaryError, BinaryOverflowError, parse_int8, parse_int16, parse_int32,
    parse_int64, parse_uint8, parse_uint16, parse_uint32, parse_uint64,
    parse_float32, parse_float64, parse_bool, dump_int8, dump_int16,
    dump_int32, dump_int64, dump_uint8, dump_uint16, dump_uint32, dump_uint64,
    dump_float32, dump_float64, dump_bool)


_INVALID = "invalid"
_OVERFLOW = 999999999999999999999999999999999999999999999999999
_MISMATCH_BYTES = bytes(10)
_MISMATCH_PARSE_REGEX = re.compile(
    "Length of byte buffer is 10, expected \d.")
_OVERFLOW_DUMP_REGEX = re.compile(
    "Number \d+ is too large to fit within \d bytes.")
_TYPE_ERROR_PARSE_REGEX = re.compile(
    "Expected object of bytes-like type, not \w+.")
_TYPE_ERROR_DUMP_REGEX = re.compile(
    "Expected object of number-like type, not \w+.")
_TYPE_ERROR_DUMP_BOOL_REGEX = re.compile(
    "Expected object of boolean-like type, not \w+.")


class TestParse:
    def test_parse_int8(self):
        assert parse_int8(_INT8_BYTES) == _INT8

    def test_parse_int8_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_int8(_INVALID)

    def test_parse_int8_raises_binary_error_on_mismatch(self):
        with pytest.raises(BinaryError, match=_MISMATCH_PARSE_REGEX):
            parse_int8(_MISMATCH_BYTES)

    def test_parse_int16(self):
        assert parse_int16(_INT16_BYTES) == _INT16

    def test_parse_int16_little(self):
        assert parse_int16(_INT16_BYTES_LITTLE, Endian.LITTLE) == _INT16

    def test_parse_int16_big(self):
        assert parse_int16(_INT16_BYTES_BIG, Endian.BIG) == _INT16

    def test_parse_int16_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_int16(_INVALID)

    def test_parse_int16_raises_binary_error_on_mismatch(self):
        with pytest.raises(BinaryError, match=_MISMATCH_PARSE_REGEX):
            parse_int16(_MISMATCH_BYTES)

    def test_parse_int32(self):
        assert parse_int32(_INT32_BYTES) == _INT32

    def test_parse_int32_little(self):
        assert parse_int32(_INT32_BYTES_LITTLE, Endian.LITTLE) == _INT32

    def test_parse_int32_big(self):
        assert parse_int32(_INT32_BYTES_BIG, Endian.BIG) == _INT32

    def test_parse_int32_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_int32(_INVALID)

    def test_parse_int32_raises_binary_error_on_mismatch(self):
        with pytest.raises(BinaryError, match=_MISMATCH_PARSE_REGEX):
            parse_int32(_MISMATCH_BYTES)

    def test_parse_int64(self):
        assert parse_int64(_INT64_BYTES) == _INT64

    def test_parse_int64_little(self):
        assert parse_int64(_INT64_BYTES_LITTLE, Endian.LITTLE) == _INT64

    def test_parse_int64_big(self):
        assert parse_int64(_INT64_BYTES_BIG, Endian.BIG) == _INT64

    def test_parse_int64_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_int64(_INVALID)

    def test_parse_int64_raises_binary_error_on_mismatch(self):
        with pytest.raises(BinaryError, match=_MISMATCH_PARSE_REGEX):
            parse_int64(_MISMATCH_BYTES)

    def test_parse_uint8(self):
        assert parse_uint8(_UINT8_BYTES) == _UINT8

    def test_parse_uint8_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_uint8(_INVALID)

    def test_parse_uint8_raises_binary_error_on_mismatch(self):
        with pytest.raises(BinaryError, match=_MISMATCH_PARSE_REGEX):
            parse_uint8(_MISMATCH_BYTES)

    def test_parse_uint16(self):
        assert parse_uint16(_UINT16_BYTES) == _UINT16

    def test_parse_uint16_little(self):
        assert parse_uint16(_UINT16_BYTES_LITTLE, Endian.LITTLE) == _UINT16

    def test_parse_uint16_big(self):
        assert parse_uint16(_UINT16_BYTES_BIG, Endian.BIG) == _UINT16

    def test_parse_uint16_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_uint16(_INVALID)

    def test_parse_uint16_raises_binary_error_on_mismatch(self):
        with pytest.raises(BinaryError, match=_MISMATCH_PARSE_REGEX):
            parse_uint16(_MISMATCH_BYTES)

    def test_parse_uint32(self):
        assert parse_uint32(_UINT32_BYTES) == _UINT32

    def test_parse_uint32_little(self):
        assert parse_uint32(_UINT32_BYTES_LITTLE, Endian.LITTLE) == _UINT32

    def test_parse_uint32_big(self):
        assert parse_uint32(_UINT32_BYTES_BIG, Endian.BIG) == _UINT32

    def test_parse_uint32_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_uint32(_INVALID)

    def test_parse_uint32_raises_binary_error_on_mismatch(self):
        with pytest.raises(BinaryError, match=_MISMATCH_PARSE_REGEX):
            parse_uint32(_MISMATCH_BYTES)

    def test_parse_uint64(self):
        assert parse_uint64(_UINT64_BYTES) == _UINT64

    def test_parse_uint64_little(self):
        assert parse_uint64(_UINT64_BYTES_LITTLE, Endian.LITTLE) == _UINT64

    def test_parse_uint64_big(self):
        assert parse_uint64(_UINT64_BYTES_BIG, Endian.BIG) == _UINT64

    def test_parse_uint64_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_uint64(_INVALID)

    def test_parse_uint64_raises_binary_error_on_mismatch(self):
        with pytest.raises(BinaryError, match=_MISMATCH_PARSE_REGEX):
            parse_uint64(_MISMATCH_BYTES)

    def test_parse_float32(self):
        assert parse_float32(_FLOAT32_BYTES) == pytest.approx(_FLOAT32)

    def test_parse_float32_little(self):
        assert parse_float32(
            _FLOAT32_BYTES_LITTLE, Endian.LITTLE) == pytest.approx(_FLOAT32)

    def test_parse_float32_big(self):
        assert parse_float32(
            _FLOAT32_BYTES_BIG, Endian.BIG) == pytest.approx(_FLOAT32)

    def test_parse_float32_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_float32(_INVALID)

    def test_parse_float32_raises_binary_error_on_mismatch(self):
        with pytest.raises(BinaryError, match=_MISMATCH_PARSE_REGEX):
            parse_float32(_MISMATCH_BYTES)

    def test_parse_float64(self):
        assert parse_float64(_FLOAT64_BYTES) == pytest.approx(_FLOAT64)

    def test_parse_float64_little(self):
        assert parse_float64(
            _FLOAT64_BYTES_LITTLE, Endian.LITTLE) == pytest.approx(_FLOAT64)

    def test_parse_float64_big(self):
        assert parse_float64(
            _FLOAT64_BYTES_BIG, Endian.BIG) == pytest.approx(_FLOAT64)

    def test_parse_float64_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_float64(_INVALID)

    def test_parse_float64_raises_binary_error_on_mismatch(self):
        with pytest.raises(BinaryError, match=_MISMATCH_PARSE_REGEX):
            parse_float64(_MISMATCH_BYTES)

    def test_parse_bool_true(self):
        assert parse_bool(_BOOL_TRUE_BYTES)

    def test_parse_bool_false(self):
        assert parse_bool(_BOOL_FALSE_BYTES) is False

    def test_parse_bool_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_PARSE_REGEX):
            parse_bool(_INVALID)

    def test_parse_bool_raises_binary_error_on_mismatch(self):
        with pytest.raises(BinaryError, match=_MISMATCH_PARSE_REGEX):
            parse_bool(_MISMATCH_BYTES)


class TestDump:
    def test_dump_int8(self):
        assert dump_int8(_INT8) == _INT8_BYTES

    def test_dump_int8_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            dump_int8(_INVALID)

    def test_dump_int8_raises_overflow_error_on_overflow(self):
        with pytest.raises(BinaryOverflowError, match=_OVERFLOW_DUMP_REGEX):
            dump_int8(_OVERFLOW)

    def test_dump_int16(self):
        assert dump_int16(_INT16) == _INT16_BYTES

    def test_dump_int16_little(self):
        assert dump_int16(_INT16, Endian.LITTLE) == _INT16_BYTES_LITTLE

    def test_dump_int16_big(self):
        assert dump_int16(_INT16, Endian.BIG) == _INT16_BYTES_BIG

    def test_dump_int16_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            dump_int16(_INVALID)

    def test_dump_int16_raises_overflow_error_on_overflow(self):
        with pytest.raises(BinaryOverflowError, match=_OVERFLOW_DUMP_REGEX):
            dump_int16(_OVERFLOW)

    def test_dump_int32(self):
        assert dump_int32(_INT32) == _INT32_BYTES

    def test_dump_int32_little(self):
        assert dump_int32(_INT32, Endian.LITTLE) == _INT32_BYTES_LITTLE

    def test_dump_int32_big(self):
        assert dump_int32(_INT32, Endian.BIG) == _INT32_BYTES_BIG

    def test_dump_int32_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            dump_int32(_INVALID)

    def test_dump_int32_raises_overflow_error_on_overflow(self):
        with pytest.raises(BinaryOverflowError, match=_OVERFLOW_DUMP_REGEX):
            dump_int32(_OVERFLOW)

    def test_dump_int64(self):
        assert dump_int64(_INT64) == _INT64_BYTES

    def test_dump_int64_little(self):
        assert dump_int64(_INT64, Endian.LITTLE) == _INT64_BYTES_LITTLE

    def test_dump_int64_big(self):
        assert dump_int64(_INT64, Endian.BIG) == _INT64_BYTES_BIG

    def test_dump_int64_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            dump_int64(_INVALID)

    def test_dump_int64_raises_overflow_error_on_overflow(self):
        with pytest.raises(BinaryOverflowError, match=_OVERFLOW_DUMP_REGEX):
            dump_int64(_OVERFLOW)

    def test_dump_uint8(self):
        assert dump_uint8(_UINT8) == _UINT8_BYTES

    def test_dump_uint8_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            dump_uint8(_INVALID)

    def test_dump_uint8_raises_overflow_error_on_overflow(self):
        with pytest.raises(BinaryOverflowError, match=_OVERFLOW_DUMP_REGEX):
            dump_uint8(_OVERFLOW)

    def test_dump_uint16(self):
        assert dump_uint16(_UINT16) == _UINT16_BYTES

    def test_dump_uint16_little(self):
        assert dump_uint16(_UINT16, Endian.LITTLE) == _UINT16_BYTES_LITTLE

    def test_dump_uint16_big(self):
        assert dump_uint16(_UINT16, Endian.BIG) == _UINT16_BYTES_BIG

    def test_dump_uint16_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            dump_uint16(_INVALID)

    def test_dump_uint16_raises_overflow_error_on_overflow(self):
        with pytest.raises(BinaryOverflowError, match=_OVERFLOW_DUMP_REGEX):
            dump_uint16(_OVERFLOW)

    def test_dump_uint32(self):
        assert dump_uint32(_UINT32) == _UINT32_BYTES

    def test_dump_uint32_little(self):
        assert dump_uint32(_UINT32, Endian.LITTLE) == _UINT32_BYTES_LITTLE

    def test_dump_uint32_big(self):
        assert dump_uint32(_UINT32, Endian.BIG) == _UINT32_BYTES_BIG

    def test_dump_uint32_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            dump_uint32(_INVALID)

    def test_dump_uint32_raises_overflow_error_on_overflow(self):
        with pytest.raises(BinaryOverflowError, match=_OVERFLOW_DUMP_REGEX):
            dump_uint32(_OVERFLOW)

    def test_dump_uint64(self):
        assert dump_uint64(_UINT64) == _UINT64_BYTES

    def test_dump_uint64_little(self):
        assert dump_int64(_UINT64, Endian.LITTLE) == _UINT64_BYTES_LITTLE

    def test_dump_uint64_big(self):
        assert dump_uint64(_UINT64, Endian.BIG) == _UINT64_BYTES_BIG

    def test_dump_uint64_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            dump_uint64(_INVALID)

    def test_dump_uint64_raises_overflow_error_on_overflow(self):
        with pytest.raises(BinaryOverflowError, match=_OVERFLOW_DUMP_REGEX):
            dump_uint64(_OVERFLOW)

    def test_dump_float32(self):
        assert dump_float32(_FLOAT32) == _FLOAT32_BYTES

    def test_dump_float32_little(self):
        assert dump_float32(_FLOAT32, Endian.LITTLE) == _FLOAT32_BYTES_LITTLE

    def test_dump_float32_big(self):
        assert dump_float32(_FLOAT32, Endian.BIG) == _FLOAT32_BYTES_BIG

    def test_dump_float32_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            dump_float32(_INVALID)

    def test_dump_float32_raises_overflow_error_on_overflow(self):
        with pytest.raises(BinaryOverflowError, match=_OVERFLOW_DUMP_REGEX):
            dump_float32(_OVERFLOW)

    def test_dump_float64(self):
        assert dump_float64(_FLOAT64) == _FLOAT64_BYTES

    def test_dump_float64_little(self):
        assert dump_float64(_FLOAT64, Endian.LITTLE) == _FLOAT64_BYTES_LITTLE

    def test_dump_float64_big(self):
        assert dump_float64(_FLOAT64, Endian.BIG) == _FLOAT64_BYTES_BIG

    def test_dump_float64_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_REGEX):
            dump_float64(_INVALID)

    def test_dump_float64_raises_overflow_error_on_overflow(self):
        with pytest.raises(BinaryOverflowError, match=_OVERFLOW_DUMP_REGEX):
            dump_float64(_OVERFLOW)

    def test_dump_bool_true(self):
        assert dump_bool(True) == _BOOL_TRUE_BYTES

    def test_dump_bool_false(self):
        assert dump_bool(False) == _BOOL_FALSE_BYTES

    def test_dump_bool_raises_type_error_on_invalid_type(self):
        with pytest.raises(TypeError, match=_TYPE_ERROR_DUMP_BOOL_REGEX):
            dump_bool(_INVALID)
