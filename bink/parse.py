import struct
import re
from bink.endian import Endian


class BinaryError(Exception):
    """
    Base class for exceptions related to converting binary numbers.
    """
    pass


class BinarySizeMismatch(BinaryError):
    """
    Raised when there is a mismatch in size between expected input and output.
    For example when trying to convert the number 1000 into a 1 byte integer.
    """
    pass


def parse_int8(_bytes):
    """
    Parses a given byte array as a signed 1 byte integer.
    Args:
        _bytes: The byte array to be parsed.
    Raises:
        TypeError: If byte array is not of type 'bytes' or 'bytearray'.
        BinarySizeMismatch: If length of byte array is not equal to 1.
        BinaryError: If an unexpected conversation error occurs.
    Returns:
        The integer that was parsed.
    """
    return _parse_from_format(_INT8_FORMAT, _bytes)


def parse_uint8(_bytes):
    """
    Parses a given byte array as an unsigned 1 byte integer.
    Args:
        _bytes: The byte array to be parsed.
    Raises:
        TypeError: If byte array is not of type 'bytes' or 'bytearray'.
        BinarySizeMismatch: If length of byte array is not equal to 1.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        The integer that was parsed.
    """
    return _parse_from_format(_UINT8_FORMAT, _bytes)


def parse_int16(_bytes, endian=None):
    """
    Parses a given byte array as a signed 2 byte integer.
    Args:
        _bytes: The byte array to be parsed.
        endian: The byte order of the byte array. Defaults to native order.
    Raises:
        TypeError: If byte array is not of type 'bytes' or 'bytearray'.
        BinarySizeMismatch: If length of byte array is not equal to 2.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        The integer that was parsed.
    """
    return _parse_from_format(_INT16_FORMAT, _bytes, endian)


def parse_uint16(_bytes, endian=None):
    """
    Parses a given byte array as an unsigned 2 byte integer.
    Args:
        _bytes: The byte array to be parsed.
        endian: The byte order of the byte array. Defaults to native order.
    Raises:
        TypeError: If byte array is not of type 'bytes' or 'bytearray'.
        BinarySizeMismatch: If length of byte array is not equal to 2.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        The integer that was parsed.
    """
    return _parse_from_format(_UINT16_FORMAT, _bytes, endian)


def parse_int32(_bytes, endian=None):
    """
    Parses a given byte array as a signed 4 byte integer.
    Args:
        _bytes: The byte array to be parsed.
        endian: The byte order of the byte array. Defaults to native order.
    Raises:
        TypeError: If byte array is not of type 'bytes' or 'bytearray'.
        BinarySizeMismatch: If length of byte array is not equal to 4.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        The integer that was parsed.
    """
    return _parse_from_format(_INT32_FORMAT, _bytes, endian)


def parse_uint32(_bytes, endian=None):
    """
    Parses a given byte array as an unsigned 4 byte integer.
    Args:
        _bytes: The byte array to be parsed.
        endian: The byte order of the byte array. Defaults to native order.
    Raises:
        TypeError: If byte array is not of type 'bytes' or 'bytearray'.
        BinarySizeMismatch: If length of byte array is not equal to 4.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        The integer that was parsed.
    """
    return _parse_from_format(_UINT32_FORMAT, _bytes, endian)


def parse_int64(_bytes, endian=None):
    """
    Parses a given byte array as a signed 8 byte integer.
    Args:
        _bytes: The byte array to be parsed.
        endian: The byte order of the byte array. Defaults to native order.
    Raises:
        TypeError: If byte array is not of type 'bytes' or 'bytearray'.
        BinarySizeMismatch: If length of byte array is not equal to 8.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        The integer that was parsed.
    """
    return _parse_from_format(_INT64_FORMAT, _bytes, endian)


def parse_uint64(_bytes, endian=None):
    """
    Parses a given byte array as an unsigned 8 byte integer.
    Args:
        _bytes: The byte array to be parsed.
        endian: The byte order of the byte array. Defaults to native order.
    Raises:
        TypeError: If byte array is not of type 'bytes' or 'bytearray'.
        BinarySizeMismatch: If length of byte array is not equal to 8.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        The integer that was parsed.
    """
    return _parse_from_format(_UINT64_FORMAT, _bytes, endian)


