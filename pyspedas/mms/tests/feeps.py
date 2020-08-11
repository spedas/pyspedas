import unittest
import numpy as np
from ..feeps.mms_read_feeps_sector_masks_csv import mms_read_feeps_sector_masks_csv
from pyspedas import mms_load_feeps, mms_feeps_pad
from ...utilities.data_exists import data_exists

class FEEPSTestCases(unittest.TestCase):
    def test_pad_ions_brst(self):
        mms_load_feeps(probe=4, data_rate='brst', datatype='ion', trange=['2015-10-01/10:48:16', '2015-10-01/10:49:16'])
        mms_feeps_pad(probe=4, data_rate='brst', datatype='ion', angles_from_bfield=True)
        self.assertTrue(data_exists('mms4_epd_feeps_brst_l2_ion_intensity_70-600keV_pad'))
        self.assertTrue(data_exists('mms4_epd_feeps_brst_l2_ion_intensity_70-600keV_pad_spin'))

    def test_pad_ions_srvy(self):
        mms_load_feeps(probe=4, datatype='ion', trange=['2015-10-01/10:48:16', '2015-10-01/10:49:16'])
        mms_feeps_pad(probe=4, datatype='ion')
        self.assertTrue(data_exists('mms4_epd_feeps_srvy_l2_ion_intensity_70-600keV_pad'))
        self.assertTrue(data_exists('mms4_epd_feeps_srvy_l2_ion_intensity_70-600keV_pad_spin'))

    def test_pad_electrons_srvy(self):
        mms_load_feeps()
        mms_feeps_pad()
        self.assertTrue(data_exists('mms1_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad_spin'))
        self.assertTrue(data_exists('mms1_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad'))

    def test_pad_electrons_srvy_probe(self):
        mms_load_feeps(probe=4)
        mms_feeps_pad(probe=4)
        self.assertTrue(data_exists('mms4_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad_spin'))
        self.assertTrue(data_exists('mms4_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad'))

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

if __name__ == '__main__':
    unittest.main()