import struct


_INT8 = -128
_INT8_BYTES = struct.pack("=b", _INT8)

_INT16 = -32768
_INT16_BYTES = struct.pack("=h", _INT16)
_INT16_BYTES_LITTLE = struct.pack("<h", _INT16)
_INT16_BYTES_BIG = struct.pack(">h", _INT16)

_INT32 = -2147483648
_INT32_BYTES = struct.pack("=i", _INT32)
_INT32_BYTES_LITTLE = struct.pack("<i", _INT32)
_INT32_BYTES_BIG = struct.pack(">i", _INT32)

_INT64 = -9223372036854775808
_INT64_BYTES = struct.pack("=q", _INT64)
_INT64_BYTES_LITTLE = struct.pack("<q", _INT64)
_INT64_BYTES_BIG = struct.pack(">q", _INT64)

_UINT8 = 127
_UINT8_BYTES = struct.pack("=B", _UINT8)

_UINT16 = 32767
_UINT16_BYTES = struct.pack("=H", _UINT16)
_UINT16_BYTES_LITTLE = struct.pack("<H", _UINT16)
_UINT16_BYTES_BIG = struct.pack(">H", _UINT16)

_UINT32 = 2147483647
_UINT32_BYTES = struct.pack("=I", _UINT32)
_UINT32_BYTES_LITTLE = struct.pack("<I", _UINT32)
_UINT32_BYTES_BIG = struct.pack(">I", _UINT32)

_UINT64 = 9223372036854775807
_UINT64_BYTES = struct.pack("=Q", _UINT64)
_UINT64_BYTES_LITTLE = struct.pack("<Q", _UINT64)
_UINT64_BYTES_BIG = struct.pack(">Q", _UINT64)

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