def parse_float32(_bytes, endian=None):
    """
    Parses a given byte array as a 4 byte float.
    Args:
        _bytes: The byte array to be parsed.
        endian: The byte order of the byte array. Defaults to native order.
    Raises:
        TypeError: If byte array is not of type 'bytes' or 'bytearray'.
        BinarySizeMismatch: If length of byte array is not equal to 4.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        The float that was parsed.
    """
    return _parse_from_format(_FLOAT32_FORMAT, _bytes, endian)


def parse_float64(_bytes, endian=None):
    """
    Parses a given byte array as a 8 byte float.
    Args:
        _bytes: The byte array to be parsed.
        endian: The byte order of the byte array. Defaults to native order.
    Raises:
        TypeError: If byte array is not of type 'bytes' or 'bytearray'.
        BinarySizeMismatch: If length of byte array is not equal to 8.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        The float that was parsed.
    """
    return _parse_from_format(_FLOAT64_FORMAT, _bytes, endian)


def parse_bool(_bytes):
    """
    Parses a given byte array as a uint8, then converts that value to a bool.
    Args:
        _bytes: The byte array to be parsed.
        endian: The byte order of the byte array. Defaults to native order.
    Raises:
        TypeError: If byte array is not of type 'bytes' or 'bytearray'.
        BinarySizeMismatch: If length of byte array is not equal to 2.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        False if the parsed uint8 equals 0.
        True otherwise.
    """
    return parse_uint8(_bytes) != 0


def dump_int8(_int):
    """
    Serializes a given integer as a signed 1 byte integer in binary form.
    Args:
        _int: The integer to be serialized.
    Raises:
        TypeError: If integer is not of type 'int'.
        BinarySizeMismatch: If value is too small or too big to be held by
            a signed 1 byte integer.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        A byte array containing the serialized integer.
    """
    return _dump_from_format(_INT8_FORMAT, _int)


def dump_uint8(_int):
    """
    Serializes a given integer as an unsigned 1 byte integer in binary form.
    Args:
        _int: The integer to be serialized.
    Raises:
        TypeError: If integer is not of type 'int'.
        BinarySizeMismatch: If value is too small or too big to be held by
            an unsigned 1 byte integer.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        A byte array containing the serialized integer.
    """
    return _dump_from_format(_UINT8_FORMAT, _int)


def dump_int16(_int, endian=None):
    """
    Serializes a given integer as a signed 2 byte integer in binary form.
    Args:
        _int: The integer to be serialized.
        endian: The byte order of the returned byte array. Defaults to native.
    Raises:
        TypeError: If integer is not of type 'int'.
        BinarySizeMismatch: If value is too small or too big to be held by
            a signed 2 byte integer.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        A byte array containing the serialized integer.
    """
    return _dump_from_format(_INT16_FORMAT, _int, endian)


def dump_uint16(_int, endian=None):
    """
    Serializes a given integer as an unsigned 2 byte integer in binary form.
    Args:
        _int: The integer to be serialized.
        endian: The byte order of the returned byte array. Defaults to native.
    Raises:
        TypeError: If integer is not of type 'int'.
        BinarySizeMismatch: If value is too small or too big to be held by
            an unsigned 2 byte integer.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        A byte array containing the serialized integer.
    """
    return _dump_from_format(_UINT16_FORMAT, _int, endian)


def dump_int32(_int, endian=None):
    """
    Serializes a given integer as a signed 4 byte integer in binary form.
    Args:
        _int: The integer to be serialized.
        endian: The byte order of the returned byte array. Defaults to native.
    Raises:
        TypeError: If integer is not of type 'int'.
        BinarySizeMismatch: If value is too small or too big to be held by
            a signed 4 byte integer.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        A byte array containing the serialized integer.
    """
    return _dump_from_format(_INT32_FORMAT, _int, endian)


