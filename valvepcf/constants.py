try:
    from __future__ import absolute_import
    from __future__ import division
    from __future__ import print_function
    from __future__ import unicode_literals

    from future import standard_library
    standard_library.install_aliases()
except ImportError:
    pass

DEFAULT_ORDER = ['renderers', 'operators', 'initializers', 'emitters',
                 'children', 'forces', 'constraints',
                 'attributes', 'particleSystemDefinitions']
OPERATORS = ['renderers', 'operators', 'initializers', 'emitters',
             'children', 'forces', 'constraints']
