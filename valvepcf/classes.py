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
    """
    An abstract class to represent different types of pcf elements
    and hold their collections of attributes
    """

    def __init__(self, ename, etype, edesc='', euuid=None):
        """
        :param ename: the element's name
        :type ename: str
        :param etype: the element's type
        :type etype: str
        :param edesc: the element's description
        :type edesc: str, optional
        :param euuid: the element's uuid (autogenerated if not provided)
        :type euuid: str, optional
        """

        self._type = etype  #: :type: (str) - The element's type.
        self._name = ename or 'untitled'  #: :type: (str) - The element's name.
        #: :type: (str) - The element's uuid (generally autogenerated).
        self._uuid = euuid or uuid.uuid4().bytes
        #: :type: (str) - The element's description.
        self._desc = edesc or 'DmElement'
        #: :type: (list[PcfAttribute]) - The element's list of attributes.
        self.attributes = []

    def __repr__(self, indent=0, operator=''):
        """A printable summary of the PcfNode and its child nodes.

        :returns: A Python formated string.
        :rtype: str
        """

        type_ = type(self)
        module = type_.__module__
        qualname = type_.__qualname__
        ret = "  " * indent
        ret += f"<{module}.{qualname} {operator or self._type} named" + \
            f" '{self._name}' at {hex(id(self))}>"
        return ret


class PcfRootNode(PcfNode):
    """
    PcfRootNode is the top level structure which includes a collection of
    :py:class:`PcfSystemNode<PcfSystemNode>` as well as pcf format and schema versions.
    """

    def __init__(self, ename, etype, edesc='', euuid=None):

        super().__init__(ename, etype, edesc, euuid)

        self.binary_format = 'dmx'  #: :type: (str) Always 'dmx'
        self.binary_version = 3  #: :type: (int) Ranges from 2 to 5
        self.pcf_format = 'pcf'  #: :type: (str) 'dmx' or 'pcf'
        self.pcf_version = 2  #: :type: (int) Ranges from 1 to 2

        #: :type: (list[PcfSystemNode]) List of particle systems
        self.systems = []

        self._unaccounted_strings = []
        self._order = None

    def __repr__(self, indent=0):
        ret = super().__repr__()
        for syst in self.systems:
            ret += '\n' + syst.__repr__(indent + 1)
        return ret


class PcfSystemNode(PcfNode):
    """PcfSystemNode is used to define a pcf system which regroups multiple
    :py:class:`PcfOperatorNode<PcfOperatorNode>`. Operators are separated in specialized lists."""

    def __init__(self, ename, etype, edesc='', euuid=None):
        super().__init__(ename, etype, edesc, euuid)

        #: :type: (list[PcfOperatorNode]) - list of renderers
        self.renderers = []
        #: :type: (list[PcfOperatorNode]) - list of operators
        self.operators = []
        #: :type: (list[PcfOperatorNode]) - list of initializers
        self.initializers = []
        #: :type: (list[PcfOperatorNode]) - list of emmiters
        self.emitters = []
        #: :type: (list[PcfRefNode]) - list of childrens
        self.children = []
        #: :type: (list[PcfOperatorNode]) - list of forces
        self.forces = []
        #: :type: (list[PcfOperatorNode]) - list of constraints
        self.constraints = []

    def __repr__(self, indent=0):
        ret = super().__repr__(indent)
        for c in reversed(OPERATORS):
            for node in getattr(self, c):
                ret += '\n' + node.__repr__(indent + 1, c)
        return ret


class PcfOperatorNode(PcfNode):
    """PcfOperatorNode is used to hold specific collection of attributes for
    :py:class:`PcfSystemNode<PcfSystemNode>`."""


class PcfRefNode(PcfNode):
    """PcfRefNode is used to create child relationships between particle systems."""

    def __init__(self, ename, etype, edesc='', euuid=None):
        super().__init__(ename, etype, edesc, euuid)

        #: :type: (PcfSystemNode) - reference an other system
        self.ref = None


class PcfAttribute(object):
    """
    PcfAttribute represents an attribute held by an element.
    """

    def __init__(self, name, type, data):
        """
        :param name: The attribute's name.
        :param type: The attribute's type.
        :param data: The attribute's value.
        """
        #: :type: (str) - Name of the attribute
        self._name = name
        #: :type: (int) - Ranges (1-28), defines the type of :py:attr:`_data<_data>`
        self._type = type
        #: The attribute's value, can be one of many different types, must match :py:attr:`_type<_type>`
        self._data = data
