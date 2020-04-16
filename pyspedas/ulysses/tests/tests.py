
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_vhm_data(self):
        data = pyspedas.ulysses.vhm()
        self.assertTrue(data_exists('B_MAG'))

    def test_load_swoops_data(self):
        data = pyspedas.ulysses.swoops()
        self.assertTrue(data_exists('Density'))
        self.assertTrue(data_exists('Temperature'))
        self.assertTrue(data_exists('Velocity'))

    def test_load_swics_data(self):
        data = pyspedas.ulysses.swics()
        self.assertTrue(data_exists('Velocity'))

    def test_load_epac_data(self):
        data = pyspedas.ulysses.epac()
        self.assertTrue(data_exists('Omni_Protons'))

    def test_load_hiscale_data(self):
        data = pyspedas.ulysses.hiscale()
        self.assertTrue(data_exists('Electrons'))
        
    def test_load_grb_data(self):
        data = pyspedas.ulysses.grb()
        self.assertTrue(data_exists('Count_Rate'))

    def test_downloadonly(self):
        files = pyspedas.ulysses.urap(downloadonly=True, trange=['2003-01-01', '2003-01-02'])
        self.assertTrue(os.path.exists(files[0]))

if __name__ == '__main__':
    unittest.main()