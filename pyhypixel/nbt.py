import base64
import gzip
from enum import Enum
from typing import NoReturn
import struct


class TagType(Enum):
    END = 0
    BYTE = 1
    SHORT = 2
    INT = 3
    LONG = 4
    FLOAT = 5
    DOUBLE = 6
    BYTE_ARRAY = 7
    STRING = 8
    LIST = 9
    COMPOUND = 10
    INT_ARRAY = 11
    LONG_ARRAY = 12


def not_implemented(*_, **__) -> NoReturn:
    raise NotImplementedError

def parse_byte(data: bytes, index: int):
    return (struct.unpack_from("b", data, index)[0], index + 1)


def parse_short(data: bytes, index: int):
    return (struct.unpack_from(">h", data, index)[0], index + 2)


def parse_int(data: bytes, index: int):
    return (struct.unpack_from(">i", data, index)[0], index + 4)


def parse_long(data: bytes, index: int):
    return (struct.unpack_from(">l", data, index)[0], index + 8)


def parse_float(data: bytes, index: int):
    return (struct.unpack_from(">f", data, index)[0], index + 4)


def parse_double(data: bytes, index: int):
    return (struct.unpack_from(">d", data, index)[0], index + 8)


def parse_byte_array(data: bytes, index: int):
    length = struct.unpack_from(">i", data, index)[0]
    index += 4
    return (
        bytearray(data[index : index + length]),
        index + length,
    )


def parse_string(data: bytes, index: int):
    length = struct.unpack_from(">H", data, index)[0]
    index += 2
    return (data[index : index + length].decode("utf-8"), index + length)


def parse_list(data: bytes, index: int):
    tag_type = TagType(struct.unpack_from(">b", data, index)[0])
    index += 1
    length = struct.unpack_from(">i", data, index)[0]
    index += 4
    tags = []
    for _ in range(length):
        tag, index = handlers[tag_type](data, index)
        tags.append(tag)
    return (tags, index)


def parse_compound(data: bytes, index: int):
    tags = {}
    while True:
        tag_type = TagType(struct.unpack_from(">b", data, index)[0])
        index += 1
        if tag_type == TagType.END:
            return (tags, index)
        name_length = struct.unpack_from(">H", data, index)[0]
        index += 2
        name = data[index : index + name_length].decode("utf-8")
        index += name_length
        tags[name], index = handlers[tag_type](data, index)


def parse_int_array(data: bytes, index: int):
    length = struct.unpack_from(">i", data, index)[0]
    index += 4
    nums = []
    for _ in range(length):
        nums.append(struct.unpack_from(">i", data, index)[0])
        index += 4
    return (nums, index)


def parse_long_array(data: bytes, index: int):
    length = struct.unpack_from(">i", data, index)[0]
    index += 4
    nums = []
    for _ in range(length):
        nums.append(struct.unpack_from(">l", data, index)[0])
        index += 8
    return (nums, index)


handlers = {
    TagType.END: not_implemented,
    TagType.BYTE: parse_byte,
    TagType.SHORT: parse_short,
    TagType.INT: parse_int,
    TagType.LONG: parse_long,
    TagType.FLOAT: parse_float,
    TagType.DOUBLE: parse_double,
    TagType.BYTE_ARRAY: parse_byte_array,
    TagType.STRING: parse_string,
    TagType.LIST: parse_list,
    TagType.COMPOUND: parse_compound,
    TagType.INT_ARRAY: parse_int_array,
    TagType.LONG_ARRAY: parse_long_array,
}


def parse_data(data: bytes):
    decoded = base64.b64decode(data)
    unzipped = gzip.decompress(decoded)
    tag_type = TagType(struct.unpack_from(">B", unzipped)[0])
    assert tag_type == TagType.COMPOUND
    name_length = struct.unpack_from(">H", unzipped, 1)[0]
    name = unzipped[3 : 3 + name_length].decode("utf-8")
    index = 3 + name_length
    return parse_compound(unzipped, index)[0]
