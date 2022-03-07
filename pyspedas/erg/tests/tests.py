
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_hep_data(self):
        hep_vars = pyspedas.erg.hep()
        self.assertTrue(data_exists('erg_hep_l2_FEDO_L'))
        self.assertTrue(data_exists('erg_hep_l2_FEDO_H'))

    def test_load_xep_data(self):
        xep_vars = pyspedas.erg.xep()
        self.assertTrue(data_exists('erg_xep_l2_FEDO_SSD'))

    def test_load_orb_data(self):
        orb_vars = pyspedas.erg.orb()
        self.assertTrue(data_exists('erg_orb_l2_pos_gse'))
        self.assertTrue(data_exists('erg_orb_l2_pos_gsm'))
        self.assertTrue(data_exists('erg_orb_l2_pos_sm'))
        self.assertTrue(data_exists('erg_orb_l2_vel_gse'))
        self.assertTrue(data_exists('erg_orb_l2_vel_gsm'))
        self.assertTrue(data_exists('erg_orb_l2_vel_sm'))

    def test_load_l3_orb_data(self):
        orb_vars = pyspedas.erg.orb(level='l3')
        self.assertTrue(data_exists('erg_orb_l3_pos_eq_op'))
        self.assertTrue(data_exists('erg_orb_l3_pos_iono_north_op'))
        self.assertTrue(data_exists('erg_orb_l3_pos_iono_south_op'))

    def test_load_mgf_data(self):
        mgf_vars = pyspedas.erg.mgf(time_clip=True)
        self.assertTrue(data_exists('erg_mgf_l2_mag_8sec_sm'))

    def test_load_lepe_data(self):
        lepe_vars = pyspedas.erg.lepe()
        self.assertTrue(data_exists('erg_lepe_l2_omniflux_FEDO'))

    def test_load_lepi_data(self):
        lepi_vars = pyspedas.erg.lepi()
        self.assertTrue(data_exists('erg_lepi_l2_omniflux_FPDO'))
        self.assertTrue(data_exists('erg_lepi_l2_omniflux_FHEDO'))
        self.assertTrue(data_exists('erg_lepi_l2_omniflux_FODO'))

    def test_load_mepe_data(self):
        mepe_vars = pyspedas.erg.mepe()
        self.assertTrue(data_exists('erg_mepe_l2_omniflux_FEDO'))

    def test_load_mepi_data(self):
        mepi_vars = pyspedas.erg.mepi_nml()
        self.assertTrue(data_exists('erg_mepi_l2_omniflux_epoch_tof'))
        mepi_vars = pyspedas.erg.mepi_tof()
        self.assertTrue(data_exists('erg_mepi_l2_tofflux_FPDU'))
        self.assertTrue(data_exists('erg_mepi_l2_tofflux_FODU'))

    def test_load_pwe_ofa_data(self):
        pwe_vars = pyspedas.erg.pwe_ofa()
        self.assertTrue(data_exists('erg_pwe_ofa_l2_spec_E_spectra_132'))
        self.assertTrue(data_exists('erg_pwe_ofa_l2_spec_B_spectra_132'))

    # test is failing as of 26 Jan 2022
    # def test_load_pwe_efd_data(self):
    #     pwe_vars = pyspedas.erg.pwe_efd()
    #     self.assertTrue(data_exists('erg_pwe_efd_l2_E_spin_Eu_dsi'))
    #     self.assertTrue(data_exists('erg_pwe_efd_l2_E_spin_Ev_dsi'))
    #     self.assertTrue(data_exists('erg_pwe_efd_l2_E_spin_Ev1_dsi'))
    #     self.assertTrue(data_exists('erg_pwe_efd_l2_E_spin_Eu2_dsi'))

    def test_load_pwe_hfa_data(self):
        pwe_vars = pyspedas.erg.pwe_hfa()
        self.assertTrue(data_exists('erg_pwe_hfa_l2_low_spectra_eu'))
        self.assertTrue(data_exists('erg_pwe_hfa_l2_low_spectra_ev'))
        self.assertTrue(data_exists('erg_pwe_hfa_l2_low_spectra_esum'))
        self.assertTrue(data_exists('erg_pwe_hfa_l2_low_spectra_er'))

    def test_downloadonly(self):
        files = pyspedas.erg.mgf(downloadonly=True, trange=['2017-03-27', '2017-03-28'])
        self.assertTrue(os.path.exists(files[0]))

if __name__ == '__main__':
    unittest.main()