import os
import importlib
import unittest
from unittest.mock import MagicMock, patch
from pyspedas.tplot_tools import data_exists, tplot_names, del_data
from pyspedas.projects import maven
from pyspedas.projects.maven.download_files_utilities import get_orbit_files, merge_orbit_files, get_file_from_site
from pyspedas.projects.maven.maven_load import maven_filenames
from pyspedas.projects.maven.maven_kp_to_tplot import maven_kp_to_tplot
from pyspedas.projects.maven.utilities import get_latest_iuvs_files_from_date_range
import time
import collections
from pyspedas.projects.maven.config import CONFIG
from datetime import datetime

# We need sleep time to avoid "HTTP Error 429: Too Many Requests"
# As of January 2025, this may no longer be necessary for MAVEN
sleep_time = 1
maven_load_module = importlib.import_module("pyspedas.projects.maven.maven_load")


def get_kp_dict():
    data = maven.kp()
    local_data_dir = CONFIG["local_data_dir"]
    # These paths frequently need to be updated to match the server responses.
    # Maybe we could wild them somehow, without getting confused if multiple versions are present
    # in the data directory from previous downloads?
    fn = [
        os.path.join(
            local_data_dir,
            "maven/data/sci/kp/insitu/2016/01/mvn_kp_insitu_20160101_v26_r01.tab",
        ),
        os.path.join(
            local_data_dir,
            "maven/data/sci/kp/insitu/2016/01/mvn_kp_insitu_20160102_v26_r01.tab",
        ),
    ]
    return maven_kp_to_tplot(filename=fn, notplot=True)


class OrbitTestCases(unittest.TestCase):
    def test_get_merge_orbit_files(self):
        from pyspedas.projects.maven.config import CONFIG

        get_orbit_files()
        merge_orbit_files()
        orbfilepath = os.path.join(
            CONFIG["local_data_dir"], "orbitfiles", "merged_maven_orbits.orb"
        )
        self.assertTrue(os.path.exists(orbfilepath))


class DownloadFileTestCases(unittest.TestCase):
    def test_instrument_loaders_forward_load_kp(self):
        loader_names = [
            "euv",
            "iuv",
            "lpw",
            "mag",
            "ngi",
            "rse",
            "sep",
            "sta",
            "swea",
            "swia",
        ]

        for loader_name in loader_names:
            with self.subTest(loader=loader_name):
                module = importlib.import_module(
                    f"pyspedas.projects.maven.{loader_name}"
                )
                mock_load = MagicMock()
                with patch.dict(module.__dict__, {"maven_load": mock_load}):
                    getattr(module, loader_name)(load_kp=False)

                self.assertFalse(mock_load.call_args.kwargs["load_kp"])

    @patch.object(maven_load_module, "get_filenames")
    def test_maven_filenames_loads_kp_by_default(self, mock_get_filenames):
        mock_get_filenames.side_effect = [
            "mvn_mag_l2_2016001ss1s_20160101_v01_r01.cdf",
            "mvn_kp_insitu_20160101_v01_r01.tab",
        ]

        files = maven_filenames(instruments=["mag"], local_dir="maven_data")

        self.assertEqual(set(files), {"mag", "kp"})
        self.assertEqual(mock_get_filenames.call_count, 2)
        self.assertIn("instrument=kp", mock_get_filenames.call_args_list[1].args[0])

    @patch.object(maven_load_module, "get_filenames")
    def test_maven_filenames_can_skip_kp(self, mock_get_filenames):
        mock_get_filenames.return_value = (
            "mvn_mag_l2_2016001ss1s_20160101_v01_r01.cdf"
        )

        files = maven_filenames(
            instruments=["mag"],
            local_dir="maven_data",
            load_kp=False,
        )

        self.assertEqual(set(files), {"mag"})
        mock_get_filenames.assert_called_once()
        self.assertNotIn("instrument=kp", mock_get_filenames.call_args.args[0])

    @patch.object(maven_load_module, "get_filenames")
    def test_maven_iuvs_filenames_include_insitu_kp(self, mock_get_filenames):
        mock_get_filenames.side_effect = [
            "mvn_kp_iuvs_periapse_20150307_v01_r01.tab",
            "mvn_kp_insitu_20150307_v01_r01.tab",
        ]

        files = maven_filenames(
            level="kp",
            insitu=True,
            iuvs=True,
            local_dir="maven_data",
        )

        self.assertEqual(mock_get_filenames.call_count, 2)
        iuvs_query = mock_get_filenames.call_args_list[0].args[0]
        insitu_query = mock_get_filenames.call_args_list[1].args[0]
        self.assertIn("level=iuvs", iuvs_query)
        self.assertIn("level=insitu", insitu_query)
        self.assertEqual(len(files["kp"]), 6)

    @patch.object(maven_load_module, "get_filenames")
    def test_maven_iuvs_filenames_can_exclude_insitu_kp(self, mock_get_filenames):
        mock_get_filenames.return_value = (
            "mvn_kp_iuvs_periapse_20150307_v01_r01.tab"
        )

        files = maven_filenames(
            level="kp",
            insitu=False,
            iuvs=True,
            local_dir="maven_data",
        )

        mock_get_filenames.assert_called_once()
        self.assertIn("level=iuvs", mock_get_filenames.call_args.args[0])
        self.assertEqual(len(files["kp"]), 3)

    @patch("pyspedas.projects.maven.download_files_utilities.download")
    def test_get_file_from_public_site(self, mock_download):
        filename = "mvn_mag_l2_20200101_v01_r01.cdf"

        get_file_from_site(filename, public=True, data_dir="maven_data")

        mock_download.assert_called_once_with(
            remote_file=(
                "https://lasp.colorado.edu/maven/sdc/public/files/api/v1/"
                "search/science/fn_metadata/download?file=" + filename
            ),
            local_path="maven_data",
            local_file=filename,
            no_wildcards=True,
            force_download=True,
        )

    @patch("pyspedas.projects.maven.download_files_utilities.download")
    def test_get_file_from_private_site(self, mock_download):
        filename = "mvn_mag_l2_20200101_v01_r01.cdf"
        credentials = {
            "maven_username": "test-user",
            "maven_password": "test-password",
        }

        with patch.dict(CONFIG, credentials):
            get_file_from_site(filename, public=False, data_dir="maven_data")

        mock_download.assert_called_once_with(
            remote_file=(
                "https://lasp.colorado.edu/maven/sdc/service/files/api/v1/"
                "search/science/fn_metadata/download?file=" + filename
            ),
            local_path="maven_data",
            local_file=filename,
            no_wildcards=True,
            force_download=True,
            username="test-user",
            password="test-password",
            basic_auth=True,
        )


