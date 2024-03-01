import unittest

from mth5.clients.make_mth5 import FDSN
from pyspedas.mth5.load_fdsn import load_fdsn

import pyspedas
import pytplot

import time
import os

import h5py
import pandas as pd

from pyspedas.mth5.config import CONFIG

import loguru
from contextlib import contextmanager
@contextmanager
def loguru_capture_logs(level="INFO", format="{level}:{name}:{message}"):
    """Capture loguru-based logs. There is no other way to assert the loguru log. The custom filter also must be defined here"""
    output = []
    handler_id = loguru.logger.add(output.append, level=level, format=format, filter=pyspedas.mth5._disable_loguru_warnings)
    yield output
    loguru.logger.remove(handler_id)

class Timer:
    """
    Class that tracks the function call time
    """
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.interval = self.end - self.start

class TestMTH5LoadFDSN(unittest.TestCase):
    # Flag to check if there is any open instances of h5 files
    H5OPEN = False

    # This flag result in false if basic test fails and will not run other tests
    BASIC_TEST_FAILED = False

    @classmethod
    def setUpClass(cls):
        # Test if there is any open instances of h5 files
        # This case may not work because tests are executed in a different console where h5 reference may not exist.
        o = h5py.h5f.get_obj_ids(types=h5py.h5f.OBJ_FILE)
        cls.H5OPEN = len(o) > 0

    def setUp(self):
        if len(pytplot.tplot_names()) > 0:
            pytplot.del_data('*')

    def test01_load_fdsn_notrange(self):
        """
        Testing the load_fdsn function without a trange.
        The log message should be printed.
        """
        with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
            load_fdsn(network="4P", station="REU49")
        self.assertIn('trange not specified', cm.output[0])
        self.assertFalse('fdsn_4P_REU49' in pytplot.tnames())

    def test01_load_fdsn_nonetwork(self):
        """
        Test loading data without specifying a network
        The log message should be printed.
        """
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
            load_fdsn(station='REU49', trange=[date_start, date_end])
        self.assertIn('Network not specified', cm.output[0])
        self.assertFalse('fdsn_4P_REU49' in pytplot.tnames())

    def test01_load_fdsn_nostation(self):
        """
        Test loading data without specifying a station
        The log message should be printed.
        """
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
            load_fdsn(network='4P', trange=[date_start, date_end])
        self.assertIn('Station not specified', cm.output[0])
        self.assertFalse('fdsn_4P_REU49' in pytplot.tnames())

    def test02_load_fdsn_basic(self):
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'
        load_fdsn(network="4P", station="REU49", trange=[date_start, date_end])
        load_fdsn(network="4P", station="GAW50", trange=[date_start, date_end])

        try:
            self.assertTrue('fdsn_4P_REU49' in pytplot.tnames())
            self.assertTrue('fdsn_4P_GAW50' in pytplot.tnames())
            self.BASIC_TEST_FAILED = False
        except AssertionError:
            self.BASIC_TEST_FAILED = True

    @unittest.skipIf(BASIC_TEST_FAILED, "Basic test failed.")
    # @patch('sys.stdout', new_callable=StringIO)
    def test03_load_fdsn_nowarnings(self):
        """
        Test with and without nowarning flag
        """
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        # Try loading data, which should result in warnings by MTH5
        with loguru_capture_logs() as output:
            load_fdsn(network="4P", station="REU49", trange=[date_start, date_end], nowarnings=False)
        iswaring = any('WARNING:' in s for s in output)

        if not iswaring:
            self.skipTest("load_fdsn does not produce warnings.")
        with loguru_capture_logs() as output:
            load_fdsn(network="4P", station="REU49", trange=[date_start, date_end], nowarnings=True)
        self.assertFalse(any('WARNING:' in s for s in output))

    @unittest.skipIf(BASIC_TEST_FAILED, "Basic test failed.")
    def test03_load_fdsn_nodownload(self):
        """
        If nodownload flag is specify the h5 file will be reused.
        Testing if the function works faster. Skipping the test if the file was not created.
        """

        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'
        with Timer() as t1:
            load_fdsn(network="4P", station="REU49", trange=[date_start, date_end], nowarnings=False, nodownload=False)

        # Check if the h5 file exist
        if not os.path.isfile(os.path.join(CONFIG['local_data_dir'], '4P_REU49_20150622T014500_20150622T022000.h5')):
            self.skipTest("load_fdsn does not produce h5 file.")

        with Timer() as t2:
            load_fdsn(network="4P", station="REU49", trange=[date_start, date_end], nowarnings=False, nodownload=True)

        self.assertTrue(t1.interval > t2.interval)

    def test04_load_fdsn_samedates(self):
        """
              If dates are the same, tplot variable should not be created.
              load_fdsn should return none
        """

        date_start = '2015-06-22T01:45:00'
        date_end = date_start

        tvar = load_fdsn(network="4P", station="REU49", trange=[date_start, date_end])
        self.assertIsNone(tvar)

    @unittest.skipIf(BASIC_TEST_FAILED, "Basic test failed.")
    def test05_load_fdsn_timeclip(self):
        """
        Test if the time is cliped correctly.
        """
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        tvar = load_fdsn(network="4P", station="REU49", trange=[date_start, date_end], nodownload=True)
        time, data = pytplot.get_data(tvar)

        t1 = pytplot.time_datetime(time[0]).strftime('%Y-%m-%dT%H:%M:%S')
        t2 = pytplot.time_datetime(time[-1]).strftime('%Y-%m-%dT%H:%M:%S')
        self.assertTrue(t1 == date_start)
        self.assertTrue(t2 == date_end)

    def test06_load_fdsn_wrong_network_station(self):
        """
            Test incorrect input. load_fdsn should return raise an error and the temporary files should not exist
        """

        def test_network_station_error(network, station):
            date_start = '2015-06-22T01:45:00'
            date_end = '2015-06-22T02:20:00'

            with self.assertRaises(Exception):
                load_fdsn(network=network, station=station, trange=[date_start, date_end])

            tmp_file = os.path.join(CONFIG['local_data_dir'], f'{network}_{station}.h5')
            self.assertFalse(os.path.isfile(tmp_file))

            with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
                try:
                    load_fdsn(network=network, station=station, trange=[date_start, date_end])
                except:
                    pass
            self.assertIn('Cannot initialize mth5 object', cm.output[0])
            self.assertFalse('fdsn_4P_REU49' in pytplot.tnames())

        # incorrect network
        test_network_station_error(network="4P_", station="REU49")

        # incorrect station
        test_network_station_error(network="4P", station="REU49_")


    # This test seems to be obsolete
    @unittest.skipIf(H5OPEN, "Open h5 files detected. Close all the h5 references before runing this test")
    @unittest.skip
    def test99_load_fdsn_h5_file_error(self):
        # Testing if the file can be created when error occurs
        from pyspedas.mth5.config import CONFIG
        from pyspedas.mth5.load_fdsn import load_fdsn

        request_df = pd.DataFrame(
            {
                "network": ["4P"],
                "station": ["ALW48"],
                "location": ["--"],
                "channel": ["*F*"],
                "start": ["2015-06-22T00:00:00"],
                "end": ["2015-06-24T00:00:00:00"]  # intentional error
            }
        )

        fdsn_object = FDSN(mth5_version='0.2.0', client="IRIS")
        try:
            # This will raise an error because the date format is wrong. But the h5 files will be created and open
            fdsn_object.make_mth5_from_fdsn_client(request_df, interact=False, path=CONFIG['local_data_dir'])
        except Exception as e:
            # Check if the type error is raised
            self.assertIsInstance(e, TypeError)
            pass

        # test is load_fdsn closes the file when error is raised and message is logged
        with self.assertLogs(logger=pyspedas.logger, level="INFO") as cm:
            try:
                load_fdsn(network="4P", station="ALW48", trange=['2015-06-22', '2015-06-24'])
            except Exception as e:
                pass
            # test if we have ERROR and INFO in the log messages
            self.assertTrue(any(map(lambda x: x.find("ERROR") == 0, cm.output)))
            self.assertTrue(any(map(lambda x: x.find("INFO") == 0, cm.output)))

        # Empty lists/dicts evaluate to False
        self.assertFalse(h5py.h5f.get_obj_ids(types=h5py.h5f.OBJ_FILE))

        # import h5py
        # print(h5py.h5f.get_obj_ids(types=h5py.h5f.OBJ_FILE))
        #
        # with self.assertLogs(level="ERROR") as cm:
        #     try:
        #         load_fdsn(network="4P", station="ALW48", trange=['2015-06-22', '2015-06-24'])
        #     except:
        #         pass
        # print(cm)

        pass

    @unittest.skip
    def test99_load_fdsn_no_data(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
