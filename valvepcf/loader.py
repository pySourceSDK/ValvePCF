from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import range
from builtins import next
from builtins import open
from future import standard_library
standard_library.install_aliases()

from valvepcf.structs import *
from valvepcf.classes import *
from valvepcf.constants import DEFAULT_ORDER, OPERATORS

import collections
try:
    collectionsAbc = collections.abc
except AttributeError:
    collectionsAbc = collections


def load_pcf(pcf):

    with open(pcf.source_path, 'rb') as f:
        data = PCF.parse_stream(f)

    nodes = []
    attrs = []

    tracked_strings = TrackedStrings(data.strings)

    # load elements and attributes
    for i in range(len(data.elements)):
        attrs.append(load_attributes(data.attributes[i], tracked_strings))
        nodes.append(load_element(data.elements[i], tracked_strings))

    root = nodes[0]
    load_versions(root, data)

    # make references between nodes, load their attributes
    for i in range(len(nodes)):
        if nodes[i]._type in ['DmeElement', 'DmElement']:
            load_node_systems(nodes[i], attrs[0], nodes)
        elif nodes[i]._type == 'DmeParticleChild':
            load_node_ref(nodes[i], attrs[i], nodes)
        elif nodes[i]._type == 'DmeParticleSystemDefinition':
            load_node_operators(nodes[i], attrs[i], nodes)
        load_node_attributes(nodes[i], attrs[i])

    root._unaccounted_strings = list(tracked_strings.unused)
    root._order = load_order(data, tracked_strings)

    pcf._data = data
    load_root(pcf, root)


class TrackedStrings(collectionsAbc.MutableMapping, list):
    # provides the list of parsed strings while tracking their usage
    def __init__(self, strings):
        self._strs = list(strings)
        self.unused = list(strings)

    def __getitem__(self, sid):
        if isinstance(sid, int):
            self.unused = [x for x in self.unused if x is not self._strs[sid]]
            return self._strs[sid]
        else:
            return sid


def ensure_once(itemlist, item):
    if item not in itemlist:
        itemlist.append(item)


def load_versions(node, data):
    node.binary_format = 'dmx'
    node.binary_version = data.versions[0]
    node.pcf_format = data.versions[1]
    node.pcf_version = data.versions[2]


def load_order(data, strings):
    ORDERABLE_ATTRS = ['material', 'color']
    root_order = []

    for root_attr in data.attributes[0]:
        referential = root_attr.attributeType == 15
        name = 'attributes' if not referential else 'particleSystemDefinitions'
        ensure_once(root_order, name)
    for name in [o for o in DEFAULT_ORDER if o not in OPERATORS]:
        ensure_once(root_order, name)

    element = next((x for x in data.elements if strings[x.elementType] ==
                    'DmeParticleSystemDefinition'), None)
    if not element:
        return DEFAULT_ORDER

    elem_attrs = data.attributes[data.elements.index(element)]

    order = []
    for attr in elem_attrs:
        addname = strings[attr.attributeName]
        if addname not in ORDERABLE_ATTRS and attr.attributeType not in [1, 15]:
            addname = 'attributes'

        # remove ORDERABLE_ATTRS if they are contiguous with 'attributes'
        last = order[-1] if order else None
        if last in ORDERABLE_ATTRS and addname == 'attributes':
            order = [s for s in order if s not in ORDERABLE_ATTRS]
        # skip ORDERABLE_ATTRS if they are contiguous with 'attributes'
        elif last == 'attributes' and addname in ORDERABLE_ATTRS:
            continue

        if addname == 'attributes':
            for name in root_order:
                ensure_once(order, name)
            continue

        ensure_once(order, addname)

    return order or DEFAULT_ORDER


def load_node_ref(node, nattrs, nodes):
    node.ref = next((nodes[attr._data] for attr in nattrs
                     if attr._type == 1), None)


def load_node_systems(node, nattrs, nodes):
    for attr in nattrs:
        if attr._type == 15:
            for eid in attr._data:
                node.systems.append(nodes[eid])


def load_node_operators(node, nattrs, nodes):
    for attr in [x for x in nattrs if x._type == 15 and x._name in OPERATORS]:
        for eid in attr._data:
            getattr(node, attr._name, None).append(nodes[eid])


def load_node_attributes(node, nattrs):
    node.attributes = [attr for attr in nattrs if attr._type not in [1, 15]]


TYPEMAP = {
    'DmElement': PcfRootNode,
    'DmeElement': PcfRootNode,
    'DmeParticleSystemDefinition': PcfSystemNode,
    'DmeParticleOperator': PcfOperatorNode,
    'DmeParticleChild': PcfRefNode,
}


def load_element(elem, strings):
    ename = strings[elem.elementName]
    etype = strings[elem.elementType]
    edesc = strings[elem.elementDesc]
    euuid = elem.elementUUID
    PClass = TYPEMAP[etype] if etype in TYPEMAP.keys() else PcfNode
    return PClass(ename, etype, edesc, euuid)


def load_attribute(attr, strings):
    aname = strings[attr.attributeName]
    atype = attr.attributeType
    adata = attr.attributeData
    if atype == 5:
        adata = strings[attr.attributeData]
    elif (atype >= 8 and atype <= 14) or \
            atype == 15 or atype > 22:
        adata = list(attr.attributeData)
    return PcfAttribute(aname, atype, adata)


def load_attributes(attrs, strings):
    return [load_attribute(a, strings) for a in attrs]


def load_root(pcf, root):
    pcf._name = root._name
    pcf._type = root._type
    pcf._uuid = root._uuid
    pcf._desc = root._desc

    pcf.binary_format = root.binary_format
    pcf.binary_version = root.binary_version
    pcf.pcf_format = root.pcf_format
    pcf.pcf_version = root.pcf_version

    pcf.systems = root.systems
    pcf.attributes = root.attributes

    pcf._unaccounted_strings = root._unaccounted_strings
    pcf._order = root._order
