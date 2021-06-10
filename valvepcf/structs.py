from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from builtins import range
from builtins import int
from future import standard_library
standard_library.install_aliases()

from construct import *
import uuid

attribute_types = {
    1: Default(Int32sl, 0) * "ATTRIBUTE_ELEMENT",
    2: Default(Int32sl, 0) * "ATTRIBUTE_INTEGER",
    3: Default(Float32l, 0.0) * "ATTRIBUTE_FLOAT",
    4: Default(Flag, False) * "ATTRIBUTE_BOOLEAN",
    5: Default(Switch(lambda ctx: ctx._root.versions[0], {4: Int16ul, 5: Int32ul},
                      default=CString('ascii')), None) * "ATTRIBUTE_STRING",
    6: PrefixedArray(Int32ul, Byte) * "ATTRIBUTE_BINARY",
    7: Default(Float32l, 0.0) * "ATTRIBUTE_TIME",
    8: Default(Int8ul[4], [0, 0, 0, 255]) * "ATTRIBUTE_COLOR",
    9: Default(Float32l[2], [0.0, 0.0]) * "ATTRIBUTE_VECTOR2",
    10: Default(Float32l[3], [0.0, 0.0, 0.0]) * "ATTRIBUTE_VECTOR3",
    11: Default(Float32l[4], [0.0, 0.0, 0.0, 0.0]) * "ATTRIBUTE_VECTOR4",
    12: Default(Float32l[3], [0.0, 0.0, 0.0]) * "ATTRIBUTE_QANGLE",
    13: Default(Float32l[4], [0.0, 0.0, 0.0, 1.0]) * "ATTRIBUTE_QUATERNION",
    14: Float32l[4][4] * "ATTRIBUTE_MATRIX"
}

for n in range(1, 15):
    attribute_types[n + 14] = PrefixedArray(Int32ul, attribute_types[n])


def build_versions(versions):
    return "<!-- dmx encoding binary {} format {} {} -->\n".format(*versions)


def parse_versions(vstring):
    return (int(vstring[25]), vstring[34:37], int(vstring[38]))


CDmxAttribute = Struct(
    'attributeName' / Switch(this._root.versions[0], {5: Int32ul},
                             default=Int16ul) * 'String dictionary index',
    'attributeType' / Int8ul * "Determines the type of attributeData",
    'attributeData' / Switch(this.attributeType, attribute_types))

CDmxElement = Struct(
    'elementType' / Int16ul,
    'elementDesc' / If(lambda ctx: ctx._root.versions[0] == 5, Int16ul),
    'elementName' / Switch(lambda ctx: ctx._root.versions[0],
                           {4: Int16ul, 5: Int32ul}, default=CString('ascii')),
    'elementUUID' / Default(Bytes(16) * "Globally unique identifier",
                            lambda ctx: uuid.uuid4().bytes))

PCF = Struct(
    'versionString' / Rebuild(CString('ascii'),
                              lambda ctx: build_versions(ctx._root.versions)),
    'versions' / Computed(lambda ctx: parse_versions(ctx.versionString)),
    'strings' / PrefixedArray(Switch(this._root.versions[0],
                                     {4: Int32ul, 5: Int32ul},
                                     default=Int16ul), CString('ascii')),
    'elements' / PrefixedArray(Int32ul, CDmxElement),
    'attributes' / PrefixedArray(Int32ul, CDmxAttribute)[len_(this.elements)])
