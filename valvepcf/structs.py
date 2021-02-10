from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from builtins import int
from builtins import range
from future import standard_library
standard_library.install_aliases()

from collections import OrderedDict

from construct import *

suggested_attribute_types = {
    0: Int32sl,  # ATTRIBUTE_ELEMENT'
    1: Int32sl,  # ATTRIBUTE_INTEGER
    2: Float32l,  # ATTRIBUTE_FLOAT
    3: Flag,  # ATTRIBUTE_BOOLEAN
    4: CString('ascii'),  # ATTRIBUTE_STRING
    5: Sequence('length' / Int8ul,
                'data' / Bytes(this.length)),  # ATTRIBUTE_BINARY
    6: Float32l,  # ATTRIBUTE_TIME
    7: Int8ul[4],  # ATTRIBUTE_COLOR
    8: Float32l[2],  # ATTRIBUTE_VECTOR2
    9: Float32l[3],  # ATTRIBUTE_VECTOR3
    10: Float32l[4],  # ATTRIBUTE_VECTOR4
    11: Float32l[3],  # ATTRIBUTE_QANGLE
    12: Float32l[4],  # ATTRIBUTE_QUATERNION
    13: Float32l[4][4]  # ATTRIBUTE_MATRIX
}


attribute_types = {
    0: Int32sl,  # ATTRIBUTE_ELEMENT
    1: Int32sl,  # ATTRIBUTE_INTEGER
    2: Int32sl,  # ATTRIBUTE_INTEGER - verified
    3: Float32l,   # ATTRIBUTE_FLOAT - verified
    4: Flag,  # ATTRIBUTE_BOOLEAN - verified
    5: CString('ascii'),  # ATTRIBUTE_STRING - verified
    6: Sequence('length' / Int8ul,
                'data' / Bytes(this.length)),  # ATTRIBUTE_BINARY
    7: Float32l,  # ATTRIBUTE_TIME
    8: Int8ul[4],  # ATTRIBUTE_COLOR - verified

    9: Float32l[2],  # ATTRIBUTE_VECTOR2
    10: Float32l[3],  # ATTRIBUTE_VECTOR3
    11: Float32l[4],  # ATTRIBUTE_VECTOR3

    12: Float32l[4],  # ATTRIBUTE_QANGLE
    13: Float32l[4],  # ATTRIBUTE_QUATERNION
    14: Float32l[4][4]  # ATTRIBUTE_MATRIX
    #15  - verified
}


for n in range(14):
    attribute_types[n+14] = Struct('count' / Int32sl,
                                   'array' / attribute_types[n][this.count])

CDmxElement = Struct(
    'typeNameIndex' / Int16ul * "Element Type as a string dict index",
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
    'typeNameIndex' / Int16ul * 'String dictionary index',
    'attributeType' / Int8ul,
    'attributeData' / Switch(this.attributeType, attribute_types)
)


def binary_version(ctx):
    version = version_string.replace('<!-- dmx encoding binary ', '')
    return int(version[0])


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
        'recount' / Computed(lambda ctx: ctx.count),
        'attributes' / CDmxAttribute[this.recount]
    )[this.element_count]
)


def structure(versions):
    if versions['binary_version'] >= 4:
        return structure_b4
    else:
        return structure_default
