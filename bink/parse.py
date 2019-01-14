import struct
import re
from bink.endian import Endian

INT8_FORMAT = "b"
UINT8_FORMAT = "B"

INT16_FORMAT = "h"
UINT16_FORMAT = "H"

INT32_FORMAT = "i"
UINT32_FORMAT = "I"

INT64_FORMAT = "q"
UINT64_FORMAT = "Q"

FLOAT32_FORMAT = "f"
FLOAT64_FORMAT = "d"

STRUCT_ARG_OOR1 = "argument out of range"
STRUCT_ARG_OOR2 = re.compile(
    "format requires \(?-?\d+\)? <= number <= \(?-?\d+\)?")
STRUCT_ARG_TOO_LARGE = "int too large to convert"
STRUCT_TYPE_MISMATCH_REGEX = re.compile(
    "required argument is not (an|a) (integer|float)")


class BinaryError(Exception):
    pass


class BinarySizeMismatch(BinaryError):
    pass


def parse_int8(byte):
    return _parse_from_format(INT8_FORMAT, byte)


def parse_uint8(byte):
    return _parse_from_format(UINT8_FORMAT, byte)


def parse_int16(_bytes, endian=None):
    return _parse_from_format(INT16_FORMAT, _bytes, endian)


def parse_uint16(_bytes, endian=None):
    return _parse_from_format(UINT16_FORMAT, _bytes, endian)


def parse_int32(_bytes, endian=None):
    return _parse_from_format(INT32_FORMAT, _bytes, endian)


def parse_uint32(_bytes, endian=None):
    return _parse_from_format(UINT32_FORMAT, _bytes, endian)


def parse_int64(_bytes, endian=None):
    return _parse_from_format(INT64_FORMAT, _bytes, endian)


def parse_uint64(_bytes, endian=None):
    return _parse_from_format(UINT64_FORMAT, _bytes, endian)


def parse_float32(_bytes, endian=None):
    return _parse_from_format(FLOAT32_FORMAT, _bytes, endian)


def parse_float64(_bytes, endian=None):
    return _parse_from_format(FLOAT64_FORMAT, _bytes, endian)


def parse_bool(byte):
    return parse_uint8(byte) != 0


def dump_int8(value):
    return _dump_from_format(INT8_FORMAT, value)


def dump_uint8(value):
    return _dump_from_format(UINT8_FORMAT, value)


def dump_int16(value, endian=None):
    return _dump_from_format(INT16_FORMAT, value, endian)


def dump_uint16(value, endian=None):
    return _dump_from_format(UINT16_FORMAT, value, endian)


def dump_int32(value, endian=None):
    return _dump_from_format(INT32_FORMAT, value, endian)


def dump_uint32(value, endian=None):
    return _dump_from_format(UINT32_FORMAT, value, endian)


def dump_int64(value, endian=None):
    return _dump_from_format(INT64_FORMAT, value, endian)


def dump_uint64(value, endian=None):
    return _dump_from_format(UINT64_FORMAT, value, endian)


def dump_float32(value, endian=None):
    return _dump_from_format(FLOAT32_FORMAT, value, endian)


def dump_float64(value, endian=None):
    return _dump_from_format(FLOAT64_FORMAT, value, endian)


def dump_bool(value):
    if not isinstance(value, bool):
        raise TypeError(
            "Expected object of bool-like type, not '{0}'."
            .format(type(value).__name__))
    return dump_uint8(int(value))


def _parse_from_format(_format, _bytes, endian=None):
    fixed_format = _format_with_endian(_format, endian)
    try:
        _values = struct.unpack(fixed_format, _bytes)
        return _values[0]
    except TypeError as e:
        raise TypeError(
            "Expected object of bytes-like type, not '{0}'."
            .format(type(_bytes).__name__))
    except struct.error as e:
        calced_size = struct.calcsize(fixed_format)
        if calced_size != len(_bytes):
            raise BinarySizeMismatch(
                "Length of byte array is {0}, expected {1}."
                .format(len(_bytes), calced_size))
        else:
            raise BinaryError(
                "Could not parse bytes {0}.".format(_bytes)) from e


def _dump_from_format(_format, value, endian=None):
    fixed_format = _format_with_endian(_format, endian)
    try:
        return struct.pack(fixed_format, value)
    except struct.error as e:
        msg = str(e)
        # Hack to check if error was caused by a type mismatch.
        if STRUCT_TYPE_MISMATCH_REGEX.match(msg):
            raise TypeError(
                "Expected object of number-like type, not '{0}'."
                .format(type(value).__name__))
        # Hack to check if error was caused by argument out of bounds.
        elif (msg == STRUCT_ARG_OOR1 or STRUCT_ARG_OOR2.search(msg)
                or msg == STRUCT_ARG_TOO_LARGE):
            _raise_mismatch(fixed_format, value)
        else:
            raise BinaryError(
                "Could not dump number {0}.".format(value)) from e
    except OverflowError as e:
        _raise_mismatch(fixed_format, value)


def _format_with_endian(_format, endian=None):
    if endian is None:
        endian = Endian.NATIVE
    endian_char = "<" if endian == Endian.LITTLE else ">"
    return endian_char + _format


def _raise_mismatch(_format, value):
    calced_size = struct.calcsize(_format)
    raise BinarySizeMismatch(
        "Number {0} requires more than {1} bytes to store."
        .format(value, calced_size))
