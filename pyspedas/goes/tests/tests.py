
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        mag_files = pyspedas.goes.fgm(datatype='1min', downloadonly=True)
        self.assertTrue(os.path.exists(mag_files[0]))

    def test_load_orbit_data(self):
        mag_vars = pyspedas.goes.orbit()
        self.assertTrue(data_exists('XYZ_GSM'))
        self.assertTrue(data_exists('XYZ_GSE'))
        self.assertTrue(data_exists('XYZ_SM'))
        self.assertTrue(data_exists('XYZ_GEO'))

    def test_load_1min_mag_data(self):
        mag_vars = pyspedas.goes.fgm(datatype='1min')
        self.assertTrue(data_exists('BX_1'))
        self.assertTrue(data_exists('BY_1'))
        self.assertTrue(data_exists('BZ_1'))

    def test_load_5min_mag_data(self):
        mag_vars = pyspedas.goes.fgm(datatype='5min')
        self.assertTrue(data_exists('BX_1'))
        self.assertTrue(data_exists('BY_1'))
        self.assertTrue(data_exists('BZ_1'))

    def test_load_mag_data(self):
        mag_vars = pyspedas.goes.fgm(datatype='512ms', suffix='_512')
        self.assertTrue(data_exists('BX_1_512'))
        self.assertTrue(data_exists('BY_1_512'))
        self.assertTrue(data_exists('BZ_1_512'))

    def test_load_1min_epead_data(self):
        epead_vars = pyspedas.goes.epead()
        self.assertTrue(data_exists('E1E_UNCOR_FLUX'))
        self.assertTrue(data_exists('E1W_UNCOR_FLUX'))
        self.assertTrue(data_exists('E2E_UNCOR_FLUX'))

    def test_load_full_epead_data(self):
        epead_vars = pyspedas.goes.epead(datatype='full')
        self.assertTrue(data_exists('E1E_UNCOR_FLUX'))
        self.assertTrue(data_exists('E1W_UNCOR_FLUX'))
        self.assertTrue(data_exists('E2E_UNCOR_FLUX'))

    def test_load_5min_epead_data(self):
        epead_vars = pyspedas.goes.epead(datatype='5min')
        self.assertTrue(data_exists('E1E_UNCOR_FLUX'))
        self.assertTrue(data_exists('E1W_UNCOR_FLUX'))
        self.assertTrue(data_exists('E2E_UNCOR_FLUX'))

    def test_load_full_maged_data(self):
        maged_vars = pyspedas.goes.maged(datatype='full')
        self.assertTrue(data_exists('M_1ME1_DTC_UNCOR_CR'))

    def test_load_1min_maged_data(self):
        maged_vars = pyspedas.goes.maged(time_clip=True)
        self.assertTrue(data_exists('M_1ME1_DTC_UNCOR_FLUX'))

    def test_load_5min_maged_data(self):
        maged_vars = pyspedas.goes.maged(datatype='5min')
        self.assertTrue(data_exists('M_1ME1_DTC_UNCOR_FLUX'))

    def test_load_full_magpd_data(self):
        magpd_vars = pyspedas.goes.magpd(datatype='full')
        self.assertTrue(data_exists('M_1MP1_DTC_UNCOR_CR'))

    def test_load_1min_magpd_data(self):
        magpd_vars = pyspedas.goes.magpd()
        self.assertTrue(data_exists('M_1MP1_DTC_UNCOR_FLUX'))

    def test_load_5min_magpd_data(self):
        magpd_vars = pyspedas.goes.magpd(datatype='5min')
        self.assertTrue(data_exists('M_1MP1_DTC_UNCOR_FLUX'))

    def test_load_full_hepad_data(self):
        hepad_vars = pyspedas.goes.hepad(datatype='full')
        self.assertTrue(data_exists('P10_FLUX'))

    def test_load_1min_hepad_data(self):
        hepad_vars = pyspedas.goes.hepad()
        self.assertTrue(data_exists('P10_FLUX'))

    def test_load_5min_hepad_data(self):
        hepad_vars = pyspedas.goes.hepad(datatype='5min')
        self.assertTrue(data_exists('P10_FLUX'))

    def test_load_xrs_data(self):
        xrs_vars = pyspedas.goes.xrs()
        self.assertTrue(data_exists('A_AVG'))
        xrs_vars = pyspedas.goes.xrs(datatype='5min', trange=['2000-09-01', '2000-09-01'])
        xrs_vars = pyspedas.goes.xrs(datatype='2s')

    def test_load_eps_data(self):
        eps_vars = pyspedas.goes.eps(trange=['2000-09-01', '2000-09-01'], probe='11')
        eps_vars = pyspedas.goes.eps(trange=['2000-09-01', '2000-09-01'], probe='11', datatype='5min')
        self.assertTrue(data_exists('e1_flux_i'))
        self.assertTrue(data_exists('e2_flux_i'))
        self.assertTrue(data_exists('e3_flux_i'))
        self.assertTrue(data_exists('p1_flux'))
        self.assertTrue(data_exists('p2_flux'))
        self.assertTrue(data_exists('p3_flux'))
        self.assertTrue(data_exists('p4_flux'))
        self.assertTrue(data_exists('p5_flux'))
        self.assertTrue(data_exists('p6_flux'))
        self.assertTrue(data_exists('p7_flux'))


if __name__ == '__main__':
    unittest.main()