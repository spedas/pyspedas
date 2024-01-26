import unittest

import h5py
import pandas as pd

import pyspedas
import pytplot
from mth5.clients.make_mth5 import FDSN
from pyspedas.mth5.load_fdsn import load_fdsn


class TestMTH5LoadFDSN(unittest.TestCase):
    # Flag to check if there is any open instances of h5 files
    H5OPEN = False

    @classmethod
    def setUpClass(cls):
        # Test if there is any open instances of h5 files
        # This case may not work because tests are executed in a different console where h5 reference may not exist.
        o = h5py.h5f.get_obj_ids(types=h5py.h5f.OBJ_FILE)
        cls.H5OPEN = len(o) > 0

    def setUp(self):
        pass

    def test_load_fdsn_notrange(self):
        """
        Testing the load_fdsn function without a trange.
        The log message should be printed.
        """
        with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
            load_fdsn(network="4P", station="REU49")
        self.assertIn('trange not specified', cm.output[0])
        self.assertFalse('fdsn_4P_REU49' in pytplot.tnames())

    def test_load_fdsn_nonetwork(self):
        """
        Test loading data without specifying a network
        """
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
            load_fdsn(station='REU49', trange=[date_start, date_end])
        self.assertIn('Network not specified', cm.output[0])
        self.assertFalse('fdsn_4P_REU49' in pytplot.tnames())

    def test_load_fdsn_nostation(self):
        """
        Test loading data without specifying a station
        """
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'

        with self.assertLogs(logger=pyspedas.logger, level='ERROR') as cm:
            load_fdsn(network='4P', trange=[date_start, date_end])
        self.assertIn('Station not specified', cm.output[0])
        self.assertFalse('fdsn_4P_REU49' in pytplot.tnames())



    def test_load_fdsn_example(self):
        date_start = '2015-06-22T01:45:00'
        date_end = '2015-06-22T02:20:00'
        load_fdsn(network="4P", station="REU49", trange=[date_start, date_end])
        load_fdsn(network="4P", station="GAW50", trange=[date_start, date_end])

        self.assertTrue('fdsn_4P_REU49' in pytplot.tnames())
        self.assertTrue('fdsn_4P_GAW50' in pytplot.tnames())


    # This test seems to be obsolete
    @unittest.skipIf(H5OPEN, "Open h5 files detected. Close all the h5 references before runing this test")
    def test_load_fdsn_h5_file_error(self):
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

    def test_load_fdsn_no_data(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
