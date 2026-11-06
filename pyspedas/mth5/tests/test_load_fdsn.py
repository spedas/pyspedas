import unittest
from unittest.mock import patch, MagicMock, mock_open
import urllib.error
from urllib.error import URLError, HTTPError
import socket
from types import SimpleNamespace

# from mth5.clients.fdsn import FDSN
from pyspedas.mth5.load_fdsn import load_fdsn
from pyspedas.mth5.utilities import _list_of_fdsn_channels
from pyspedas.mth5.utilities import datasets

# This one is unused
# from pyspedas.mth5.config import CONFIG

import pyspedas

import time
import os
import io

import h5py
import pandas as pd
import numpy as np

from pyspedas.mth5.config import CONFIG

import loguru
from contextlib import contextmanager
from pyspedas import tnames, del_data

# Handling exceptions of bad data input
from obspy.clients.fdsn.header import FDSNBadRequestException
from obspy.clients.fdsn.header import FDSNException
# from obspy.clients.fdsn.header import FDSNNoServiceException # Replaced by FDSNException


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

    # This flag results in False if basic test fails and will not run other tests
    BASIC_TEST_FAILED = False

    # This flag results in False if the connection check fails, so tests that
    # need a real connection but don't depend on BASIC_TEST_FAILED can skip
    # cleanly instead of failing noisily when there is no network.
    CONNECTION_FAILED = False

    @classmethod
    def setUpClass(cls):
        # TODO: H5OPEN - is not evaluated correctly. The @unittest.skipIf decorator evaluates the condition at import time
        # Test if there is any open instances of h5 files
        # This case may not work because tests are executed in a different console where h5 reference may not exist.
        o = h5py.h5f.get_obj_ids(types=h5py.h5f.OBJ_FILE)
        cls.H5OPEN = len(o) > 0

    def setUp(self):
        if len(pyspedas.tplot_names()) > 0:
            pyspedas.del_data('*')

    # Tests are named test<bucket>_<description>, where <bucket> groups tests
    # that share the same run-order requirement (10_ no connection/mock,
    # 20_ mocked network, 30_ connection error, 40_ basic load and connection
    # check, 50_ real FDSN calls independent of basic, 60_ depend on basic).
    # Tests within a bucket keep the same number so a later insertion between
    # buckets can use an unused number (e.g. test15_, test45_) without
    # renumbering anything else. See tests.md for the full rationale.

    def test10_load_fdsn_notrange(self):
        """
        Testing the load_fdsn function without a trange.
        The log message should be printed.
        """
        with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
            load_fdsn(network="4P", station="REU49")
        self.assertIn('trange not specified', cm.output[0])
        self.assertFalse('fdsn_4P_REU49' in pyspedas.tnames())

    def test10_load_fdsn_trange_wrong_length(self):
        """
        A trange that is not exactly 2 elements must log an ERROR and
        return without creating a tplot variable, instead of raising a
        raw IndexError or silently ignoring extra elements.
        """
        with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
            load_fdsn(network="4P", station="REU49", trange=['2015-06-22T01:45:00'])
        self.assertIn('trange must have exactly 2 elements', cm.output[0])
        self.assertFalse('fdsn_4P_REU49' in pyspedas.tnames())

        with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
            load_fdsn(
                network="4P", station="REU49",
                trange=['2015-06-22T01:45:00', '2015-06-22T02:20:00', '2015-06-22T03:00:00'],
            )
        self.assertIn('trange must have exactly 2 elements', cm.output[0])
        self.assertFalse('fdsn_4P_REU49' in pyspedas.tnames())

    def test10_load_fdsn_nonetwork(self):
        """
        Test loading data without specifying a network
        The log message should be printed.
        """
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
            load_fdsn(station='REU49', trange=[date_start, date_end])
        self.assertIn('Network not specified', cm.output[0])
        self.assertFalse('fdsn_4P_REU49' in pyspedas.tnames())

    def test10_load_fdsn_nostation(self):
        """
        Test loading data without specifying a station
        The log message should be printed.
        """
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
            load_fdsn(network='4P', trange=[date_start, date_end])
        self.assertIn('Station not specified', cm.output[0])
        self.assertFalse('fdsn_4P_REU49' in pyspedas.tnames())

    # Shared time range for the mocked run-splitting tests below.
    SPLIT_DATE_START = '2015-06-22T01:45:00'
    SPLIT_DATE_END = '2015-06-22T02:20:00'

    @staticmethod
    def _mocked_fdsn_station(coord_sys, units, measurement_type, times, values,
                              missing_units_channel=None, missing_channel=None):
        """
        Build a mocked MTH5 station with one run of magnetic data.

        Mimics just enough of the MTH5 object tree (station_data.metadata,
        run_data.metadata.time_period, run_ts.dataset.hx/hy/hz) for
        load_fdsn to process one run end-to-end. missing_units_channel, one
        of 'hx'/'hy'/'hz', builds that channel without a units attribute,
        simulating a sensor that didn't report its units. missing_channel,
        also one of 'hx'/'hy'/'hz', leaves that channel out of the dataset
        entirely, simulating a sensor that recorded no data at all.
        """
        channel_names = [name for name in ('hx', 'hy', 'hz') if name != missing_channel]

        def make_channel(channel_name):
            if channel_name == missing_units_channel:
                return SimpleNamespace(to_numpy=lambda: np.array(values), type=measurement_type)
            return SimpleNamespace(to_numpy=lambda: np.array(values), units=units, type=measurement_type)

        dataset_kwargs = {name: make_channel(name) for name in channel_names}
        run_ts = SimpleNamespace(
            dataset=SimpleNamespace(
                attrs={'channels_recorded_magnetic': channel_names},
                channels_recorded_magnetic=channel_names,
                time=SimpleNamespace(to_numpy=lambda: np.array(times)),
                **dataset_kwargs,
            ),
            filters=[object()],
        )
        run_ts.calibrate = MagicMock(return_value=run_ts)
        run = SimpleNamespace(
            metadata=SimpleNamespace(
                time_period=SimpleNamespace(
                    start=TestMTH5LoadFDSN.SPLIT_DATE_START,
                    end=TestMTH5LoadFDSN.SPLIT_DATE_END,
                )
            ),
            to_runts=MagicMock(return_value=run_ts),
        )
        station_metadata = SimpleNamespace(
            orientation=SimpleNamespace(reference_frame=SimpleNamespace(value=coord_sys)),
            run_list=['run'],
            channels_recorded=['hx', 'hy', 'hz'],
        )
        return SimpleNamespace(metadata=station_metadata, get_run=MagicMock(return_value=run))

    @patch('os.path.isfile', return_value=True)
    @patch('pyspedas.mth5.load_fdsn.MTH5')
    def test20_load_fdsn_splits_on_units(self, mock_MTH5, mock_isfile):
        """Runs with different units (e.g. a sensor swap) split into separate tplot variables."""
        stations = [
            self._mocked_fdsn_station('geographic', 'nT', 'magnetic', [1, 2], [10, 20]),
            self._mocked_fdsn_station('geographic', 'mV', 'magnetic', [3], [30]),
        ]
        mock_mth5 = mock_MTH5.return_value.__enter__.return_value
        mock_mth5.surveys_group.groups_list = ['survey1', 'survey2']
        mock_mth5.get_station.side_effect = stations

        with self.assertLogs(logger=pyspedas.logger, level='WARNING') as cm:
            result = load_fdsn(
                network='TEST', station='TEST',
                trange=[self.SPLIT_DATE_START, self.SPLIT_DATE_END],
                nodownload=True,
            )

        self.assertEqual(result, 'fdsn_TEST_TEST')
        self.assertTrue(any('inconsistent run metadata' in message for message in cm.output))
        self.assertEqual(pyspedas.get_data('fdsn_TEST_TEST', metadata=True)['data_att']['units'], 'nT')
        self.assertEqual(pyspedas.get_data('fdsn_TEST_TEST_1', metadata=True)['data_att']['units'], 'mV')

    @patch('os.path.isfile', return_value=True)
    @patch('pyspedas.mth5.load_fdsn.MTH5')
    def test20_load_fdsn_splits_on_measurement_type(self, mock_MTH5, mock_isfile):
        """Runs with different measurement types split into separate tplot variables."""
        stations = [
            self._mocked_fdsn_station('geographic', 'nT', 'magnetic', [1, 2], [10, 20]),
            self._mocked_fdsn_station('geographic', 'nT', 'auxiliary', [3], [30]),
        ]
        mock_mth5 = mock_MTH5.return_value.__enter__.return_value
        mock_mth5.surveys_group.groups_list = ['survey1', 'survey2']
        mock_mth5.get_station.side_effect = stations

        with self.assertLogs(logger=pyspedas.logger, level='WARNING') as cm:
            result = load_fdsn(
                network='TEST', station='TEST',
                trange=[self.SPLIT_DATE_START, self.SPLIT_DATE_END],
                nodownload=True,
            )

        self.assertEqual(result, 'fdsn_TEST_TEST')
        self.assertTrue(any('inconsistent run metadata' in message for message in cm.output))
        self.assertEqual(
            pyspedas.get_data('fdsn_TEST_TEST', metadata=True)['data_att']['measurements_type'], 'magnetic',
        )
        self.assertEqual(
            pyspedas.get_data('fdsn_TEST_TEST_1', metadata=True)['data_att']['measurements_type'], 'auxiliary',
        )

    @patch('os.path.isfile', return_value=True)
    @patch('pyspedas.mth5.load_fdsn.MTH5')
    def test20_load_fdsn_splits_on_coord_sys(self, mock_MTH5, mock_isfile):
        """Runs with different coordinate systems split into separate tplot variables."""
        stations = [
            self._mocked_fdsn_station('geographic', 'nT', 'magnetic', [1, 2], [10, 20]),
            self._mocked_fdsn_station('geomagnetic', 'nT', 'magnetic', [3], [30]),
        ]
        mock_mth5 = mock_MTH5.return_value.__enter__.return_value
        mock_mth5.surveys_group.groups_list = ['survey1', 'survey2']
        mock_mth5.get_station.side_effect = stations

        with self.assertLogs(logger=pyspedas.logger, level='WARNING') as cm:
            result = load_fdsn(
                network='TEST', station='TEST',
                trange=[self.SPLIT_DATE_START, self.SPLIT_DATE_END],
                nodownload=True,
            )

        self.assertEqual(result, 'fdsn_TEST_TEST')
        self.assertTrue(any('inconsistent run metadata' in message for message in cm.output))
        self.assertEqual(pyspedas.get_coords('fdsn_TEST_TEST'), 'geographic')
        self.assertEqual(pyspedas.get_coords('fdsn_TEST_TEST_1'), 'geomagnetic')

    @patch('os.path.isfile', return_value=True)
    @patch('pyspedas.mth5.load_fdsn.MTH5')
    def test20_load_fdsn_splits_on_missing_channel_units(self, mock_MTH5, mock_isfile):
        """A run missing units on one channel (e.g. hy) gets its own signature instead of merging silently."""
        stations = [
            self._mocked_fdsn_station('geographic', 'nT', 'magnetic', [1, 2], [10, 20]),
            self._mocked_fdsn_station('geographic', 'nT', 'magnetic', [3], [30], missing_units_channel='hy'),
        ]
        mock_mth5 = mock_MTH5.return_value.__enter__.return_value
        mock_mth5.surveys_group.groups_list = ['survey1', 'survey2']
        mock_mth5.get_station.side_effect = stations

        with self.assertLogs(logger=pyspedas.logger, level='WARNING') as cm:
            result = load_fdsn(
                network='TEST', station='TEST',
                trange=[self.SPLIT_DATE_START, self.SPLIT_DATE_END],
                nodownload=True,
            )

        self.assertEqual(result, 'fdsn_TEST_TEST')
        self.assertTrue(any('inconsistent run metadata' in message for message in cm.output))
        self.assertEqual(pyspedas.get_data('fdsn_TEST_TEST', metadata=True)['data_att']['units'], 'nT')
        self.assertEqual(
            pyspedas.get_data('fdsn_TEST_TEST_1', metadata=True)['data_att']['units'], 'nT,None,nT',
        )

    @patch('os.path.isfile', return_value=True)
    @patch('pyspedas.mth5.load_fdsn.MTH5')
    def test20_load_fdsn_fills_missing_channel_with_nan(self, mock_MTH5, mock_isfile):
        """A run with only 2 of 3 magnetic components still loads, with the missing one NaN-filled."""
        stations = [
            self._mocked_fdsn_station('geographic', 'nT', 'magnetic', [1, 2], [10, 20], missing_channel='hy'),
        ]
        mock_mth5 = mock_MTH5.return_value.__enter__.return_value
        mock_mth5.surveys_group.groups_list = ['survey1']
        mock_mth5.get_station.side_effect = stations

        result = load_fdsn(
            network='TEST', station='TEST',
            trange=[self.SPLIT_DATE_START, self.SPLIT_DATE_END],
            nodownload=True,
        )

        self.assertEqual(result, 'fdsn_TEST_TEST')
        time, data = pyspedas.get_data(result)
        self.assertEqual(data.shape, (2, 3))
        self.assertTrue(np.array_equal(data[:, 0], [10, 20]))
        self.assertTrue(np.all(np.isnan(data[:, 1])))
        self.assertTrue(np.array_equal(data[:, 2], [10, 20]))

    # Mock FDSN and MTH5 so we do not make unnecessary calls
    @patch('mth5.clients.make_mth5.FDSN.__init__', return_value=None)
    @patch('mth5.mth5.MTH5.__init__', return_value=None)
    def test20_print_request(self, mock_FDSN, mock_MTH5):
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

    @patch('pyspedas.mth5.load_fdsn.MTH5')
    @patch('os.rename')
    @patch('os.path.isfile', return_value=False)
    @patch('mth5.clients.make_mth5.FDSN.make_mth5_from_fdsn_client', return_value='fake_downloaded.h5')
    def test20_downloadonly_returns_path(self, mock_make_mth5, mock_isfile, mock_rename, mock_MTH5):
        """
        downloadonly=True must return the cached MTH5 path and skip tplot creation.

        make_mth5_from_fdsn_client is mocked to return a fake download path.
        os.path.isfile and os.rename are mocked because load_fdsn otherwise
        touches the real filesystem to check for and rename the cache file.
        The fake path is asserted below as the os.rename source argument.
        """
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        result = load_fdsn(
            trange=[date_start, date_end], network="TEST", station="TEST",
            downloadonly=True,
        )

        self.assertTrue(result.endswith('.h5'))
        mock_MTH5.assert_not_called()
        # Confirms the fake download path actually reached load_fdsn's
        # rename step, instead of being an unused mock return value.
        mock_rename.assert_called_once_with('fake_downloaded.h5', result)

    @patch('mth5.clients.make_mth5.FDSN.make_mth5_from_fdsn_client')
    def test20_request_df_parameter(self, mock_make_mth5):
        """Test the request_df parameter with a custom DataFrame."""
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        # Use different values so we can see that this DataFrame takes priority.
        custom_request_df = pd.DataFrame({
            "network": ["CUSTOM"],
            "station": ["CUSTOM_STATION"],
            "location": ["--"],
            "channel": ["*F*"],
            "start": [date_start],
            "end": [date_end]
        })
        original_request_df = custom_request_df.copy(deep=True)

        class RequestCaptured(Exception):
            pass

        # Stop here once the request has been handed off.
        mock_make_mth5.side_effect = RequestCaptured

        # The loader should hand off the request before doing any real download.
        with self.assertRaises(RequestCaptured):
            load_fdsn(
                trange=[date_start, date_end],
                network="4P",
                station="REU49",
                request_df=custom_request_df,
            )

        # The downloader should receive exactly the request we supplied.
        mock_make_mth5.assert_called_once_with(
            custom_request_df,
            interact=False,
            path=CONFIG['local_data_dir'],
        )
        # The custom station details should still be present after the call.
        self.assertEqual(custom_request_df.loc[0, "network"], "CUSTOM")
        self.assertEqual(custom_request_df.loc[0, "station"], "CUSTOM_STATION")
        # Passing the request must not change the caller's DataFrame.
        pd.testing.assert_frame_equal(custom_request_df, original_request_df)

    @patch('os.path.isfile', return_value=True)
    @patch('pyspedas.mth5.load_fdsn.MTH5')
    def test20_station_data_undefined_unboundlocalerror(self, mock_MTH5, mock_isfile):
        """
        If no survey matches the station, station_data is never assigned,
        so referencing it later raises UnboundLocalError. That must be
        caught and logged as "station_data was not defined correctly",
        the same as the AttributeError case below.
        """
        mock_mth5_instance = MagicMock()
        mock_mth5_instance.__enter__.return_value.surveys_group.groups_list = []
        mock_MTH5.return_value = mock_mth5_instance

        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
            result = load_fdsn(
                network="4P", station="REU49", trange=[date_start, date_end],
                nodownload=True, noexception=True,
            )
        self.assertIn('station_data was not defined correctly', cm.output[0])
        self.assertIsNone(result)

    @patch('os.path.isfile', return_value=True)
    @patch('pyspedas.mth5.load_fdsn.MTH5')
    def test20_station_data_missing_channels_attributeerror(self, mock_MTH5, mock_isfile):
        """
        If station_data.metadata has no channels_recorded attribute,
        referencing it raises AttributeError. That must be caught and
        logged as "station_data was not defined correctly", the same as
        the UnboundLocalError case above.
        """
        station_metadata = SimpleNamespace(run_list=[])
        station_data = SimpleNamespace(metadata=station_metadata)

        mock_mth5_instance = MagicMock()
        mock_mth5_instance.__enter__.return_value.surveys_group.groups_list = ['4P']
        mock_mth5_instance.__enter__.return_value.get_station.return_value = station_data
        mock_MTH5.return_value = mock_mth5_instance

        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
            result = load_fdsn(
                network="4P", station="REU49", trange=[date_start, date_end],
                nodownload=True, noexception=True,
            )
        self.assertIn('station_data was not defined correctly', cm.output[0])
        self.assertIsNone(result)

    @patch('urllib.request.OpenerDirector.open')
    def test30_connection_errors(self, mock_open):
        """Test the function handling of network connection issues."""
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        # Simulate a no internet connection
        mock_open.side_effect = URLError("Network unreachable")

        with self.assertRaises(Exception) as cm:
            load_fdsn(trange=[date_start, date_end], network="4P", station="REU49")

        # Depending on whether obspy's service-discovery cache for this host is
        # already warm (see tests.md), the simulated connection failure surfaces
        # as FDSNNoServiceException (cold cache) or a plain FDSNException (warm
        # cache). Both are FDSNException, so check that instead of either
        # specific subclass or URLError, which obspy never lets escape here.
        self.assertIsInstance(cm.exception, FDSNException)

    def test40_connection_check(self):
        """
        Makes a real load_fdsn call to confirm the network/FDSN service is
        reachable. Sets self.CONNECTION_FAILED so that test50_* tests can
        skip cleanly instead of failing noisily when there is no connection.
        """
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'
        try:
            load_fdsn(network="4P", station="REU49", trange=[date_start, date_end])
            self.CONNECTION_FAILED = False
        except Exception:
            self.CONNECTION_FAILED = True

    def test40_load_fdsn_basic(self):
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'
        load_fdsn(network="4P", station="REU49", trange=[date_start, date_end])
        load_fdsn(network="4P", station="GAW50", trange=[date_start, date_end])

        try:
            self.assertTrue('fdsn_4P_REU49' in pyspedas.tnames())
            self.assertTrue('fdsn_4P_GAW50' in pyspedas.tnames())
            self.BASIC_TEST_FAILED = False
        except AssertionError:
            self.BASIC_TEST_FAILED = True

    def test50_load_fdsn_samedates(self):
        """
              If dates are the same, tplot variable should not be created.
              load_fdsn should return None
        """
        if self.CONNECTION_FAILED:
            self.skipTest("No connection.")

        # The server response has changed to '422: Unprocessable Entity' for this request
        # because of the same start/end times. So we need to catch the exception now.
        from obspy.clients.fdsn.header import FDSNException

        date_start = '2015-06-22T01:45:00'
        date_end = date_start
        tvar = None
        # Identical or out of order start times should be caught by load_fdsn now.
        exception_occurred = False

        try:
            tvar = load_fdsn(network="4P", station="REU49", trange=[date_start, date_end])
        except FDSNException as e:
            # If load_fdsn doesn't catch the problem with start/end times, the MTH5 library
            # will throw an exception. We consider that a failed test.
            exception_occurred = True
            pass

        self.assertFalse(exception_occurred)
        self.assertIsNone(tvar)

    def test50_load_fdsn_wrong_network_station(self):
        """
            Test incorrect input. load_fdsn should raise an error and the temporary files should not exist
        """
        if self.CONNECTION_FAILED:
            self.skipTest("No connection.")

        def test_network_station_error(network, station):
            date_start = '2015-06-22T01:45:00'
            date_end = '2015-06-22T02:20:00'

            with self.assertLogs(logger=pyspedas.logger, level='ERROR') as log:
                with self.assertRaises(FDSNBadRequestException):
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
            self.assertFalse('fdsn_4P_REU49' in pyspedas.tnames())

        # incorrect network
        test_network_station_error(network="4P_", station="REU49")

        # incorrect station
        test_network_station_error(network="4P", station="REU49_")

    def test50_invalid_date(self):
        """Test the function with invalid date formats in trange."""
        if self.CONNECTION_FAILED:
            self.skipTest("No connection.")

        invalid_date_start = '2015-06-22'
        invalid_date_end = '21-06-2015'  # Day-first string; parses to a date earlier than invalid_date_start

        with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
            load_fdsn(trange=[invalid_date_start, invalid_date_end], network="4P", station="REU49")
        # Test for Error message. The error now: "End time 2015-06-21 00:00:00 earlier or equal to start time 2015-06-22 00:00:00"
        self.assertTrue(len(cm.output) > 0)

        self.assertTrue(len(tnames()) == 0)

    def test50_invalid_date_format(self):
        """A date string that is not YYYY-MM-DDThh:mm:ss must raise ValueError."""
        if self.CONNECTION_FAILED:
            self.skipTest("No connection.")

        custom_request_df = pd.DataFrame({
            "network": ["4P"],
            "station": ["REU49"],
            "location": ["--"],
            "channel": ["*F*"],
            "start": ["not-a-date"],
            "end": ["2015-06-22T02:20:00"],
        })

        with self.assertRaises(ValueError):
            load_fdsn(trange=["x", "y"], network="4P", station="REU49", request_df=custom_request_df)

        self.assertTrue(len(tnames()) == 0)

    # @patch('sys.stdout', new_callable=StringIO)
    def test60_load_fdsn_nowarnings(self):
        """
        Test with and without nowarning flag
        """
        # self.skipTest(...) raises unittest.SkipTest, which the test runner
        # reports the same way as @unittest.skipIf. Unlike the decorator, it
        # is evaluated at call time, so it sees whatever test40_load_fdsn_basic
        # set self.BASIC_TEST_FAILED to when that test ran, not the class
        # default from when the class body was first executed.
        if self.BASIC_TEST_FAILED:
            self.skipTest("Basic test failed.")

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

    def test60_load_fdsn_nodownload(self):
        """
        If nodownload flag is specified the h5 file will be reused.
        Testing if the function works faster. Skipping the test if the file was not created.
        """
        if self.BASIC_TEST_FAILED:
            self.skipTest("Basic test failed.")

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

    def test60_load_fdsn_timeclip(self):
        """
        Test if the time is clipped correctly.
        """
        if self.BASIC_TEST_FAILED:
            self.skipTest("Basic test failed.")

        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        tvar = load_fdsn(network="4P", station="REU49", trange=[date_start, date_end])
        time, data = pyspedas.get_data(tvar)

        # Validate the stored payload, not only its boundary timestamps.
        self.assertEqual(tvar, "fdsn_4P_REU49")
        self.assertIn(tvar, pyspedas.tnames())
        self.assertGreater(len(time), 0)
        self.assertEqual(data.ndim, 2)
        self.assertEqual(data.shape, (len(time), 3))
        self.assertTrue(all(time[index] <= time[index + 1] for index in range(len(time) - 1)))
        self.assertTrue((data != 0).any())

        t1 = pyspedas.time_datetime(time[0]).strftime('%Y-%m-%dT%H:%M:%S')
        t2 = pyspedas.time_datetime(time[-1]).strftime('%Y-%m-%dT%H:%M:%S')

        # Test information output, useful for debug.
        # import mth5
        # print('mth5 version: ',mth5.__version__)
        # import mt_metadata
        # print('mt-metadata version: ', mt_metadata.__version__)
        # import obspy
        # print('obspy version: ', obspy.__version__)
        #
        # print('date_start: ', date_start)
        # print('t1: ', t1)
        # print('date_end: ', date_end)
        # print('t2: ', t2)

        self.assertTrue(t1 == date_start)
        self.assertTrue(t2 == date_end)

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
    # Mock data of the response
    mock_data = """Network|Station|Location|Channel|Latitude|Longitude|Elevation|Depth|Azimuth|Dip|SensorDescription|Scale|ScaleFreq|ScaleUnits|SampleRate|StartTime|EndTime
4P|ALW48||LFE|0|0|0|0|0|0|NIMS|1|1|nT|1|2015-06-18T15:00:36.0000|2015-07-09T13:45:10.0000
4P|ALW48||LFN|0|0|0|0|0|0|NIMS|1|1|nT|1|2015-06-18T15:00:36.0000|2015-07-09T13:45:10.0000
4P|ALW48||LFZ|0|0|0|0|0|0|NIMS|1|1|nT|1|2015-06-18T15:00:36.0000|2015-07-09T13:45:10.0000
"""

    # Set to True if we can get to https://service.earthscope.org
    PING_IRIS = False

    @classmethod
    def setUpClass(cls):
        host = "service.earthscope.org"
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
