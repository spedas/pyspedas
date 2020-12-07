
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    # failing due to the vars not loading into pytplot variables
    # def test_load_hep_data(self):
    #     hep_vars = pyspedas.erg.hep()
    #     self.assertTrue(data_exists('erg_hep_l2_FEDO_L'))
    #     self.assertTrue(data_exists('erg_hep_l2_FEDO_H'))

    # same as above
    # def test_load_xep_data(self):
    #     xep_vars = pyspedas.erg.xep()
    #     self.assertTrue(data_exists('erg_xep_l2_FEDO_SSD'))
    #     self.assertTrue(data_exists('erg_xep_l2_FEDO_GSO'))

    def test_load_orb_data(self):
        orb_vars = pyspedas.erg.orb()
        self.assertTrue(data_exists('erg_orb_l3_pos_eq_op'))
        self.assertTrue(data_exists('erg_orb_l3_pos_iono_north_op'))
        self.assertTrue(data_exists('erg_orb_l3_pos_iono_south_op'))
        self.assertTrue(data_exists('erg_orb_l3_pos_lmc_op'))

    def test_load_mgf_data(self):
        mgf_vars = pyspedas.erg.mgf(time_clip=True)
        self.assertTrue(data_exists('erg_mgf_l2_mag_8sec_sm'))

    def test_load_lepe_data(self):
        lepe_vars = pyspedas.erg.lepe()
        self.assertTrue(data_exists('erg_lepe_l2_FEDO'))

    def test_load_lepi_data(self):
        lepi_vars = pyspedas.erg.lepi()
        self.assertTrue(data_exists('erg_lepi_l2_FPDO'))
        self.assertTrue(data_exists('erg_lepi_l2_FHEDO'))
        self.assertTrue(data_exists('erg_lepi_l2_FODO'))

    def test_load_mepe_data(self):
        mepe_vars = pyspedas.erg.mepe()
        self.assertTrue(data_exists('erg_mepe_l2_FEDO'))

    def test_load_mepi_data(self):
        mepi_vars = pyspedas.erg.mepi()
        self.assertTrue(data_exists('erg_mepi_l2_FPDO'))
        self.assertTrue(data_exists('erg_mepi_l2_FHE2DO'))
        self.assertTrue(data_exists('erg_mepi_l2_FHEDO'))
        self.assertTrue(data_exists('erg_mepi_l2_FOPPDO'))

    def test_load_pwe_ofa_data(self):
        pwe_vars = pyspedas.erg.pwe_ofa()
        self.assertTrue(data_exists('erg_pwe_ofa_l2_E_spectra_132'))
        self.assertTrue(data_exists('erg_pwe_ofa_l2_quality_flag_e132'))
        self.assertTrue(data_exists('erg_pwe_ofa_l2_B_spectra_132'))
        self.assertTrue(data_exists('erg_pwe_ofa_l2_quality_flag_b132'))

    def test_load_pwe_efd_data(self):
        pwe_vars = pyspedas.erg.pwe_efd()
        self.assertTrue(data_exists('erg_pwe_efd_l2_Eu_dsi'))
        self.assertTrue(data_exists('erg_pwe_efd_l2_Ev_dsi'))
        self.assertTrue(data_exists('erg_pwe_efd_l2_Ev2_dsi'))
        self.assertTrue(data_exists('erg_pwe_efd_l2_Eu2_dsi'))

    def test_load_pwe_hfa_data(self):
        pwe_vars = pyspedas.erg.pwe_hfa()
        self.assertTrue(data_exists('erg_pwe_hfa_l2_spectra_eu'))
        self.assertTrue(data_exists('erg_pwe_hfa_l2_spectra_ev'))
        self.assertTrue(data_exists('erg_pwe_hfa_l2_spectra_bgamma'))
        self.assertTrue(data_exists('erg_pwe_hfa_l2_spectra_esum'))
        self.assertTrue(data_exists('erg_pwe_hfa_l2_spectra_er'))

    def test_downloadonly(self):
        files = pyspedas.erg.mgf(downloadonly=True, trange=['2017-03-27', '2017-03-28'])
        self.assertTrue(os.path.exists(files[0]))

if __name__ == '__main__':
    unittest.main()