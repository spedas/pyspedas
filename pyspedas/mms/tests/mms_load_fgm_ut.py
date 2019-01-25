
import sys
import os 

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../')
import unittest

from pyspedas.mms import mms_load_fgm
from pyspedas.utilities.data_exists import data_exists

class FGMLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_fgm()
        self.assertTrue(data_exists('mms1_fgm_b_gse_srvy_l2'))

    def test_load_multiple_sc(self):
        data = mms_load_fgm(probes=['1', '2', '3', '4'])
        self.assertTrue(data_exists('mms1_fgm_b_gse_srvy_l2'))
        self.assertTrue(data_exists('mms2_fgm_b_gse_srvy_l2'))
        self.assertTrue(data_exists('mms3_fgm_b_gse_srvy_l2'))
        self.assertTrue(data_exists('mms4_fgm_b_gse_srvy_l2'))

    def test_load_brst_data(self):
        data = mms_load_fgm(data_rates='brst', trange=['2015-10-16/13:00', '2015-10-16/13:10'])
        self.assertTrue(data_exists('mms1_fgm_b_gse_brst_l2'))

if __name__ == '__main__':
    unittest.main()