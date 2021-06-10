from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import open
from future import standard_library
standard_library.install_aliases()

from valvepcf.classes import *
from valvepcf.loader import load_pcf
from valvepcf.unloader import unload_pcf, save_pcf


class Pcf(PcfRoot):

    def __init__(self, origin=None):
        self.source_path = origin
        self._data = None  # raw parsed data

        self.binary_format = None
        self.binary_version = None
        self.pcf_format = None
        self.pcf_version = None

        if self.source_path:
            load_pcf(self)

    def save(self, destination=None):
        dest = destination or self.source_path

        try:
            d = open(dest, 'wb+')
        except:
            raise FileNotFoundError

        save_pcf(self, dest)
