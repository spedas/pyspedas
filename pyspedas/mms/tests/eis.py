import unittest
import numpy as np
from pyspedas import mms_load_eis, mms_eis_pad
from ...utilities.data_exists import data_exists

class EISTestCases(unittest.TestCase):
    def test_pad_extof_srvy(self):
        mms_load_eis(datatype='extof')
        mms_eis_pad(datatype='extof')
        self.assertTrue(data_exists('mms1_epd_eis_extof_56-535keV_proton_flux_omni_pad_spin'))
        self.assertTrue(data_exists('mms1_epd_eis_extof_56-535keV_proton_flux_omni_pad'))

    def test_pad_extof_srvy_probe(self):
        mms_load_eis(probe=4)
        mms_eis_pad(probe=4)
        self.assertTrue(data_exists('mms4_epd_eis_extof_56-535keV_proton_flux_omni_pad_spin'))
        self.assertTrue(data_exists('mms4_epd_eis_extof_56-535keV_proton_flux_omni_pad'))
