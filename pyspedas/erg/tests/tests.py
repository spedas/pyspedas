
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_mgf_data(self):
        mgf_vars = pyspedas.erg.mgf(time_clip=True)
        self.assertTrue(data_exists('erg_mgf_l2_mag_8sec_sm'))

    def test_downloadonly(self):
        files = pyspedas.erg.mgf(downloadonly=True, trange=['2017-03-27', '2017-03-28'])
        self.assertTrue(os.path.exists(files[0]))

if __name__ == '__main__':
    unittest.main()