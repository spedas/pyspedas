
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_fld_data(self):
        fields_vars = pyspedas.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_rtn', level='l2', time_clip=True)
        self.assertTrue(data_exists('psp_fld_l2_mag_RTN'))

    def test_load_spc_data(self):
        spc_vars = pyspedas.psp.spc(trange=['2018-11-5', '2018-11-6'], datatype='l3i', level='l3')
        self.assertTrue(data_exists('np_fit'))

    def test_load_spe_data(self):
        spe_vars = pyspedas.psp.spe(trange=['2018-11-5', '2018-11-6'], datatype='spa_sf1_32e', level='l2')
        self.assertTrue(data_exists('EFLUX'))

    def test_load_spi_data(self):
        spi_vars = pyspedas.psp.spi(trange=['2018-11-5', '2018-11-6'], datatype='spi_sf0a_mom_inst', level='l3')
        self.assertTrue(data_exists('DENS'))

    def test_load_epihi_data(self):
        epihi_vars = pyspedas.psp.epihi(trange=['2018-11-5', '2018-11-5/06:00'], datatype='let1_rates1h', level='l2')
        self.assertTrue(data_exists('B_He_Rate'))

    def test_load_epi_data(self):
        epilo_vars = pyspedas.psp.epi()
        self.assertTrue(data_exists('HET_A_Electrons_Rate_TS'))

    def test_downloadonly(self):
        files = pyspedas.psp.epilo(downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

if __name__ == '__main__':
    unittest.main()