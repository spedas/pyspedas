
import os
import unittest
from pyspedas.utilities.data_exists import data_exists
from pyspedas import maven

# class OrbitTestCases(unittest.TestCase):
#     def test_get_merge_orbit_files(self):
#         from pyspedas.maven.download_files_utilities import get_orbit_files, merge_orbit_files
#         get_orbit_files()
#         merge_orbit_files()
#         self.assertTrue(os.path.join(os.path.join(os.path.dirname(__file__), '..'), 'maven_orb_rec.orb'))

class LoadTestCases(unittest.TestCase):
    def test_load_kp_data(self):
        data = maven.kp()
        self.assertTrue(data_exists('mvn_kp::spacecraft::geo_x'))

    def test_load_mag_data(self):
        data = maven.mag()
        self.assertTrue(data_exists('OB_B'))

    def test_load_sta_data(self):
        data = maven.sta()
        self.assertTrue(data_exists('hkp_raw_2a-hkp'))
        self.assertTrue(data_exists('hkp_2a-hkp'))

    def test_load_swea_data(self):
        data = maven.swea()
        self.assertTrue(data_exists('diff_en_fluxes_svyspec'))

    def test_load_swia_data(self):
        data = maven.swia()
        self.assertTrue(data_exists('spectra_diff_en_fluxes_onboardsvyspec'))

    def test_load_sep_data(self):
        data = maven.sep()
        self.assertTrue(data_exists('f_ion_flux_tot_s2-cal-svy-full'))

    def test_load_lpw_data(self):
        data = maven.lpw()
        self.assertTrue(data_exists('mvn_lpw_lp_iv_l2_lpiv'))

    def test_load_euv_data(self):
        data = maven.euv()
        self.assertTrue(data_exists('mvn_euv_calib_bands_bands'))

    # def test_load_rse_data(self):
    #     data = maven.rse()
    #     self.assertTrue(data_exists(''))

    # def test_load_iuv_data(self):
    #     data = maven.iuv()
    #     self.assertTrue(data_exists(''))

    # def test_load_ngi_data(self):
    #     data = maven.ngi()
    #     self.assertTrue(data_exists(''))

if __name__ == '__main__':
    unittest.main()