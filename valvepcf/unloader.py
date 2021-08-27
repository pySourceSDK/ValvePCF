from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import range
from builtins import open
from builtins import next
from future import standard_library
standard_library.install_aliases()

from valvepcf.structs import *
from valvepcf.classes import *
from valvepcf.constants import OPERATORS


def save_pcf(pcf, dest):
    with open(dest, 'wb') as f:
        data = unload_pcf(pcf)
        PCF.build_stream(data, f)


def unload_pcf(pcf):
    output = {'versions': (pcf.binary_version,
                           pcf.pcf_format,
                           pcf.pcf_version),
              'strings': [],
              'elements': [],
              'attributes': []}

    relisted = []
    relisted.append(pcf)
    systems = list(pcf.systems)

    def register_elem(elem, order, elemlist=[]):

        elemlist.append(elem)

        if isinstance(elem, PcfSystemNode):
            for o in reversed([o for o in order if o in OPERATORS]):
                if o == 'children':
                    for child in elem.children:
                        elemlist = register_elem(child, order, elemlist)
                else:
                    items = getattr(elem, o, None)
                    if items:
                        elemlist = elemlist + items

        elif isinstance(elem, PcfRefNode):
            if elem.ref in systems:
                systems.remove(elem.ref)
            if elem.ref and elem.ref not in elemlist:
                elemlist = register_elem(elem.ref, order, elemlist)

        return elemlist

    while(systems):
        system = systems.pop(0)
        relisted = register_elem(system, pcf._order, relisted)

    def pcfnode_to_elem(pcfnode):
        return {'elementType': pcfnode._type,
                'elementDesc': pcfnode._desc,
                'elementName': pcfnode._name,
                'elementUUID': pcfnode._uuid}

    def new_attr(attr_name, attr_type, attr_data):
        return {'attributeName': attr_name,
                'attributeType': attr_type,
                'attributeData': attr_data}

    def pcfattr_to_attr(pcfattr):
        return new_attr(pcfattr._name, pcfattr._type, pcfattr._data)

    def ref_to_attr(node, attr_name):
        return new_attr(attr_name, 1, relisted.index(node))

    def refs_to_attr(node_list, attr_name):
        ids = [relisted.index(node) for node in node_list]
        return new_attr(attr_name, 15, ids)

    def node_attrs(node):
        nattrs = []

        list_attributes = [x for x in node.attributes if x._type >= 15]
        norm_attributes = [x for x in node.attributes if x._type < 15 and
                           x._type != 1]

        def register_attributes():
            for nattr in list_attributes:
                nattrs.append(pcfattr_to_attr(nattr))

            for nattr in norm_attributes:
                nattrs.append(pcfattr_to_attr(nattr))

        def register_root():
            attrs_types = list(pcf._order)

            for a_t in attrs_types:
                if a_t == 'attributes':
                    register_attributes()
                elif a_t == 'particleSystemDefinitions':
                    nattrs.append(refs_to_attr(node.systems,
                                               'particleSystemDefinitions'))

        def register_children():
            attrs_types = list(pcf._order)
            for a_t in attrs_types:
                if a_t == 'attributes':
                    register_attributes()
                elif a_t == 'children' and node.ref:
                    nattrs.append(ref_to_attr(node.ref, 'child'))

        def register_system_node():
            attrs_types = list(pcf._order)

            if 'material' in attrs_types:
                material_attr = next(
                    (x for x in norm_attributes if x._name == 'material'), None)
                if material_attr:
                    norm_attributes.remove(material_attr)
            if 'color' in attrs_types:
                color_attr = next(
                    (x for x in norm_attributes if x._name == 'color'), None)
                if color_attr:
                    norm_attributes.remove(color_attr)

            for a_t in attrs_types:
                # we golfin bois!
                if a_t == 'material' and material_attr:
                    nattrs.append(pcfattr_to_attr(material_attr))
                if a_t == 'color' and color_attr:
                    nattrs.append(pcfattr_to_attr(color_attr))
                if a_t == 'attributes':
                    register_attributes()
                else:
                    d = getattr(node, a_t, None)
                    if d != None and a_t in pcf._data.strings:
                        nattrs.append(refs_to_attr(d, a_t))

        if isinstance(node, PcfSystemNode):
            register_system_node()
        elif isinstance(node, PcfRootNode):
            register_root()
        elif isinstance(node, PcfRefNode):
            register_children()
        else:
            register_attributes()

        return nattrs

    def register_string(pcf_string, minver=0):
        # Register a string
        if isinstance(pcf_string, int):
            return pcf_string
        if pcf.binary_version >= minver:
            if pcf_string not in output['strings']:
                output['strings'].append(pcf_string)
                if pcf_string in ['functionName', 'child'] and \
                   'type_dictionary' in pcf._unaccounted_strings:
                    # dont' know what this string is about, but it's always there
                    register_string('type_dictionary')
            return output['strings'].index(pcf_string)
        else:
            return pcf_string

    def register_element_strings(elem):
        # Register strings of an element
        elem['elementType'] = register_string(elem['elementType'])
        elem['elementDesc'] = register_string(elem['elementDesc'], 5)
        elem['elementName'] = register_string(elem['elementName'], 4)

    def register_attribute_strings(attr):
        # Register strings of an attribute
        attr['attributeName'] = register_string(attr['attributeName'])
        if (attr['attributeType'] == 5):
            attr['attributeData'] = register_string(attr['attributeData'], 4)

    for nodeid in range(len(relisted)):

        # make element
        n_elem = pcfnode_to_elem(relisted[nodeid])
        output['elements'].append(n_elem)
        register_element_strings(n_elem)

        # make attributes
        n_attrs = node_attrs(relisted[nodeid])
        output['attributes'].append(n_attrs)
        for attr in reversed(n_attrs):
            register_attribute_strings(attr)

        # additional garbo
        if nodeid == 0 and 'name' in pcf._unaccounted_strings:
            register_string('name')

    if 'type_dictionary' in pcf._unaccounted_strings and pcf.binary_version < 4:
        register_string('type_dictionary')

    return output
