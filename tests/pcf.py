import os
import sys
import unittest
import tempfile
import filecmp

from valvepcf.pcf import Pcf  # NOQA: #402


class ParseBspTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.pcf_file = os.path.join(self.test_dir, 'test.pcf')
        return

    def tearDown(self):
        return

    def test_struct_bsp(self):
        pcf = Pcf('tests/data/test.pcf')

        print(pcf.data)

        nattrs = []
        for eattrs in pcf.data.element_attributes:
            for attr in eattrs.attributes:
                if attr.attributeType not in nattrs:
                    nattrs.append(attr.attributeType)

        print(nattrs)

        self.assertTrue(True)
