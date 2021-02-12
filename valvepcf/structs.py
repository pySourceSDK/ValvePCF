from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from builtins import int
from builtins import range
from future import standard_library
standard_library.install_aliases()

from construct import *

attribute_types = {
    1: Int32sl,  # ATTRIBUTE_ELEMENT
    2: Int32sl,  # ATTRIBUTE_INTEGER
    3: Float32l,   # ATTRIBUTE_FLOAT
    4: Flag,  # ATTRIBUTE_BOOLEAN
    5: Switch(lambda ctx: ctx._root.versions[0], {4: Int16ul, 5: Int32ul},
              default=CString('ascii')),  # ATTRIBUTE_STRING
    6: PrefixedArray(Int8ul, Byte),  # ATTRIBUTE_BINARY
    7: Float32l,  # ATTRIBUTE_TIME
    8: Int8ul[4],  # ATTRIBUTE_COLOR
    9: Float32l[2],  # ATTRIBUTE_VECTOR2
    10: Float32l[3],  # ATTRIBUTE_VECTOR3
    11: Float32l[4],  # ATTRIBUTE_VECTOR4
    12: Float32l[4],  # ATTRIBUTE_QANGLE
    13: Float32l[4],  # ATTRIBUTE_QUATERNION
    14: Float32l[4][4]  # ATTRIBUTE_MATRIX
}

for n in range(1, 15):
    attribute_types[n + 14] = PrefixedArray(Int32sl, attribute_types[n])


def build_versions(versions):
    return "<!-- dmx encoding binary {} format {} {} -->\n".format(*versions)


def parse_versions(vstring):
    return (int(vstring[25]), vstring[34:37], int(vstring[38]))


CDmxAttribute = Struct(
    'typeNameIndex' / Switch(this._root.versions[0], {5: Int32ul},
                             default=Int16ul) * 'String dictionary index',
    'attributeType' / Int8ul,
    'attributeData' / Switch(this.attributeType, attribute_types))

CDmxElement = Struct(
    'typeNameIndex' / Int16ul,
    'elementName' / Switch(lambda ctx: ctx._root.versions[0], {4: Int16ul, 5: Int16ul},
                           default=CString('ascii')),
    'dataSignature' / Switch(lambda ctx: ctx._root.versions[0], {5: Bytes(20)},
                             default=Bytes(16)) * "Globally unique identifier")

PCF = Struct(
    'version_string' / Rebuild(CString('ascii'),
                               lambda ctx: build_versions(ctx.versions)),
    'versions' / Computed(lambda ctx: parse_versions(ctx.version_string)),
    'strings' / PrefixedArray(Switch(this._root.versions[0],
                                     {4: Int32ul, 5: Int32ul},
                                     default=Int16ul), CString('ascii')),
    'elements' / PrefixedArray(Int32sl, CDmxElement),
    'attributes' / PrefixedArray(Int32sl, CDmxAttribute)[len_(this.elements)])
