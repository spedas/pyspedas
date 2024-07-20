import unittest
from unittest.mock import patch, MagicMock, mock_open
import urllib.error
from urllib.error import URLError, HTTPError
import socket

from mth5.clients.make_mth5 import FDSN
from pyspedas.mth5.load_fdsn import load_fdsn
from pyspedas.mth5.utilities import _list_of_fdsn_channels
from pyspedas.mth5.utilities import datasets

# This one is unused
from pyspedas.mth5.config import CONFIG

import pyspedas
import pytplot

import time
import os
import io

import h5py
import pandas as pd

from pyspedas.mth5.config import CONFIG

import loguru
from contextlib import contextmanager

# Handling exceptions of bad data input
from obspy.clients.fdsn.header import FDSNBadRequestException
from obspy.clients.fdsn.header import FDSNNoServiceException


@contextmanager
def loguru_capture_logs(level="INFO", format="{level}:{name}:{message}"):
    """Capture loguru-based logs. There is no other way to assert the loguru log. The custom filter also must be defined here"""
    loguru.logger.remove()
    output = []
    handler_id = loguru.logger.add(output.append, level=level, format=format,
                                   filter=pyspedas.mth5._disable_loguru_warnings)
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
        # TODO: H5OPEN - is not evaluated correctly. The  @unittest.skipIf decorator evaluates the condition at import time
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

    # TODO: this should not work, because BASIC_TEST_FAILED should be evaluated before the call of the test...
    @unittest.skipIf(BASIC_TEST_FAILED, "Basic test failed.")
    # @patch('sys.stdout', new_callable=StringIO)
    def test03_load_fdsn_nowarnings(self):
        """
        Test with and without nowarning flag
        """
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        # Try loading data, which should result in warnings by MTH5
        with loguru_capture_logs(level="WARNING") as output:
            load_fdsn(network="4P", station="REU49", trange=[date_start, date_end], nowarnings=False)
            self.assertTrue(len(output) > 0)
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
        Test if the time is clipped correctly.
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

            with self.assertLogs(logger=pyspedas.logger, level='ERROR') as log:
                with self.assertRaises(Exception):
                    load_fdsn(network=network, station=station, trange=[date_start, date_end])
                self.assertIn("HTTP Status code: 400", log.output[0])

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

    # Mock FDSN and MTH so we do not make unnessesary calls
    @patch('mth5.clients.make_mth5.FDSN.__init__', return_value=None)
    @patch('mth5.mth5.MTH5.__init__', return_value=None)
    def test07_print_request(self, mock_FDSN, mock_MTH5):
        """Test the print_request parameter and ensure print output is correct."""
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        # Terminate function after print is complete
        def side_effect(*args, **kwargs):
            raise SystemExit("Exiting test.")

        # Assign the side effect to the mock objects
        mock_FDSN.side_effect = side_effect
        mock_MTH5.side_effect = side_effect

        # Capture the printed output
        printed_output = io.StringIO()
        with self.assertRaises(SystemExit) as cm:
            with patch('sys.stdout', new=printed_output):
                load_fdsn(trange=[date_start, date_end], network="4P", station="REU49", print_request=True)

        # Check the content of the print output
        printed_df = printed_output.getvalue()
        expected_columns = ['network', 'station', 'start', 'end']
        self.assertTrue(all(col in printed_df for col in expected_columns))

    @patch('mth5.clients.make_mth5.FDSN.make_mth5_from_fdsn_client')
    def test08_request_df_parameter(self, mock_make_mth5):
        """Test the request_df parameter with a custom DataFrame."""
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        custom_request_df = pd.DataFrame({
            "network": ["4P"],
            "station": ["REU49"],
            "location": ["--"],
            "channel": ["*F*"],
            "start": [date_start],
            "end": [date_end]
        })

        def side_effect(*args, **kwargs):
            raise SystemExit("make_mth5_from_fdsn_client called, exiting test.")

        mock_make_mth5.side_effect = side_effect

        with self.assertRaises(SystemExit) as cm:
            load_fdsn(trange=[date_start, date_end], network="4P", station="REU49", request_df=custom_request_df)

        # Verify that the reason for exit is the make_mth5_from_fdsn_client call
        self.assertEqual(str(cm.exception), "make_mth5_from_fdsn_client called, exiting test.")

        # Verify that make_mth5_from_fdsn_client was called with the custom DataFrame
        # mock_make_mth5.assert_called_once_with(custom_request_df, interact=False, path=CONFIG['local_data_dir'])
        self.assertTrue(any(call_args[0][0].equals(custom_request_df) for call_args in mock_make_mth5.call_args_list))

    def test09_invalid_date_or_data(self):
        """Test the function with invalid date formats in trange."""
        invalid_date_start = '2015-06-22'
        invalid_date_end = '21-06-2015'  # Invalid format (should handle ok) but the date end before start should results in Exception
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        with self.assertRaises(FDSNBadRequestException) as cm:
            load_fdsn(trange=[invalid_date_start, invalid_date_end], network="4P", station="REU49")

        # Verify the exception type
        self.assertTrue(isinstance(cm.exception, FDSNBadRequestException))

        with self.assertRaises(FDSNBadRequestException) as cm:
            load_fdsn(trange=[date_start, date_end], network="4P", station="NON_EXISTENT")

        # Verify the exception type
        self.assertTrue(isinstance(cm.exception, FDSNBadRequestException))

        with self.assertRaises(FDSNBadRequestException) as cm:
            load_fdsn(trange=[date_start, date_end], network="NON_EXISTENT", station="REU49")

        # Verify the exception type
        self.assertTrue(isinstance(cm.exception, FDSNBadRequestException))

    # TODO: FOR SOME REASON, this test must be called before test02_load_fdsn_basic. Otherwise it does not work.
    @patch('urllib.request.OpenerDirector.open')
    def test02__connection_errors(self, mock_open):
        """Test the function handling of network connection issues."""
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        # Simulate a no internet connection
        mock_open.side_effect = URLError("Network unreachable")

        with self.assertRaises(Exception) as cm:
            load_fdsn(trange=[date_start, date_end], network="4P", station="REU49")
            print(cm.exception)

        # Verify the exception type and message for URLError
        self.assertTrue(isinstance(cm.exception, FDSNNoServiceException) or isinstance(cm.exception, URLError))
        # self.assertTrue(isinstance(cm.exception, URLError))

    # This test seems to be obsolete
    @unittest.skipIf(H5OPEN, "Open h5 files detected. Close all the h5 references before runing this test")
    @unittest.skip
    def test99_load_fdsn_h5_file_error(self):
        # Testing if the file can be created when error occurs

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


