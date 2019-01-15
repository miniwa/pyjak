# Pyjak

A Python library for reading and writing binary sources. The standard library
package `struct` has many caveats and is not very user friendly. We wrap it for
you and present a slick api with sane exception handling.

[![Build Status](https://travis-ci.org/miniwa/pyjak.svg?branch=master)](https://travis-ci.org/miniwa/pyjak)



## Examples

Heres how you would serialize a common integer:

```python
from pyjak import dump_int32
_bytes = dump_int32(1)
print(_bytes)
```

Result: (On little endian systems)

```python
b'\x01\x00\x00\x00'
```

And to turn it back into an integer:

```python
from pyjak import parse_int32
_int = parse_int32(b'\x01\x00\x00\x00')
print(_int)
```

Result: (On little endian systems)

```python
1
```

### Unsigned integers

All integer functions have unsigned versions as well. Lets say you want to fit
the number 4000000000 into a 4 byte integer. You would need the
unsigned version:

```python
from pyjak import dump_uint32
_bytes = dump_uint32(4000000000)
print(_bytes)
```

Result: (On little endian systems)

```python
b'\x00(k\xee'
```

And to turn it back into an integer:

```python
from pyjak import parse_uint32
_int = parse_uint32(b'\x00(k\xee')
print(_int)
```

Result: (On little endian systems)

```python
4000000000
```

### Byte order

As you may have noticed, we didn't need to specify the byte order
(or endianness) of the byte array. This is because all functions in
pyjak defaults to the native byte order of your system.

But you can also specify which byte order you want by using the `ByteOrder`
enumeration (except when calling int8 or uint8 functions).
The available orders are:

```python
from pyjak import ByteOrder
ByteOrder.LITTLE
ByteOrder.BIG
ByteOrder.NATIVE
print(ByteOrder.NATIVE == ByteOrder.LITTLE)
```

Result: (On little endian systems)

```python
True
```

You can specify what byte order the serialized output should have:

```python
from pyjak import dump_int32, ByteOrder
_bytes = dump_int32(1, ByteOrder.BIG)
print(_bytes)
```

Result:

```python
b'\x00\x00\x00\x01'
```

Or when parsing:

```python
from pyjak import parse_int32, ByteOrder
_int = parse_int32(b'\x00\x00\x00\x01', ByteOrder.BIG)
print(_int)
```

Result:

```python
1
```

### Booleans

You can also serialize booleans. Booleans are assumed to represented as an
unsigned 1 byte integer, where 0 means False and any other value means True.

## Supported data types

* int8 (Signed 1 byte integer)
* uint8 (Unsigned 1 byte integer)
* int16 (Signed 2 byte integer)
* uint16 (Unsigned 2 byte integer)
* int32 (Signed 4 byte integer)
* uint32 (Unsigned 4 byte integer)
* int64 (Signed 8 byte integer)
* uint64 (Unsigned 8 byte integer)
* float32 (4 byte single precision float)
* float64 (8 byte double precision float)
* bool (unsigned 1 byte integer)

## Issues

Report issues using the issue tracker on the github repo.

## Changelog

### v0.1.0

* Initial release.

## License

MIT (see LICENSE)
