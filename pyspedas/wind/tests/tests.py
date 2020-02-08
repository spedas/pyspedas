
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        files = pyspedas.wind.mfi(trange=['2013-11-5', '2013-11-6'], downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_load_mfi_data(self):
        mfi_vars = pyspedas.wind.mfi(trange=['2013-11-5', '2013-11-6'], time_clip=True)
        self.assertTrue(data_exists('BGSE'))

    def test_load_swe_data(self):
        swe_vars = pyspedas.wind.swe(trange=['2013-11-5', '2013-11-6'])
        self.assertTrue(data_exists('N_elec'))
        self.assertTrue(data_exists('T_elec'))
        self.assertTrue(data_exists('W_elec'))

if __name__ == '__main__':
    unittest.main()