class LoadTestCases(unittest.TestCase):
    def test_load_kp_data(self):
        del_data("*")
        data = maven.kp()
        self.assertTrue(data_exists("mvn_kp::spacecraft::geo_x"))
        time.sleep(sleep_time)

    def test_load_kp_spdf_data(self):
        del_data("*")
        data = maven.kp(spdf=True)
        self.assertTrue(data_exists("LPW_Electron_density"))
        time.sleep(sleep_time)

    def test_load_kp_iuvs_occ_data(self):
        del_data("*")
        data = maven.kp(trange=["2016-01-18","2016-01-19"],iuvs=True)
        self.assertTrue(data_exists("mvn_kp::spacecraft::geo_x"))
        dt1 = datetime.strptime("2016-01-18", "%Y-%m-%d")
        dt2 = datetime.strptime("2016-01-19", "%Y-%m-%d")
        fnames = get_latest_iuvs_files_from_date_range(dt1,dt2)
        self.assertTrue(len(fnames) > 0)
        self.assertTrue("mvn_kp_iuvs_occ-02533_20160118T125134_v13_r01.tab" in fnames[0])
        time.sleep(sleep_time)

    def test_load_kp_iuvs_periapse_data(self):
        del_data("*")
        data = maven.kp(trange=["2015-03-07","2015-03-08"],iuvs=True)
        self.assertTrue(data_exists("mvn_kp::spacecraft::geo_x"))
        dt1 = datetime.strptime("2015-03-07", "%Y-%m-%d")
        dt2 = datetime.strptime("2015-03-08", "%Y-%m-%d")
        # fnames = get_latest_iuvs_files_from_date_range(dt1,dt2)
        # print(fnames)
        #self.assertTrue(len(fnames) > 0)
        #self.assertTrue("mvn_kp_iuvs_00850_20150308T221253_v13_r01.tab" in fnames[0])
        time.sleep(sleep_time)

    def test_load_kp_iuvs_corona_data(self):
        del_data("*")
        data = maven.kp(trange=["2016-01-14","2016-01-15"],iuvs=True)
        self.assertTrue(data_exists("mvn_kp::spacecraft::geo_x"))
        dt1 = datetime.strptime("2016-01-07", "%Y-%m-%d")
        dt2 = datetime.strptime("2016-01-08", "%Y-%m-%d")
        # fnames = get_latest_iuvs_files_from_date_range(dt1,dt2)
        # print(fnames)
        #self.assertTrue(len(fnames) > 0)
        #self.assertTrue("mvn_kp_iuvs_00850_20150308T221253_v13_r01.tab" in fnames[0])
        time.sleep(sleep_time)

    def test_kp_param_errors(self):
        from pyspedas.projects.maven.kp_utilities import param_list, param_range, range_select
        # bad value in kp dict
        kp = {}
        kp["foo"] = "bar"
        with self.assertLogs(level="WARNING") as log:
            param_list = param_list(kp)
            self.assertTrue("unexpected value type" in log.output[0])
        kp_insitu = {}
        kp_iuvs = {}
        kp_insitu["TimeString"] = ["1970-01-01", "1970-01-02"]
        kp_insitu["Orbit"] = [0,1]
        param_range(kp_insitu)

        kp_iuvs["TimeString"] = ["1971-01-01", "1971-01-02"]
        kp_iuvs["Orbit"] = [10, 11]
        with self.assertLogs(level="WARNING") as log:
            param_range(kp_insitu, kp_iuvs)
            self.assertTrue("No overlap" in log.output[0])

        with self.assertLogs(level="WARNING") as log:
            range_select(kp_iuvs)
            self.assertTrue("*****ERROR*****" in log.output[0])
            i = len(log.output)
            range_select(kp_iuvs,parameter=0)
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            range_select(kp_iuvs,time=["1970-01-01"])
            i = len(log.output)
            range_select(kp_iuvs, time=["1970-01-01", 0])
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)

    def test_kp_utilities(self):
        from pyspedas.projects.maven.kp_utilities import (
            param_list,
            param_range,
            range_select,
            get_inst_obs_labels,
        )
        from pyspedas.projects.maven.kp_utilities import find_param_from_index

        kp = get_kp_dict()
        self.assertTrue(type(kp) is collections.OrderedDict)

        param_list = param_list(kp)
        self.assertTrue(len(param_list) > 0)
        print(param_list)

        param_range = param_range(kp)
        result = range_select(kp, [2440, 2445], [5], [1e9], [-1e9])
        self.assertTrue(len(result) > 0)
        result = range_select(kp, ["2016-01-01 00:00:00","2016-01-02 00:00:00"], [5], [1e9], [-1e9])
        self.assertTrue(len(result) > 0)
        labels = get_inst_obs_labels(kp, "LPW.EWAVE_LOW_FREQ")
        self.assertTrue("LPW" in labels)
        self.assertTrue("EWAVE_LOW_FREQ" in labels)
        param = find_param_from_index(kp, 5)
        self.assertTrue(param == "LPW.ELECTRON_DENSITY")
        # no min
        result = range_select(kp, ["2016-01-01 00:00:00","2016-01-02 00:00:00"], parameter=[5], maximum=[1e9])
        self.assertTrue(len(result) > 0)
        # no max
        result = range_select(kp, ["2016-01-01 00:00:00","2016-01-02 00:00:00"], parameter=[5], minimum=[1e9])
        self.assertTrue(len(result) > 0)
        # no time, param as list with int
        result = range_select(kp, parameter=[5], minimum=[-1e9], maximum=[1e9])
        # no time, param as list with int
        result = range_select(kp, parameter=[5], minimum=[-1e9], maximum=[1e9])
        self.assertTrue(len(result) > 0)
        # no time, param as list with string
        result = range_select(kp, parameter=["LPW.ELECTRON_DENSITY"], minimum=[-1e9], maximum=[1e9])
        self.assertTrue(len(result) > 0)
        # no time, param as list with string and int
        result = range_select(kp, parameter=["LPW.ELECTRON_DENSITY",6], minimum=[-1e9, -1e9], maximum=[1e9,1e9])
        self.assertTrue(len(result) > 0)
        # no time, parameter as scalar int
        result = range_select(kp, parameter=5, minimum=[-1e9], maximum=[1e9])
        self.assertTrue(len(result) > 0)
        # no time, parameter as scalar string
        result = range_select(kp, parameter="LPW.ELECTRON_DENSITY", minimum=[-1e9], maximum=[1e9])
        self.assertTrue(len(result) > 0)
        # no time, parameter, min, max as scalars
        result = range_select(kp, parameter="LPW.ELECTRON_DENSITY", minimum=-1e9, maximum=1e9)
        self.assertTrue(len(result) > 0)
        # no time, scalar param, minimum=None
        result = range_select(kp, parameter=5, maximum=[1e9])
        self.assertTrue(len(result) > 0)
        # no time, scalar param, maximum=None
        result = range_select(kp, parameter=5, maximum=[1e9])
        self.assertTrue(len(result) > 0)
        # times, scalar param, scalar max/min
        result = range_select(kp, time=[2440,2441], parameter=5, minimum=-1e9, maximum=[1e9])
        self.assertTrue(len(result) > 0)
        # times, scalar param, no min
        result = range_select(kp, time=[2440, 2441], parameter=5, maximum=[1e9])
        # times, scalar param, no max
        result = range_select(kp, time=[2440, 2441], parameter=5, minimum = [1e9])

        with self.assertLogs(level="WARNING") as log:
            # mismatched time types
            result = range_select(kp, [2440, "2020/04/01"], [5], [1e9], [-1e9])
            self.assertTrue("*****WARNING*****" in log.output[0])
            i = len(log.output)
            # only one time
            result = range_select(kp, [2440], [5], [1e9], [-1e9])
            self.assertTrue("*****WARNING*****" in log.output[i])
            i = len(log.output)
            # parameter but no max/min
            result = range_select(kp, ["2016-01-01 00:00:00","2016-01-02 00:00:00"], parameter=[5])
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # len(min) doesn't match param
            result = range_select(kp, ["2016-01-01 00:00:00","2016-01-02 00:00:00"], parameter=[5], minimum=[-1e9,-1e9], maximum=[1e9])
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # len(max) doesn't match param
            result = range_select(kp, ["2016-01-01 00:00:00","2016-01-02 00:00:00"], parameter=[5], minimum=[-1e9], maximum=[1e9, 1e9])
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            self.assertTrue(len(result) > 0)
            # len(min) doesn't match param, no max
            result = range_select(kp, ["2016-01-01 00:00:00","2016-01-02 00:00:00"], parameter=[5], minimum=[-1e9,-1e9])
            self.assertTrue(len(result) > 0)
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # len(max) doesn't match param, no min
            result = range_select(kp, ["2016-01-01 00:00:00","2016-01-02 00:00:00"], parameter=[5], maximum=[1e9, 1e9])
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # no time, param as list with string, int, and float
            result = range_select(kp, parameter=["LPW.ELECTRON_DENSITY", 6, 1.2], minimum=[-1e9, -1e9, -1e9], maximum=[1e9, 1e9, 1e9])
            self.assertTrue(len(result) > 0)
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # no time, param as scalar float
            result = range_select(kp, parameter=1.2, minimum=[-1e9], maximum=[1e9])
            self.assertTrue(len(result) > 0)
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # no time, no param
            result = range_select(kp, minimum=[-1e9], maximum=[1e9])
            self.assertTrue(len(result) > 0)
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # no time, scalar param, no bounds
            result = range_select(kp, parameter=5)
            self.assertTrue(len(result) > 0)
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # no time, len(min) doesn't match param
            result = range_select(kp, parameter=[5], minimum=[-1e9,-1e9], maximum=[1e9])
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # no time, len(max) doesn't match param
            result = range_select(kp,  parameter=[5], minimum=[-1e9], maximum=[1e9, 1e9])
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            self.assertTrue(len(result) > 0)
            # no time, len(min) doesn't match param, no max
            result = range_select(kp,  parameter=[5], minimum=[-1e9,-1e9])
            self.assertTrue(len(result) > 0)
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # no time, len(max) doesn't match param, no min
            result = range_select(kp, parameter=[5], maximum=[1e9, 1e9])
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # only one time, no param
            result = range_select(kp, [2440])
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # Malformed times, no parameter
            result = range_select(kp, [{}, {}])
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # Malformed times, parameter given
            result = range_select(kp, [{}, {}], parameter=[5], minimum=[-1e9], maximum=[1e9])
            self.assertTrue("*****WARNING*****" in log.output[i])
            i = len(log.output)
            # times, scalar param, len(min) doesn't match param
            result = range_select(kp, time=[2440, 2441], parameter=5, minimum=[-1e9, -1e9], maximum=[1e9])
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # times, scalar param, len(max) doesn't match param
            result = range_select(kp, time=[2440, 2441], parameter=5, minimum=[-1e9], maximum=[1e9, 1e9])
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # times, scalar param, no bounds
            result = range_select(kp, time=[2440, 2441], parameter=5)
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # invalid parameter value
            a,b = get_inst_obs_labels(kp, "foo")
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # too many components
            a,b = get_inst_obs_labels(kp, "foo.bar.baz")
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)
            # Invalid numeric index
            ind = find_param_from_index(kp,999)
            self.assertTrue("*****ERROR*****" in log.output[i])
            i = len(log.output)

    def test_get_file_from_site_private(self):
        f = 'mvn_mag_l2_2016002ss1s_20160102_v01_r01.xml'
        public=False
        full_path='maven_data/maven/data/sci/mag/l2/2016/01'
        # We don't have credentials to the private site yet, so this will fail.
        try:
            get_file_from_site(f, public, full_path)
        except Exception as e:
            pass

    def test_load_mag_data(self):
        from pyspedas.projects.maven.utilities import get_l2_files_from_date

        del_data("*")
        data = maven.mag(datatype="ss1s")
        self.assertTrue(len(tplot_names("OB_B*"))>0)
        self.assertTrue(data_exists("mvn_kp::spacecraft::altitude"))
        dt = datetime.strptime("2016-01-01/12:00:00", "%Y-%m-%d/%H:%M:%S")
        files = get_l2_files_from_date(dt, "mag")
        self.assertTrue(len(files) > 0)
        time.sleep(sleep_time)

    def test_load_mag_data_without_kp(self):
        del_data("*")
        maven.mag(datatype="ss1s", load_kp=False)
        self.assertTrue(len(tplot_names("OB_B*")) > 0)
        self.assertFalse(data_exists("mvn_kp::spacecraft::altitude"))
        time.sleep(sleep_time)

    def test_load_mag_data_private(self):
        from pyspedas.projects.maven.utilities import get_l2_files_from_date

        del_data("*")
        # We don't have credentials to the private site yet, so this is expected to fail
        try:
            data = maven.mag(datatype="ss1s", public=False)
        except Exception as e:
            pass

    def test_load_mag_byorbit_data(self):
        del_data("*")
        data = maven.mag(trange=[500, 501], datatype="ss1s")
        self.assertTrue(len(tplot_names("OB_B*"))>0)
        time.sleep(sleep_time)

    def test_load_sta_data(self):
        del_data("*")
        # No datatype means "load everything"
        data = maven.sta()
        self.assertTrue(data_exists("hkp_raw_2a-hkp"))
        self.assertTrue(data_exists("hkp_2a-hkp"))
        self.assertTrue(data_exists("data_d0-32e4d16a8m"))
        self.assertTrue(data_exists("theta_d1-32e4d16a8m"))
        time.sleep(sleep_time)

    def test_load_sta_hkp_data(self):
        del_data("*")
        data = maven.sta(datatype=["2a"])
        self.assertTrue(data_exists("hkp_raw_2a-hkp"))
        self.assertTrue(data_exists("hkp_2a-hkp"))
        time.sleep(sleep_time)

    def test_load_swea_data(self):
        del_data("*")
        data = maven.swea()
        self.assertTrue(data_exists("diff_en_fluxes_svyspec"))
        time.sleep(sleep_time)

    def test_load_swia_data(self):
        del_data("*")
        data = maven.swia()
        self.assertTrue(data_exists("spectra_diff_en_fluxes_onboardsvyspec"))
        time.sleep(sleep_time)

    def test_load_sep_data(self):
        del_data("*")
        data = maven.sep()
        self.assertTrue(data_exists("f_ion_flux_tot_s2-cal-svy-full"))
        time.sleep(sleep_time)

    def test_load_lpw_data(self):
        del_data("*")
        data = maven.lpw()
        self.assertTrue(data_exists("mvn_lpw_lp_iv_l2_lpiv"))
        time.sleep(sleep_time)

    def test_load_euv_data(self):
        del_data("*")
        data = maven.euv()
        self.assertTrue(data_exists("mvn_euv_calib_bands_bands"))
        time.sleep(sleep_time)

    @unittest.skip("Unable to load RSE data in *.tab file format")
    def test_load_rse_data(self):
        del_data('*')
        data = maven.rse()
        tplot_names()
        self.assertTrue(data_exists('mvn_kp::spacecraft::geo_x'))
        print(data)
        time.sleep(sleep_time)

    def test_load_iuv_data(self):
        del_data("*")
        data = maven.iuv()
        self.assertTrue(data_exists("mvn_kp::spacecraft::altitude"))
        time.sleep(sleep_time)

    def test_load_ngi_data(self):
        del_data("*")
        data = maven.ngi()
        self.assertTrue(data_exists("mvn_kp::spacecraft::altitude"))
        time.sleep(sleep_time)


if __name__ == "__main__":
    unittest.main()
