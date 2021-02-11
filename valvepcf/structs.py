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
    5: Switch(lambda ctx: ctx._root.binary_version,
              {2: CString('ascii'),
               3: CString('ascii'),
               4: Int16ul,
               5: Int32ul}),  # ATTRIBUTE_STRING
    6: Sequence('length' / Int8ul,  # ATTRIBUTE_BINARY
                'data' / Bytes(this.length)),
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
    attribute_types[n+14] = Struct('count' / Int32sl,
                                   'array' / attribute_types[n][this.count])


def binary_version(version_string):
    version = version_string.replace('<!-- dmx encoding binary ', '')
    return int(version[0])


CDmxElement = Struct(
    'typeNameIndex' / Int16ul * "Element Type as a string dict index",
    'typeName' / Computed(lambda ctx: ctx._root.strings[ctx.typeNameIndex]),
    'elementName' / Switch(lambda ctx: ctx._root.binary_version,
                           {2: CString('ascii'),
                            3: CString('ascii'),
                            4: Int16ul,
                            5: Int16ul}) * 'Element Name as a string or a string dict index',
    'dataSignature' / Switch(lambda ctx: ctx._root.binary_version,
                             {2: Bytes(16),
                              3: Bytes(16),
                              4: Bytes(16),
                              5: Bytes(20)}) * "Globally unique identifier"
)

CDmxAttribute = Struct(
    'typeNameIndex' / Switch(this._root.binary_version,
                             {2: Int16ul,
                              3: Int16ul,
                              4: Int16ul,
                              5: Int32ul}) * 'String dictionary index',
    'typeName' / Computed(lambda ctx: ctx._root.strings[ctx.typeNameIndex]),
    'attributeType' / Int8ul,
    'attributeData' / Switch(this.attributeType, attribute_types)
)

PCF = Struct(
    'version_string' / CString('ascii'),
    'binary_version' / Computed(lambda ctx: binary_version(ctx.version_string)),
    'string_count' / Rebuild(Switch(this.binary_version,
                                    {2: Int16ul,
                                     3: Int16ul,
                                     4: Int32ul,
                                     5: Int32ul}),
                             len_(this.strings)),
    'strings' / CString('ascii')[this.string_count],
    'element_count' / Rebuild(Int32sl, len_(this.elements)),
    'elements' / CDmxElement[this.element_count],
    'element_attributes' / Struct(
        'count' / Rebuild(Int32sl, len_(this.attributes)),
        'attributes' / CDmxAttribute[this.count]
    )[this.element_count]
)
