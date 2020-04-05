
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        mag_files = pyspedas.goes.fgm(datatype='1min', downloadonly=True)
        self.assertTrue(os.path.exists(mag_files[0]))

    def test_load_1min_mag_data(self):
        mag_vars = pyspedas.goes.fgm(datatype='1min')
        self.assertTrue(data_exists('BX_1'))
        self.assertTrue(data_exists('BY_1'))
        self.assertTrue(data_exists('BZ_1'))

    def test_load_mag_data(self):
        mag_vars = pyspedas.goes.fgm(datatype='512ms', suffix='_512')
        self.assertTrue(data_exists('BX_1_512'))
        self.assertTrue(data_exists('BY_1_512'))
        self.assertTrue(data_exists('BZ_1_512'))

if __name__ == '__main__':
    unittest.main()