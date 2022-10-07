import os
import unittest
from pyspedas.utilities.data_exists import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        files = pyspedas.wind.mfi(trange=['2013-11-5', '2013-11-6'], downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_load_3dp_data(self):
        tdp_vars = pyspedas.wind.threedp(trange=['2003-09-5', '2003-09-6'], notplot=True)
        self.assertTrue('N_e_dens_wi_3dp' in tdp_vars)
        tdp_vars = pyspedas.wind.threedp(datatype='3dp_elm2', trange=['2003-09-5', '2003-09-6'], notplot=True)

    def test_load_mfi_data(self):
        mfi_vars = pyspedas.wind.mfi(trange=['2013-11-5', '2013-11-6'], time_clip=True)
        self.assertTrue(data_exists('BGSE'))

    def test_load_swe_data(self):
        swe_vars = pyspedas.wind.swe(trange=['2013-11-5', '2013-11-6'])
        self.assertTrue(data_exists('N_elec'))
        self.assertTrue(data_exists('T_elec'))
        self.assertTrue(data_exists('W_elec'))

    def test_load_waves_data(self):
        swe_vars = pyspedas.wind.waves(trange=['2013-11-5', '2013-11-6'])
        self.assertTrue(data_exists('E_VOLTAGE_RAD1'))
        self.assertTrue(data_exists('E_VOLTAGE_RAD2'))
        self.assertTrue(data_exists('E_VOLTAGE_TNR'))

    def test_load_orbit_data(self):
        orb_vars = pyspedas.wind.orbit(trange=['2013-11-5', '2013-11-6'])
        self.assertTrue(data_exists('GSM_POS'))
        self.assertTrue(data_exists('GSM_VEL'))
        self.assertTrue(data_exists('SUN_VECTOR'))
        self.assertTrue(data_exists('GCI_POS'))
        self.assertTrue(data_exists('GCI_VEL'))

    def test_load_sms_data(self):
        sms_vars = pyspedas.wind.sms()
        self.assertTrue(data_exists('Alpha_vel'))
        self.assertTrue(data_exists('C/O_ratio'))
        self.assertTrue(data_exists('C_ion_temp'))
        self.assertTrue(data_exists('O_ion_temp'))


if __name__ == '__main__':
    unittest.main()
