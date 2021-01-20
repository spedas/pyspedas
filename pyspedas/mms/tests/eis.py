import unittest
import numpy as np
from pyspedas import mms_load_eis, mms_eis_pad
from pyspedas.utilities.data_exists import data_exists

class EISTestCases(unittest.TestCase):
    def test_pad_extof_srvy(self):
        mms_load_eis(datatype='extof')
        mms_eis_pad(datatype='extof')
        self.assertTrue(data_exists('mms1_epd_eis_extof_46-10489keV_proton_flux_omni_pad_spin'))
        self.assertTrue(data_exists('mms1_epd_eis_extof_46-10489keV_proton_flux_omni_pad'))

    def test_pad_extof_srvy_probe(self):
        mms_load_eis(probe=4)
        mms_eis_pad(probe=4)
        self.assertTrue(data_exists('mms4_epd_eis_extof_44-1315keV_proton_flux_omni_pad_spin'))
        self.assertTrue(data_exists('mms4_epd_eis_extof_44-1315keV_proton_flux_omni_pad'))

    def test_pad_extof_brst(self):
        mms_load_eis(probe=4, datatype='extof', data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:07'])
        mms_eis_pad(probe=4, datatype='extof', data_rate='brst')
        self.assertTrue(data_exists('mms4_epd_eis_brst_extof_52-878keV_proton_flux_omni_pad_spin'))
        self.assertTrue(data_exists('mms4_epd_eis_brst_extof_52-878keV_proton_flux_omni_pad'))


if __name__ == '__main__':
    unittest.main()