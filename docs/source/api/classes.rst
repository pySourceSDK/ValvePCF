Pcf Classes (How it all goes together)
======================================

A pcf file is a collection of elements. Each element has a collection of Attributes. Here are the classes used to represent the various element types and their attributes.

Representing pcf elements
###########################

.. autoclass:: valvepcf.PcfNode
   :special-members: __init__, __repr__
   :inherited-members:
   :private-members:

.. autoclass:: valvepcf.PcfRootNode
   :special-members: __init__
   :inherited-members:
   :show-inheritance:

.. autoclass:: valvepcf.PcfSystemNode
   :special-members: __init__
   :inherited-members:
   :show-inheritance:

.. autoclass:: valvepcf.PcfOperatorNode
   :special-members: __init__
   :inherited-members:
   :show-inheritance:

.. autoclass:: valvepcf.PcfRefNode
   :special-members: __init__
   :inherited-members:
   :show-inheritance:


Representing pcf attributes
###########################

.. autoclass:: valvepcf.PcfAttribute
   :special-members: __init__
   :private-members:
   :inherited-members:
