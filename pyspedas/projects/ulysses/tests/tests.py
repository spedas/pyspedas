import os
import unittest
from pytplot import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_cospin_data(self):
        data = pyspedas.projects.ulysses.cospin()
        self.assertTrue(data_exists('Protons'))
        self.assertTrue(data_exists('Electrons'))
        self.assertTrue(data_exists('HiE_protons'))
        self.assertTrue(data_exists('Z_ge_3'))

    def test_load_vhm_data(self):
        data = pyspedas.projects.ulysses.vhm()
        self.assertTrue(data_exists('B_MAG'))
        data = pyspedas.projects.ulysses.vhm(notplot=True)
        self.assertTrue('B_MAG' in data)

    def test_load_swoops_data(self):
        data = pyspedas.projects.ulysses.swoops()
        self.assertTrue(data_exists('Density'))
        self.assertTrue(data_exists('Temperature'))
        self.assertTrue(data_exists('Velocity'))
        data = pyspedas.projects.ulysses.swoops(datatype='proton-moments_swoops')
        self.assertTrue(data_exists('Tpar'))
        self.assertTrue(data_exists('Tper'))
        self.assertTrue(data_exists('dens'))

    def test_load_swics_data(self):
        data = pyspedas.projects.ulysses.swics()
        self.assertTrue(data_exists('Velocity'))

    def test_load_epac_data(self):
        data = pyspedas.projects.ulysses.epac()
        self.assertTrue(data_exists('Omni_Protons'))

    def test_load_hiscale_data(self):
        data = pyspedas.projects.ulysses.hiscale()
        self.assertTrue(data_exists('Electrons'))
        
    def test_load_grb_data(self):
        data = pyspedas.projects.ulysses.grb()
        self.assertTrue(data_exists('Count_Rate'))

    def test_load_grb_data_prefix_none(self):
        data = pyspedas.projects.ulysses.grb(prefix=None)
        self.assertTrue(data_exists('Count_Rate'))

    def test_load_grb_data_suffix_none(self):
        data = pyspedas.projects.ulysses.grb(suffix=None)
        self.assertTrue(data_exists('Count_Rate'))

    def test_load_grb_data_prefix_suffix(self):
        data = pyspedas.projects.ulysses.grb(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_Count_Rate_suf'))

    def test_downloadonly(self):
        files = pyspedas.projects.ulysses.urap(downloadonly=True, trange=['2003-01-01', '2003-01-02'])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()