def dump_uint32(_int, endian=None):
    """
    Serializes a given integer as an unsigned 4 byte integer in binary form.
    Args:
        _int: The integer to be serialized.
        endian: The byte order of the returned byte array. Defaults to native.
    Raises:
        TypeError: If integer is not of type 'int'.
        BinarySizeMismatch: If value is too small or too big to be held by
            an unsigned 4 byte integer.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        A byte array containing the serialized integer.
    """
    return _dump_from_format(_UINT32_FORMAT, _int, endian)


def dump_int64(_int, endian=None):
    """
    Serializes a given integer as a signed 8 byte integer in binary form.
    Args:
        _int: The integer to be serialized.
        endian: The byte order of the returned byte array. Defaults to native.
    Raises:
        TypeError: If integer is not of type 'int'.
        BinarySizeMismatch: If value is too small or too big to be held by
            a signed 8 byte integer.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        A byte array containing the serialized integer.
    """
    return _dump_from_format(_INT64_FORMAT, _int, endian)


def dump_uint64(_int, endian=None):
    """
    Serializes a given integer as an unsigned 8 byte integer in binary form.
    Args:
        _int: The integer to be serialized.
        endian: The byte order of the returned byte array. Defaults to native.
    Raises:
        TypeError: If integer is not of type 'int'.
        BinarySizeMismatch: If value is too small or too big to be held by
            an unsigned 8 byte integer.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        A byte array containing the serialized integer.
    """
    return _dump_from_format(_UINT64_FORMAT, _int, endian)


def dump_float32(_float, endian=None):
    """
    Serializes a given float as a 4 byte float in binary form.
    Args:
        _float: The integer to be serialized.
        endian: The byte order of the returned byte array. Defaults to native.
    Raises:
        TypeError: If _float is not of type 'float'.
        BinarySizeMismatch: If value is too small or too big to be held by
            a 4 byte float.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        A byte array containing the serialized float.
    """
    return _dump_from_format(_FLOAT32_FORMAT, _float, endian)


def dump_float64(_float, endian=None):
    """
    Serializes a given float as an 8 byte float in binary form.
    Args:
        _float: The integer to be serialized.
        endian: The byte order of the returned byte array. Defaults to native.
    Raises:
        TypeError: If _float is not of type 'float'.
        BinarySizeMismatch: If value is too small or too big to be held by
            an 8 byte float.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        A byte array containing the serialized float.
    """
    return _dump_from_format(_FLOAT64_FORMAT, _float, endian)


def dump_bool(_bool):
    """
    Serializes a given bool as an unsigned 1 byte integer. The integers value
    will equal 1 if _bool is True, else it will equal 0.
    Args:
        _bool: The bool to be serialized.
    Raises:
        TypeError: If _bool is not of type 'bool'.
        BinaryError: If an unexpected conversion error occurs.
    Returns:
        A byte array containing the serialized bool.
    """
    if not isinstance(_bool, bool):
        raise TypeError(
            "Expected object of bool-like type, not '{0}'."
            .format(type(_bool).__name__))
    return dump_uint8(int(_bool))


_INT8_FORMAT = "b"
_UINT8_FORMAT = "B"

_INT16_FORMAT = "h"
_UINT16_FORMAT = "H"

_INT32_FORMAT = "i"
_UINT32_FORMAT = "I"

_INT64_FORMAT = "q"
_UINT64_FORMAT = "Q"

_FLOAT32_FORMAT = "f"
_FLOAT64_FORMAT = "d"

_STRUCT_ARG_OOR1 = "argument out of range"
_STRUCT_ARG_OOR2 = re.compile(
    "<= number <=")
_STRUCT_ARG_TOO_LARGE = "int too large to convert"
_STRUCT_TYPE_MISMATCH_REGEX = re.compile(
    "required argument is not (an|a) (integer|float)")


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
        if _STRUCT_TYPE_MISMATCH_REGEX.match(msg):
            raise TypeError(
                "Expected object of number-like type, not '{0}'."
                .format(type(value).__name__))
        # Hack to check if error was caused by argument out of bounds.
        elif (msg == _STRUCT_ARG_OOR1 or _STRUCT_ARG_OOR2.search(msg)
                or msg == _STRUCT_ARG_TOO_LARGE):
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
