import os
import unittest
from pytplot import data_exists, tplot_names
from pyspedas import maven
from pyspedas.maven.download_files_utilities import get_orbit_files, merge_orbit_files
import time

sleep_time=10

class OrbitTestCases(unittest.TestCase):
    def test_get_merge_orbit_files(self):
        from pyspedas.maven.config import CONFIG
        get_orbit_files()
        merge_orbit_files()
        orbfilepath = os.path.join(CONFIG['local_data_dir'],"orbitfiles", "maven_orb_rec.orb")
        self.assertTrue(os.path.exists(orbfilepath))


class LoadTestCases(unittest.TestCase):
    def test_load_kp_data(self):
        data = maven.kp()
        self.assertTrue(data_exists("mvn_kp::spacecraft::geo_x"))
        time.sleep(sleep_time)

    def test_load_kp_spdf_data(self):
        data = maven.kp(spdf=True)
        self.assertTrue(data_exists("LPW_Electron_density"))
        time.sleep(sleep_time)

    def test_load_kp_iuvs_data(self):
        data = maven.kp(iuvs=True)
        self.assertTrue(data_exists("mvn_kp::spacecraft::geo_x"))
        time.sleep(sleep_time)

    def test_load_mag_data(self):
        data = maven.mag(datatype="ss1s")
        self.assertTrue(data_exists("OB_B"))
        time.sleep(sleep_time)

    def test_load_mag_byorbit_data(self):
        data = maven.mag(trange=[500,501], datatype="ss1s")
        self.assertTrue(data_exists("OB_B"))
        time.sleep(sleep_time)

    def test_load_sta_data(self):
        data = maven.sta()
        self.assertTrue(data_exists("hkp_raw_2a-hkp"))
        self.assertTrue(data_exists("hkp_2a-hkp"))
        time.sleep(sleep_time)

    def test_load_swea_data(self):
        data = maven.swea()
        self.assertTrue(data_exists("diff_en_fluxes_svyspec"))
        time.sleep(sleep_time)

    def test_load_swia_data(self):
        data = maven.swia()
        self.assertTrue(data_exists("spectra_diff_en_fluxes_onboardsvyspec"))
        time.sleep(sleep_time)

    def test_load_sep_data(self):
        data = maven.sep()
        self.assertTrue(data_exists("f_ion_flux_tot_s2-cal-svy-full"))
        time.sleep(sleep_time)

    def test_load_lpw_data(self):
        data = maven.lpw()
        self.assertTrue(data_exists('mvn_lpw_lp_iv_l2_lpiv'))
        time.sleep(sleep_time)

    def test_load_euv_data(self):
        data = maven.euv()
        self.assertTrue(data_exists("mvn_euv_calib_bands_bands"))
        time.sleep(sleep_time)

    @unittest.skip
    def test_load_rse_data(self):
        data = maven.rse()
        self.assertTrue(data_exists(''))
        time.sleep(sleep_time)

    @unittest.skip
    def test_load_iuv_data(self):
        data = maven.iuv()
        self.assertTrue(data_exists(''))
        time.sleep(sleep_time)

    @unittest.skip
    def test_load_ngi_data(self):
        data = maven.ngi()
        self.assertTrue(data_exists(''))
        time.sleep(sleep_time)


if __name__ == "__main__":
    unittest.main()
