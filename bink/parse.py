import struct
import re
from bink.endian import Endian


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

STRUCT_ARG_OOR = "argument out of range"
STRUCT_ARG_TOO_LARGE = "int too large to convert"
STRUCT_TYPE_MISMATCH_REGEX = re.compile(
    "required argument is not (an|a) (integer|float)")


class BinaryError(Exception):
    pass


class BinaryOverflowError(BinaryError):
    pass


def _parse_from_format(frmt, _bytes, endianness=None):
    if endianness is None:
        endianness = Endian.NATIVE
    endian_str = "<" if endianness == Endian.LITTLE else ">"
    combined_format = endian_str + frmt

    try:
        _values = struct.unpack(combined_format, _bytes)
        return _values[0]
    except TypeError as e:
        raise TypeError(
            "Expected object of bytes-like type, not {0}."
            .format(type(_bytes).__name__))
    except struct.error as e:
        calced_size = struct.calcsize(combined_format)
        if calced_size != len(_bytes):
            raise BinaryError(
                "Length of byte buffer is {0}, expected {1}."
                .format(len(_bytes), calced_size))
        else:
            raise BinaryError(
                "Could not parse bytes {0}.".format(_bytes)) from e


def _dump_from_format(frmt, value, endianness=None):
    if endianness is None:
        endianness = Endian.NATIVE
    endian_str = "<" if endianness == Endian.LITTLE else ">"
    combined_format = endian_str + frmt
    try:
        return struct.pack(combined_format, value)
    except struct.error as e:
        # Hack to check if error was caused by a type mismatch.
        if STRUCT_TYPE_MISMATCH_REGEX.match(str(e)):
            raise TypeError(
                "Expected object of number-like type, not {0}."
                .format(type(value).__name__))
        # Hack to check if error was caused by argument out of bounds.
        elif str(e) == STRUCT_ARG_OOR or str(e) == STRUCT_ARG_TOO_LARGE:
            calced_size = struct.calcsize(combined_format)
            raise BinaryOverflowError(
                "Number {0} is too large to fit within {1} bytes."
                .format(value, calced_size))
        else:
            raise BinaryError(
                "Could not dump number {0}.".format(value)) from e


def parse_int8(byte):
    return _parse_from_format(INT8_FORMAT, byte)


def parse_int16(_bytes, endianness=None):
    return _parse_from_format(INT16_FORMAT, _bytes, endianness)


def parse_int32(_bytes, endianness=None):
    return _parse_from_format(INT32_FORMAT, _bytes, endianness)


def parse_int64(_bytes, endianness=None):
    return _parse_from_format(INT64_FORMAT, _bytes, endianness)


def parse_uint8(byte):
    return _parse_from_format(UINT8_FORMAT, byte)


def parse_uint16(_bytes, endianness=None):
    return _parse_from_format(UINT16_FORMAT, _bytes, endianness)


def parse_uint32(_bytes, endianness=None):
    return _parse_from_format(UINT32_FORMAT, _bytes, endianness)


def parse_uint64(_bytes, endianness=None):
    return _parse_from_format(UINT64_FORMAT, _bytes, endianness)


def parse_float32(_bytes, endianness=None):
    return _parse_from_format(FLOAT32_FORMAT, _bytes, endianness)


def parse_float64(_bytes, endianness=None):
    return _parse_from_format(FLOAT64_FORMAT, _bytes, endianness)


def parse_bool(byte):
    return parse_uint8(byte) != 0


def dump_int8(value):
    return _dump_from_format(INT8_FORMAT, value, None)


def dump_int16(value, endianness=None):
    return _dump_from_format(INT16_FORMAT, value, endianness)


def dump_int32(value, endianness=None):
    return _dump_from_format(INT32_FORMAT, value, endianness)


def dump_int64(value, endianness=None):
    return _dump_from_format(INT64_FORMAT, value, endianness)


def dump_uint8(value):
    return _dump_from_format(UINT8_FORMAT, value, None)


def dump_uint16(value, endianness=None):
    return _dump_from_format(UINT16_FORMAT, value, endianness)


def dump_uint32(value, endianness=None):
    return _dump_from_format(UINT32_FORMAT, value, endianness)


def dump_uint64(value, endianness=None):
    return _dump_from_format(UINT64_FORMAT, value, endianness)


def dump_float32(value, endianness=None):
    return _dump_from_format(FLOAT32_FORMAT, value, endianness)


def dump_float64(value, endianness=None):
    return _dump_from_format(FLOAT64_FORMAT, value, endianness)


def dump_bool(value):
    if not isinstance(value, bool):
        raise TypeError(
            "Expected object of boolean-like type, not {0}."
            .format(type(value).__name__))
    return dump_uint8(int(value))
