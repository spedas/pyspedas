
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        files = pyspedas.fast.acb(trange=['1999-09-22', '1999-09-23'], time_clip=True, level='k0', downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_load_dcb_data(self):
        dcb_vars = pyspedas.fast.dcb(trange=['1999-09-22', '1999-09-23'], time_clip=True, level='k0')
        self.assertTrue(data_exists('BX'))
        self.assertTrue(data_exists('BY'))
        self.assertTrue(data_exists('BZ'))

    def test_load_acb_data(self):
        dcb_vars = pyspedas.fast.acb(trange=['1999-09-22', '1999-09-23'], time_clip=True, level='k0')
        self.assertTrue(data_exists('HF_PWR'))
        self.assertTrue(data_exists('HF_E_SPEC'))

    # as of 8 Feb 2020, these data fail to load in IDL and Python
    # def test_load_esa_data(self):
    #     esa_vars = pyspedas.fast.esa()
    #     self.assertTrue(data_exists(''))

    def test_load_teams_data(self):
        teams_vars = pyspedas.fast.teams()
        self.assertTrue(data_exists('H+'))
        self.assertTrue(data_exists('O+'))
        self.assertTrue(data_exists('He+'))

if __name__ == '__main__':
    unittest.main()