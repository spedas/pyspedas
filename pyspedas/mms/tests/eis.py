import unittest
import numpy as np
from pyspedas import mms_load_eis, mms_eis_pad
from pyspedas.utilities.data_exists import data_exists

class EISTestCases(unittest.TestCase):
    def test_pad_extof_srvy(self):
        mms_load_eis(datatype='extof')
        mms_eis_pad(datatype='extof')
        self.assertTrue(data_exists('mms1_epd_eis_srvy_l2_extof_46-10489keV_proton_flux_omni_pad_spin'))
        self.assertTrue(data_exists('mms1_epd_eis_srvy_l2_extof_46-10489keV_proton_flux_omni_pad'))
        self.assertTrue(data_exists('mms1_epd_eis_srvy_l2_extof_proton_flux_omni_spin'))
        self.assertTrue(data_exists('mms1_epd_eis_srvy_l2_extof_proton_flux_omni'))
        self.assertTrue(data_exists('mms1_epd_eis_srvy_l2_extof_oxygen_energy_range'))
        self.assertTrue(data_exists('mms1_epd_eis_srvy_l2_extof_proton_energy_range'))

    def test_pad_extof_srvy_probe(self):
        mms_load_eis(probe=4)
        mms_eis_pad(probe=4)
        self.assertTrue(data_exists('mms4_epd_eis_srvy_l2_extof_44-1315keV_proton_flux_omni_pad_spin'))
        self.assertTrue(data_exists('mms4_epd_eis_srvy_l2_extof_44-1315keV_proton_flux_omni_pad'))
        self.assertTrue(data_exists('mms4_epd_eis_srvy_l2_extof_proton_flux_omni_spin'))
        self.assertTrue(data_exists('mms4_epd_eis_srvy_l2_extof_proton_flux_omni'))
        self.assertTrue(data_exists('mms4_epd_eis_srvy_l2_extof_oxygen_energy_range'))
        self.assertTrue(data_exists('mms4_epd_eis_srvy_l2_extof_proton_energy_range'))

    def test_pad_extof_brst(self):
        mms_load_eis(probe=4, datatype='extof', data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:07'])
        mms_eis_pad(probe=4, datatype='extof', data_rate='brst')
        self.assertTrue(data_exists('mms4_epd_eis_brst_l2_extof_52-878keV_proton_flux_omni_pad_spin'))
        self.assertTrue(data_exists('mms4_epd_eis_brst_l2_extof_52-878keV_proton_flux_omni_pad'))
        self.assertTrue(data_exists('mms4_epd_eis_brst_l2_extof_proton_flux_omni'))
        self.assertTrue(data_exists('mms4_epd_eis_brst_l2_extof_proton_energy_range'))
        self.assertTrue(data_exists('mms4_epd_eis_brst_l2_extof_oxygen_energy_range'))
    
    def test_load_phxtof_data(self):
        data = mms_load_eis(trange=['2015-10-16', '2015-10-16/01:00'], datatype='phxtof')
        self.assertTrue(data_exists('mms1_epd_eis_srvy_l2_phxtof_proton_flux_omni'))
        self.assertTrue(data_exists('mms1_epd_eis_srvy_l2_phxtof_proton_t5_energy_dminus'))
        self.assertTrue(data_exists('mms1_epd_eis_srvy_l2_phxtof_proton_t5_energy_dplus'))

    def test_load_phxtof_spdf(self):
        data = mms_load_eis(trange=['2015-10-16/13:06', '2015-10-16/13:07'], datatype='phxtof', data_rate='brst', spdf=True)
        self.assertTrue(data_exists('mms1_epd_eis_brst_l2_phxtof_proton_flux_omni'))
        self.assertTrue(data_exists('mms1_epd_eis_brst_l2_phxtof_proton_t5_energy_dminus'))
        self.assertTrue(data_exists('mms1_epd_eis_brst_l2_phxtof_proton_t5_energy_dplus'))

    def test_load_extof_suffix(self):
        data = mms_load_eis(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', datatype='extof', suffix='_test')
        self.assertTrue(data_exists('mms1_epd_eis_brst_l2_extof_proton_flux_omni_test'))
        self.assertTrue(data_exists('mms1_epd_eis_brst_l2_extof_proton_t5_energy_dminus_test'))
        self.assertTrue(data_exists('mms1_epd_eis_brst_l2_extof_proton_t5_energy_dminus_test'))


if __name__ == '__main__':
    unittest.main()