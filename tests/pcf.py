import os
import sys
import unittest
import tempfile
import filecmp

from construct import *

from valvepcf.pcf import Pcf  # NOQA: #402


def cmp_file(pcf, output_path):
    pcf.save(output_path)
    identical = filecmp.cmp(pcf.source_path,
                            output_path,
                            shallow=False)
    return identical


class ParsePcfTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test.pcf')
        return

    def tearDown(self):
        return

    def test_struct_pcf(self):
        test_pcf = 'tests/data/test.pcf'
        pcf = Pcf(test_pcf)
        self.assertTrue(cmp_file(pcf, self.test_file))
