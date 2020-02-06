
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_mfi_data(self):
        mam_vars = pyspedas.equator_s.mam()
        self.assertTrue(data_exists('B_xyz_gse%eq_pp_mam'))

if __name__ == '__main__':
    unittest.main()