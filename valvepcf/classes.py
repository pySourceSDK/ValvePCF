from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import super
from future import standard_library
standard_library.install_aliases()

import uuid

from valvepcf.constants import OPERATORS


class PcfNode(object):
    def __init__(self, ename, etype, euuid=None, edesc=''):
        self._type = etype
        self._name = ename or 'untitled'
        self._uuid = euuid or uuid.uuid4().bytes
        self._desc = edesc or 'DmElement'

        self.attributes = []

    def __repr__(self, indent=0, operator=''):
        type_ = type(self)
        module = type_.__module__
        qualname = type_.__qualname__
        ret = "  " * indent
        ret += f"<{module}.{qualname} {operator or self._type} named" + \
            f" '{self._name}' at {hex(id(self))}>"
        return ret


class PcfRoot(PcfNode):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.binary_format = 'dmx'
        self.binary_version = 3
        self.pcf_format = 'pcf'
        self.pcf_version = 2

        self.systems = []

        self._unaccounted_strings = []
        self._order = None

    def __repr__(self, indent=0):
        ret = super().__repr__()
        for syst in self.systems:
            ret += '\n' + syst.__repr__(indent + 1)
        return ret


class PcfSystem(PcfNode):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.renderers = []  # :PcfOperator
        self.operators = []  # :PcfOperator
        self.initializers = []  # :PcfOperator
        self.emitters = []  # :PcfOperator
        self.children = []  # :PcfRefNode
        self.forces = []  # :PcfOperator
        self.constraints = []  # :PcfOperator

    def __repr__(self, indent=0):
        ret = super().__repr__(indent)
        for c in reversed(OPERATORS):
            for node in getattr(self, c):
                if isinstance(node, PcfOperator):
                    continue
                ret += '\n' + node.__repr__(indent + 1, c)
        return ret


class PcfRefNode(PcfNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ref = None  # :PcfSystem


class PcfOperator(PcfNode):
    pass


class PcfAttribute(object):
    def __init__(self, name, type, data):
        self._name = name
        self._type = type

        self._data = data
