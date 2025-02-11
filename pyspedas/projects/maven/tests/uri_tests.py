import os, sys
import time
import requests
import unittest
import datetime as dt
import subprocess

from pytplot import data_exists, tplot_names
import pyspedas
from pyspedas.projects import maven
from pyspedas.projects.maven import config,                   \
                                    utilities,                \
                                    maven_kp_to_tplot,        \
                                    download_files_utilities
import fsspec
#==========================================================

# moto server mock details
localhost = "http://localhost:3000"
bucket_name = "test-bucket"

# Set up mock AWS environment variables (fake credentials)
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

# Set environment to use the local Moto S3 server
# S3 ENDPOINT for fsspec
# ENDPOINT URL for cdflib/boto3
os.environ["AWS_S3_ENDPOINT"] = localhost
os.environ["AWS_ENDPOINT_URL"] = localhost

# We need sleep time to avoid "HTTP Error 429: Too Many Requests"
# This may not be necessary any more
sleep_time = 1

import logging

class LoadTestCases(unittest.TestCase):
    """
    Cloud Awareness Unit Tests

    Depends upon moto[server] package. Install via:
        pip install moto[server]

    These tests essentially create a local mock-AWS server as a background
    process at port 3000.
    Note: The environment variables are used as mock credentials in order
          to avoid having to pass the endpoint url to fsspec calls.
    """

    @classmethod
    def setUpClass(cls):
        # Start the moto server for S3 in the background
        # https://github.com/getmoto/moto/issues/4418
        cls.moto_server = subprocess.Popen(
                ["moto_server", "-p3000"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Allow the server to start properly
        time.sleep(2)

        # Create a bucket using direct HTTP requests
        response = requests.put(f"http://localhost:3000/{bucket_name}")
        assert response.status_code == 200, "Bucket creation failed"

    @classmethod
    def tearDownClass(cls):
        # Terminate the moto server after tests
        cls.moto_server.terminate()
        cls.moto_server.communicate()
    
    def get_kp_dict(self):
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.kp()
        fn = [
            '/'.join([
                config.CONFIG["local_data_dir"],
                "maven/data/sci/kp/insitu/2016/01/mvn_kp_insitu_20160101_v20_r02.tab",
            ]),
            '/'.join([
                config.CONFIG["local_data_dir"],
                "maven/data/sci/kp/insitu/2016/01/mvn_kp_insitu_20160102_v20_r02.tab",
            ]),
        ]

        return maven_kp_to_tplot.maven_kp_to_tplot(filename=fn, notplot=True)
    
    def clean_data(self):
        # reset moto server to original state
        response = requests.post("http://localhost:3000/moto-api/reset")
        assert response.status_code == 200, "Moto Server reset failed"
        
        # create bucket again
        response = requests.put(f"http://localhost:3000/{bucket_name}")
        assert response.status_code == 200, "Bucket creation failed"

    #==========================================================================
    # Cloud Awareness Note: Cluster implementation does not stream data due to
    #                       lack of functionality already present in PySPEDAS.

    # Adapted unit tests for AWS-specific URI testing.
    def test_get_merge_orbit_files(self):
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        download_files_utilities.get_orbit_files()
        download_files_utilities.merge_orbit_files()
        orbfilepath = "/".join([
            config.CONFIG["local_data_dir"], "orbitfiles", "merged_maven_orbits.orb"
        ])

        # assert file exists
        fs = fsspec.filesystem("s3")
        self.assertTrue(fs.exists(orbfilepath))

    def test_load_kp_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.kp()
        self.assertTrue(data_exists("mvn_kp::spacecraft::geo_x"))
        time.sleep(sleep_time)
    
    def test_load_kp_spdf_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.kp(spdf=True)
        self.assertTrue(data_exists("LPW_Electron_density"))
        time.sleep(sleep_time)
    
    def test_load_kp_iuvs_occ_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.kp(trange=["2016-01-18","2016-01-19"],iuvs=True)
        self.assertTrue(data_exists("mvn_kp::spacecraft::geo_x"))
        dt1 = dt.datetime.strptime("2016-01-18", "%Y-%m-%d")
        dt2 = dt.datetime.strptime("2016-01-19", "%Y-%m-%d")
        fnames = utilities.get_latest_iuvs_files_from_date_range(dt1,dt2)
        self.assertTrue(len(fnames) > 0)
        self.assertTrue("mvn_kp_iuvs_occ-02533_20160118T125134_v13_r01.tab" in fnames[0])
        time.sleep(sleep_time)
    
    def test_load_kp_iuvs_periapse_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.kp(trange=["2015-03-07","2015-03-08"],iuvs=True)
        self.assertTrue(data_exists("mvn_kp::spacecraft::geo_x"))
        dt1 = dt.datetime.strptime("2015-03-07", "%Y-%m-%d")
        dt2 = dt.datetime.strptime("2015-03-08", "%Y-%m-%d")
        # fnames = get_latest_iuvs_files_from_date_range(dt1,dt2)
        # print(fnames)
        #self.assertTrue(len(fnames) > 0)
        #self.assertTrue("mvn_kp_iuvs_00850_20150308T221253_v13_r01.tab" in fnames[0])
        time.sleep(sleep_time)
    
    def test_load_kp_iuvs_corona_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.kp(trange=["2016-01-14","2016-01-15"],iuvs=True)
        self.assertTrue(data_exists("mvn_kp::spacecraft::geo_x"))
        dt1 = dt.datetime.strptime("2016-01-07", "%Y-%m-%d")
        dt2 = dt.datetime.strptime("2016-01-08", "%Y-%m-%d")
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
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        from pyspedas.projects.maven.kp_utilities import (
            param_list,
            param_range,
            range_select,
            get_inst_obs_labels,
        )
        from pyspedas.projects.maven.kp_utilities import find_param_from_index
        import collections

        kp = self.get_kp_dict()
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
    
    @unittest.skip # BROKEN
    def test_get_file_from_site_private(self):
        f = 'mvn_mag_l2_2016002ss1s_20160102_v01_r01.xml'
        public=False
        full_path='maven_data/maven/data/sci/mag/l2/2016/01'
        # We don't have credentials to the private site yet, so this will fail.
        try:
            download_files_utilities.get_file_from_site(f, public, full_path)
        except Exception as e:
            pass

    
    def test_load_mag_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        from pyspedas.projects.maven.utilities import get_l2_files_from_date

        data = maven.mag(datatype="ss1s")
        self.assertTrue(len(tplot_names("OB_B*"))>0)
        dt1 = dt.datetime.strptime("2016-01-01/12:00:00", "%Y-%m-%d/%H:%M:%S")
        files = get_l2_files_from_date(dt1, "mag")
        self.assertTrue(len(files) > 0)
        time.sleep(sleep_time)
    
    @unittest.skip
    # Cloud Awareness: This extends the prior test to check for the STS file
    #                  types in kp data. It should report an error due to
    #                  PyTplot not currently cloud aware.
    def test_load_mag_sts_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        with self.assertLogs(level="ERROR") as log:
            data = maven.mag() # slow due to the large amount of data
            self.assertIn(
                "PyTplot Error: STS importer is not URI capable.",
                log.output[0]
            )
    
    def test_load_mag_data_private(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"
        
        from pyspedas.projects.maven.utilities import get_l2_files_from_date

        # We don't have credentials to the private site yet, so this is expected to fail
        try:
            data = maven.mag(datatype="ss1s", public=False)
        except Exception as e:
            pass

    @unittest.skip # Still broken, not sure why
    def test_load_mag_byorbit_data(self):
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"
        #saved_logging_level = pyspedas.logger.getEffectiveLevel()
        #pyspedas.logger.setLevel(logging.DEBUG)
        data = maven.mag(trange=[500, 501], datatype="ss1s")
        self.assertTrue(len(tplot_names("OB_B*"))>0)
        #pyspedas.logger.setLevel(saved_logging_level)
        time.sleep(sleep_time)

    def test_load_sta_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        # No datatype means "load everything"
        data = maven.sta()
        self.assertTrue(data_exists("hkp_raw_2a-hkp"))
        self.assertTrue(data_exists("hkp_2a-hkp"))
        self.assertTrue(data_exists("data_d0-32e4d16a8m"))
        self.assertTrue(data_exists("theta_d1-32e4d16a8m"))
        time.sleep(sleep_time)

    def test_load_sta_hkp_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.sta(datatype=["2a"])
        self.assertTrue(data_exists("hkp_raw_2a-hkp"))
        self.assertTrue(data_exists("hkp_2a-hkp"))
        time.sleep(sleep_time)

    def test_load_swea_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.swea()
        self.assertTrue(data_exists("diff_en_fluxes_svyspec"))
        time.sleep(sleep_time)

    def test_load_swia_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.swia()
        self.assertTrue(data_exists("spectra_diff_en_fluxes_onboardsvyspec"))
        time.sleep(sleep_time)
    
    def test_load_sep_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.sep()
        self.assertTrue(data_exists("f_ion_flux_tot_s2-cal-svy-full"))
        time.sleep(sleep_time)

    def test_load_lpw_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.lpw()
        self.assertTrue(data_exists("mvn_lpw_lp_iv_l2_lpiv"))
        time.sleep(sleep_time)
    
    def test_load_euv_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.euv()
        self.assertTrue(data_exists("mvn_euv_calib_bands_bands"))
        time.sleep(sleep_time)
    
    def test_load_rse_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.rse()
        self.assertTrue(data_exists("mvn_kp::spacecraft::altitude"))
        time.sleep(sleep_time)

    def test_load_iuv_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.iuv()
        self.assertTrue(data_exists("mvn_kp::spacecraft::altitude"))
        time.sleep(sleep_time)
    
    def test_load_ngi_data(self):
        self.clean_data()
        config.CONFIG["local_data_dir"] = f"s3://{bucket_name}"

        data = maven.ngi()
        self.assertTrue(data_exists("mvn_kp::spacecraft::altitude"))
        time.sleep(sleep_time)

if __name__ == '__main__':
    unittest.main(verbosity=2)