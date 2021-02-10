import os
import sys
import unittest
import tempfile
import filecmp

from valvepcf.pcf import *


class ParseBspTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.pcf_file = os.path.join(self.test_dir, 'testmap.bsp')
        return

    def tearDown(self):
        return

    def test_struct_bsp(self):
        pcf = Pcf('tests/data/test.pcf')

        self.assertTrue(True)
