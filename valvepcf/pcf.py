from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from builtins import int
from builtins import open
from future import standard_library
standard_library.install_aliases()
from builtins import object

from valvepcf.structs import *


class Pcf(object):

    def __init__(self, path=None):
        self.source_path = path

        if self.source_path:
            with open(path, 'rb') as f:
                self.data = PCF.parse_stream(f)

    def save(self, destination=None):
        dest = destination or self.source_path

        if not dest:
            raise FileNotFoundError

        with open(dest, 'wb') as f:
            PCF.build_stream(self.data, f)