class TestListOfChannels(unittest.TestCase):
    def test01_list_of_channels_type(self):
        """
        Test that the _list_of_channels function returns a string.
        """
        result = _list_of_fdsn_channels()
        self.assertIsInstance(result, str)

    def test02_list_of_channels_divisible_by_three(self):
        """
        Test that the number of channel names (elements) in the list is divisible by 3.
        """
        result = _list_of_fdsn_channels()
        channel_list = result.split(',')
        self.assertEqual(len(channel_list) % 3, 0)

    def test03_list_of_channels_contains_F(self):
        """
        Test that all channel names in the list have "F" in the middle.
        """
        result = _list_of_fdsn_channels()
        channel_list = result.split(',')
        for channel in channel_list:
            # Assuming the format is always one character for band, 'F' for instrument, and one character for orientation
            self.assertTrue(channel[1] == 'F')


class TestDatasetsFunction(unittest.TestCase):
    # Mock data of the responce
    mock_data = """Network|Station|Location|Channel|Latitude|Longitude|Elevation|Depth|Azimuth|Dip|SensorDescription|Scale|ScaleFreq|ScaleUnits|SampleRate|StartTime|EndTime
4P|ALW48||LFE|0|0|0|0|0|0|NIMS|1|1|nT|1|2015-06-18T15:00:36.0000|2015-07-09T13:45:10.0000
4P|ALW48||LFN|0|0|0|0|0|0|NIMS|1|1|nT|1|2015-06-18T15:00:36.0000|2015-07-09T13:45:10.0000
4P|ALW48||LFZ|0|0|0|0|0|0|NIMS|1|1|nT|1|2015-06-18T15:00:36.0000|2015-07-09T13:45:10.0000
"""

    # Set to True if we can get to https://service.iris.edu
    PING_IRIS = False

    @classmethod
    def setUpClass(cls):
        host = "service.iris.edu"
        try:
            # Create a socket object
            with socket.create_connection((host, 443), timeout=5) as sock:
                # If the connection was successful, close it and return accessible
                cls.PING_IRIS = True
        except socket.error as e:
            print(e)
            pass

    def test01_datasets_no_trange(self):
        """Test datasets function with no trange."""
        result = datasets()
        self.assertIsNone(result)

    @patch('urllib.request.urlopen')
    @patch('pyspedas.logger.error')  # Assuming pyspedas.logger.error is the correct path
    def test02_datasets_network_failure(self, mock_logger_error, mock_urlopen):
        """Test datasets function with a network failure."""
        # Simulate an HTTPError, which is a subclass of URLError and has a 'code' attribute.
        url = 'http://example.com'
        error_message = 'Test Error'
        mock_urlopen.side_effect = urllib.error.HTTPError(url, 500, error_message, None, None)

        result = datasets(["2019-11-14", "2019-11-15"])
        mock_logger_error.assert_called_once()
        self.assertTrue(any("HTTP or URL Error" in call_args[0][0] for call_args in mock_logger_error.call_args_list))

        self.assertEqual(result, {})

    @patch('urllib.request.urlopen')
    def test02_datasets_no_data(self, mock_urlopen):
        """Test datasets function with no data returned from network."""
        mock_response = MagicMock()
        mock_response.status = 404
        mock_urlopen.return_value.__enter__.return_value = mock_response
        result = datasets(["2019-11-14", "2019-11-15"])
        self.assertEqual(result, {})

    @patch('urllib.request.urlopen')
    def test04_datasets_valid_data(self, mock_urlopen):
        """Test datasets function with valid data."""

        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = self.mock_data.encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response

        expected = {'4P': {'ALW48': {('2015-06-18T15:00:36.0000', '2015-07-09T13:45:10.0000'): ['LFE', 'LFN', 'LFZ']}}}

        result = datasets(["2015-06-22", "2015-06-23"], network="4P", station="ALW48")
        self.assertEqual(result, expected)

    @patch('urllib.request.urlopen')
    def test05_datasets_incorrect_data(self, mock_urlopen):
        """Test datasets function with data which does not have all 3 channels."""
        mock_data = self.mock_data.splitlines()
        mock_data[-2] = "4P|ALW48||UFZ|0|0|0|0|0|0|NIMS|1|1|nT|1|2015-06-18T15:00:36.0000|2015-07-09T13:45:10.0000"
        mock_data = "\n".join(mock_data)

        #         """Network|Station|Location|Channel|Latitude|Longitude|Elevation|Depth|Azimuth|Dip|SensorDescription|Scale|ScaleFreq|ScaleUnits|SampleRate|StartTime|EndTime
        # 4P|ALW48||LFE|0|0|0|0|0|0|NIMS|1|1|nT|1|2015-06-18T15:00:36.0000|2015-07-09T13:45:10.0000
        # 4P|ALW48||LFN|0|0|0|0|0|0|NIMS|1|1|nT|1|2015-06-18T15:00:36.0000|2015-07-09T13:45:10.0000
        # 4P|ALW48||UFZ|0|0|0|0|0|0|NIMS|1|1|nT|1|2015-06-18T15:00:36.0000|2015-07-09T13:45:10.0000
        # """
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = mock_data.encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response

        expected = {}

        result = datasets(["2015-06-22", "2015-06-23"], network="4P", station="ALW48")
        self.assertEqual(result, expected)

    @patch('urllib.request.urlopen')
    def test06_url_construction_with_network(self, mock_urlopen):
        """Test the URL construction when a specific network is provided."""
        datasets(["2015-06-22", "2015-06-23"], network="4P")
        # Extract the URL passed to urlopen
        called_url = mock_urlopen.call_args[0][0]
        self.assertIn("net=4P", called_url)

    @patch('urllib.request.urlopen')
    def test06_url_construction_with_station(self, mock_urlopen):
        """Test the URL construction when a specific station is provided."""
        datasets(["2015-06-22", "2015-06-23"], station="ALW48")
        # Extract the URL passed to urlopen
        called_url = mock_urlopen.call_args[0][0]
        self.assertIn("sta=ALW48", called_url)

    @patch('urllib.request.urlopen')
    def test06_url_construction_with_network_and_station(self, mock_urlopen):
        """Test the URL construction when both network and station are provided."""
        datasets(["2015-06-22", "2015-06-23"], network="4P", station="ALW48")
        # Extract the URL passed to urlopen
        called_url = mock_urlopen.call_args[0][0]
        self.assertIn("net=4P", called_url)
        self.assertIn("sta=ALW48", called_url)

    def test07_datasets_realcall(self):
        """Test datasets function with actual internet connection."""
        # Dynamically decide to skip the test based on the runtime condition
        if not self.PING_IRIS:
            self.skipTest("Cannot reach iris website")

        expected = {'4P': {'ALW48': {('2015-06-18T15:00:36.0000', '2015-07-09T13:45:10.0000'): ['LFE', 'LFN', 'LFZ']}}}
        result = datasets(["2015-06-22", "2015-06-23"], network="4P", station="ALW48")
        self.assertEqual(result, expected)

    @patch('urllib.request.urlopen')
    def test08_datasets_USAarea(self, mock_urlopen):
        """Test datasets function with USAarea set to True or False."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = self.mock_data.encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = datasets(["2015-06-22", "2015-06-23"], network="4P", station="ALW48", USAarea=True)

        # Extract the URL passed to urlopen
        called_url = mock_urlopen.call_args[0][0]
        self.assertIn("maxlat=49", called_url)
        self.assertIn("minlon=-127", called_url)
        self.assertIn("maxlon=-59", called_url)
        self.assertIn("minlat=24", called_url)

        result = datasets(["2015-06-22", "2015-06-23"], network="4P", station="ALW48")

        # Extract the URL passed to urlopen
        called_url = mock_urlopen.call_args[0][0]
        self.assertNotIn("maxlat", called_url)
        self.assertNotIn("minlon", called_url)
        self.assertNotIn("maxlon", called_url)
        self.assertNotIn("minlat", called_url)


if __name__ == '__main__':
    unittest.main()
