
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_mfi_data(self):
        mfi_vars = pyspedas.ace.mfi(trange=['2018-11-5', '2018-11-6'])
        self.assertTrue(data_exists('Magnitude'))

    def test_load_swe_data(self):
        swe_vars = pyspedas.ace.swe()
        self.assertTrue(data_exists('Np'))
        self.assertTrue(data_exists('Vp'))

    def test_load_epm_data(self):
        epm_vars = pyspedas.ace.epam()
        self.assertTrue(data_exists('H_lo'))
        self.assertTrue(data_exists('Ion_very_lo'))
        self.assertTrue(data_exists('Ion_mid'))
        self.assertTrue(data_exists('Electron_hi'))

    def test_load_cris_data(self):
        cris_vars = pyspedas.ace.cris()
        self.assertTrue(data_exists('flux_N'))

    def test_load_sis_data(self):
        sis_vars = pyspedas.ace.sis()
        self.assertTrue(data_exists('H_lo'))
        self.assertTrue(data_exists('H_hi'))

    def test_load_ule_data(self):
        ule_vars = pyspedas.ace.uleis()
        self.assertTrue(data_exists('H_S1'))

    def test_load_sep_data(self):
        sep_vars = pyspedas.ace.sepica()
        self.assertTrue(data_exists('H1'))
        self.assertTrue(data_exists('H2'))
        self.assertTrue(data_exists('H3'))

    def test_load_swi_data(self):
        swi_vars = pyspedas.ace.swics()
        self.assertTrue(data_exists('vHe2'))

if __name__ == '__main__':
    unittest.main()