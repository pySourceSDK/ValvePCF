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


class Pcf(PcfRootNode):
    """
    This is the basic class to interact with pcf files.
    To interact with the data, consult :py:class:`PcfRootNode<PcfRootNode>`
    which this class inherits
    """

    def __init__(self, path=None):
        """
        initalize a pcf file.

        :param path: The location of the pcf file to be parsed
        :type path: str
        """
        self.source_path = path  #: :type: (str) - The location of the parsed file.
        self._data = None  # raw parsed data

        self.binary_format = None
        self.binary_version = None
        self.pcf_format = None
        self.pcf_version = None

        if self.source_path:
            load_pcf(self)

    def save(self, destination=None):
        """Saves the current instance of the Pcf. Overwrites original pcf file if no destination is provided.

        :param destination: A path (directory + filename) to determine where to save the pcf file.
        :type destination: str, optional
        """

        dest = destination or self.source_path

        save_pcf(self, dest)
