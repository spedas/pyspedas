import os
import unittest
from pytplot import data_exists, tplot_names, del_data
from pyspedas import maven
from pyspedas.maven.download_files_utilities import get_orbit_files, merge_orbit_files
from pyspedas.maven.maven_kp_to_tplot import maven_kp_to_tplot
import time
import collections

sleep_time=10

def get_kp_dict():
    data = maven.kp()
    return maven_kp_to_tplot(filename=['maven_data/maven/data/sci/kp/insitu/2016/01/mvn_kp_insitu_20160101_v20_r01.tab',
                                       'maven_data/maven/data/sci/kp/insitu/2016/01/mvn_kp_insitu_20160102_v20_r01.tab'],
                                        notplot=True)

class OrbitTestCases(unittest.TestCase):
    def test_get_merge_orbit_files(self):
        from pyspedas.maven.config import CONFIG
        get_orbit_files()
        merge_orbit_files()
        orbfilepath = os.path.join(CONFIG['local_data_dir'],"orbitfiles", "maven_orb_rec.orb")
        self.assertTrue(os.path.exists(orbfilepath))


class LoadTestCases(unittest.TestCase):
    def test_load_kp_data(self):
        del_data('*')
        data = maven.kp()
        self.assertTrue(data_exists("mvn_kp::spacecraft::geo_x"))
        time.sleep(sleep_time)

    def test_load_kp_spdf_data(self):
        del_data('*')
        data = maven.kp(spdf=True)
        self.assertTrue(data_exists("LPW_Electron_density"))
        time.sleep(sleep_time)

    def test_load_kp_iuvs_data(self):
        del_data('*')
        data = maven.kp(iuvs=True)
        self.assertTrue(data_exists("mvn_kp::spacecraft::geo_x"))
        time.sleep(sleep_time)

    def test_kp_utilities(self):
        from pyspedas.maven.utilities import param_list, param_range, range_select, get_inst_obs_labels
        from pyspedas.maven.utilities import find_param_from_index
        kp = get_kp_dict()
        self.assertTrue(type(kp) is collections.OrderedDict)
        param_list = param_list(kp)
        self.assertTrue(len(param_list) > 0)
        print(param_list)
        param_range = param_range(kp)
        result = range_select(kp, [2440, 2445], [5], [1e9], [-1e9])
        self.assertTrue(len(result) > 0)
        result = range_select(kp, [2440, "2020/04/01"], [5], [1e9], [-1e9])
        print(len(result))
        labels = get_inst_obs_labels(kp, 'LPW.EWAVE_LOW_FREQ')
        self.assertTrue('LPW' in labels)
        self.assertTrue('EWAVE_LOW_FREQ' in labels)
        param = find_param_from_index(kp, 5)
        self.assertTrue(param == 'LPW.ELECTRON_DENSITY')

    def test_load_mag_data(self):
        del_data('*')
        data = maven.mag(datatype="ss1s")
        self.assertTrue(data_exists("OB_B"))
        time.sleep(sleep_time)

    def test_load_mag_byorbit_data(self):
        del_data('*')
        data = maven.mag(trange=[500,501], datatype="ss1s")
        self.assertTrue(data_exists("OB_B"))
        time.sleep(sleep_time)

    def test_load_sta_data(self):
        del_data('*')
        data = maven.sta()
        self.assertTrue(data_exists("hkp_raw_2a-hkp"))
        self.assertTrue(data_exists("hkp_2a-hkp"))
        time.sleep(sleep_time)

    def test_load_swea_data(self):
        del_data('*')
        data = maven.swea()
        self.assertTrue(data_exists("diff_en_fluxes_svyspec"))
        time.sleep(sleep_time)

    def test_load_swia_data(self):
        del_data('*')
        data = maven.swia()
        self.assertTrue(data_exists("spectra_diff_en_fluxes_onboardsvyspec"))
        time.sleep(sleep_time)

    def test_load_sep_data(self):
        del_data('*')
        data = maven.sep()
        self.assertTrue(data_exists("f_ion_flux_tot_s2-cal-svy-full"))
        time.sleep(sleep_time)

    def test_load_lpw_data(self):
        del_data('*')
        data = maven.lpw()
        self.assertTrue(data_exists('mvn_lpw_lp_iv_l2_lpiv'))
        time.sleep(sleep_time)

    def test_load_euv_data(self):
        del_data('*')
        data = maven.euv()
        self.assertTrue(data_exists("mvn_euv_calib_bands_bands"))
        time.sleep(sleep_time)

    @unittest.skip
    def test_load_rse_data(self):
        del_data('*')
        data = maven.rse()
        self.assertTrue(data_exists(''))
        time.sleep(sleep_time)

    @unittest.skip
    def test_load_iuv_data(self):
        del_data('*')
        data = maven.iuv()
        self.assertTrue(data_exists(''))
        time.sleep(sleep_time)

    @unittest.skip
    def test_load_ngi_data(self):
        del_data('*')
        data = maven.ngi()
        self.assertTrue(data_exists(''))
        time.sleep(sleep_time)


if __name__ == "__main__":
    unittest.main()
