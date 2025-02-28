import unittest
import logging
from ..feeps_tools.mms_read_feeps_sector_masks_csv import mms_read_feeps_sector_masks_csv
from pyspedas import mms_load_feeps, mms_feeps_pad
from pyspedas.projects.mms.feeps_tools.mms_feeps_gpd import mms_feeps_gpd
from pytplot import del_data, tplot, data_exists, get


class FEEPSTestCases(unittest.TestCase):
    def test_time_clip_regression(self):
        # regression test for time clipping bug with spin-averaged spectra
        mms_load_feeps(trange=['2015-12-15/10:00', '2015-12-15/12:00'], time_clip=True)
        data = get('mms1_epd_feeps_srvy_l2_electron_intensity_omni_spin')
        self.assertTrue(data.y[-1, :].sum() != 0.0)

    def test_log_filtering(self):
        # Ensure that log message filtering can be reliably enabled and disabled
        # Enable filtering
        saw_filtered_entry = False
        with self.assertLogs(level='WARNING') as cm:
            # Guarantee at least one warning is logged
            logging.warning("Dummy log entry")
            mms_load_feeps(trange=['2015-12-15/10:00', '2015-12-15/12:00'], filter_recvary_warnings=True)
            for log_output in cm.output:
                if  'record-varying' in log_output:
                    saw_filtered_entry = True
        self.assertFalse(saw_filtered_entry)
        # Disable filtering, ensure that filter from previous call was successfully removed
        saw_filtered_entry = False
        with self.assertLogs(level='WARNING') as cm:
            # Guarantee at least one warning is logged
            logging.warning("Dummy log entry")
            mms_load_feeps(trange=['2015-12-15/10:00', '2015-12-15/12:00'], filter_recvary_warnings=False)
            for log_output in cm.output:
                if 'record-varying' in log_output:
                    saw_filtered_entry = True
        self.assertTrue(saw_filtered_entry)

    def test_feeps_sitl(self):
        mms_load_feeps(datatype='electron', trange=['2016-11-23', '2016-11-24'], data_rate='srvy', probe=4,
                       level='sitl')
        self.assertTrue(data_exists('mms4_epd_feeps_srvy_sitl_electron_intensity_omni'))

    def test_feeps_pad_regression(self):
        """
        This is a regression test for a bug caused by the v7 of the FEEPS CDF files
        v7 CDFs have an extra dimension on the variables containing the pitch angle data
        """
        mms_load_feeps(datatype='electron', trange=['2016-11-23', '2016-11-24'], data_rate='srvy', probe=4)
        mms_feeps_pad(probe=4)
        self.assertTrue(data_exists('mms4_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad'))
        tplot('mms4_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad', display=False)
        del_data('*')

    def test_gyrophase_angles(self):
        mms_load_feeps(data_rate='brst', trange=['2017-07-11/22:34', '2017-07-11/22:34:25'], probe=3)
        mms_feeps_gpd(probe='3', energy=[61, 77], data_rate='brst')
        self.assertTrue(data_exists('mms3_epd_feeps_brst_l2_electron_intensity_61-77keV_gpd'))
        mms_feeps_gpd(probe='3', data_rate='brst')
        self.assertTrue(data_exists('mms3_epd_feeps_brst_l2_electron_intensity_50-500keV_gpd'))
        tplot(['mms3_epd_feeps_brst_l2_electron_intensity_61-77keV_gpd',
               'mms3_epd_feeps_brst_l2_electron_intensity_50-500keV_gpd'], display=False)

    def test_pad_ions_brst(self):
        mms_load_feeps(probe=4, data_rate='brst', datatype='ion', trange=['2015-10-01/10:48:16', '2015-10-01/10:49:16'])
        mms_feeps_pad(probe=4, data_rate='brst', datatype='ion', angles_from_bfield=True)
        self.assertTrue(data_exists('mms4_epd_feeps_brst_l2_ion_intensity_70-600keV_pad'))
        self.assertTrue(data_exists('mms4_epd_feeps_brst_l2_ion_intensity_70-600keV_pad_spin'))
        tplot(['mms4_epd_feeps_brst_l2_ion_intensity_70-600keV_pad',
               'mms4_epd_feeps_brst_l2_ion_intensity_70-600keV_pad_spin'], display=False)

    def test_pad_ions_srvy(self):
        mms_load_feeps(probe=4, datatype='ion', trange=['2015-10-01/10:48:16', '2015-10-01/10:49:16'])
        mms_feeps_pad(probe=4, datatype='ion')
        self.assertTrue(data_exists('mms4_epd_feeps_srvy_l2_ion_intensity_70-600keV_pad'))
        self.assertTrue(data_exists('mms4_epd_feeps_srvy_l2_ion_intensity_70-600keV_pad_spin'))
        tplot(['mms4_epd_feeps_srvy_l2_ion_intensity_70-600keV_pad',
               'mms4_epd_feeps_srvy_l2_ion_intensity_70-600keV_pad_spin'], display=False)

    def test_pad_electrons_srvy(self):
        mms_load_feeps()
        mms_feeps_pad()
        self.assertTrue(data_exists('mms1_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad_spin'))
        self.assertTrue(data_exists('mms1_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad'))
        tplot(['mms1_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad',
               'mms1_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad_spin'], display=False)

    def test_pad_electrons_srvy_probe(self):
        mms_load_feeps(probe=4)
        mms_feeps_pad(probe=4)
        self.assertTrue(data_exists('mms4_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad_spin'))
        self.assertTrue(data_exists('mms4_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad'))
        tplot(['mms4_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad',
               'mms4_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad_spin'], display=False)

    def test_electron_srvy_after_aug17(self):
        # there's a different set of active eyes after 16 August 2017
        # this test executes that code
        mms_load_feeps(probe=4, trange=['2017-12-01', '2017-12-02'])
        self.assertTrue(data_exists('mms4_epd_feeps_srvy_l2_electron_intensity_omni'))
        self.assertTrue(data_exists('mms4_epd_feeps_srvy_l2_electron_intensity_omni_spin'))
        tplot(['mms4_epd_feeps_srvy_l2_electron_intensity_omni',
               'mms4_epd_feeps_srvy_l2_electron_intensity_omni_spin'], display=False)

    def test_sector_masks(self):
        d = mms_read_feeps_sector_masks_csv(['2015-08-01', '2015-08-02'])
        self.assertTrue(d['mms4imaskt2'] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 58, 59, 60, 61, 62, 63])
        self.assertTrue(d['mms3imaskb3'] == [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48])
        self.assertTrue(d['mms4imaskt8'] == [0, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 57, 58, 59, 61])
        self.assertTrue(d['mms4imaskb4'] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63])
        self.assertTrue(d['mms4imaskt1'] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63])
        self.assertTrue(d['mms1imaskt2'] == [11, 12])
        self.assertTrue(d['mms3imaskb1'] == [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43])
        self.assertTrue(d['mms3imaskb5'] == [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61])
        self.assertTrue(d['mms1imaskt3'] == [22, 23, 24, 25, 26, 27, 28, 31, 32])
        d = mms_read_feeps_sector_masks_csv(['2016-08-01', '2016-08-02'])
        self.assertTrue(d['mms1imaskb4'] == [20, 21, 22, 23, 24, 25, 26, 27, 28, 37, 38, 47])
        self.assertTrue(d['mms4imaskb9'] == [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 53, 54, 55, 56])
        self.assertTrue(d['mms3imaskb9'] == [53, 54, 55, 56, 57])
        self.assertTrue(d['mms4imaskb7'] == [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43])
        self.assertTrue(d['mms3imaskb1'] == [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43])
        self.assertTrue(d['mms4imaskt9'] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 25, 26, 27, 28, 29, 30, 31, 32, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63])
        self.assertTrue(d['mms3imaskb8'] == [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45])
        d = mms_read_feeps_sector_masks_csv(['2017-08-01', '2017-08-02'])
        self.assertTrue(d['mms3imaskb9'] == [53, 54, 55, 56, 57, 58])
        self.assertTrue(d['mms2imaskt9'] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 53, 54, 60, 61, 62, 63])
        self.assertTrue(d['mms1imaskb6'] == [40, 41, 42, 49, 50, 51, 52, 53, 54, 57, 58])

    def test_all_sector_masks(self):
        # Ensure that all contamination sector CSV files are readable, with no trailing commas
        # or other formatting issues.  Update the file_times array in this test whenever new
        # CSVs are added.

        from pytplot import time_string

        file_times=[1447200000.0000000, # 11/11/2015
             1468022400.0000000, # 7/9/2016
             1477612800.0000000, # 10/28/2016
             1496188800.0000000, # 5/31/2017
             1506988800.0000000, # 10/3/2017
             1538697600.0000000, # 10/5/2018
             1642032000.0000000, # 1/13/2022
             1651795200.0000000, # 5/6/2022
             1660521600.0000000, # 8/15/2022
             1706832000.0000000, # 02/02/2024
             1721779200.0000000, # 07/24/2024
             1739664000.0000000] # 02/16/2025

        for ft in file_times:
            trange=[ft,ft+86400.0]
            logging.info("Reading files for: "+time_string(trange[0]))
            d = mms_read_feeps_sector_masks_csv(trange)
            self.assertTrue(d is not None)


if __name__ == '__main__':
    unittest.main()
