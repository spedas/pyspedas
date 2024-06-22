
import os
import unittest
from pytplot import data_exists, del_data, tplot_names

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_att_data(self):
        del_data()
        att_vars = pyspedas.erg.att()
        self.assertTrue(data_exists('erg_att_sprate'))
        self.assertTrue(data_exists('erg_att_spphase'))
        self.assertTrue('erg_att_sprate' in att_vars)
        self.assertTrue('erg_att_spphase' in att_vars)

    def test_load_hep_data(self):
        del_data()
        hep_vars = pyspedas.erg.hep()
        self.assertTrue(data_exists('erg_hep_l2_FEDO_L'))
        self.assertTrue(data_exists('erg_hep_l2_FEDO_H'))
        self.assertTrue('erg_hep_l2_FEDO_L' in hep_vars)
        self.assertTrue('erg_hep_l2_FEDO_H' in hep_vars)

    def test_load_hep_3dflux(self):
        del_data()
        hep_vars = pyspedas.erg.hep(datatype='3dflux')
        print(hep_vars)
        tplot_names()

    def test_load_xep_data(self):
        del_data()
        xep_vars = pyspedas.erg.xep()
        self.assertTrue(data_exists('erg_xep_l2_FEDO_SSD'))
        self.assertTrue('erg_xep_l2_FEDO_SSD' in xep_vars)

    def test_load_orb_data(self):
        del_data()
        orb_vars = pyspedas.erg.orb()
        self.assertTrue(data_exists('erg_orb_l2_pos_gse'))
        self.assertTrue(data_exists('erg_orb_l2_pos_gsm'))
        self.assertTrue(data_exists('erg_orb_l2_pos_sm'))
        self.assertTrue(data_exists('erg_orb_l2_vel_gse'))
        self.assertTrue(data_exists('erg_orb_l2_vel_gsm'))
        self.assertTrue(data_exists('erg_orb_l2_vel_sm'))
        self.assertTrue('erg_orb_l2_pos_gse' in orb_vars)
        self.assertTrue('erg_orb_l2_pos_gsm' in orb_vars)
        self.assertTrue('erg_orb_l2_pos_sm' in orb_vars)
        self.assertTrue('erg_orb_l2_vel_gse' in orb_vars)
        self.assertTrue('erg_orb_l2_vel_gsm' in orb_vars)
        self.assertTrue('erg_orb_l2_vel_sm' in orb_vars)

    def test_load_l3_orb_data(self):
        del_data()
        orb_vars = pyspedas.erg.orb(level='l3')
        self.assertTrue(data_exists('erg_orb_l3_pos_eq_op'))
        self.assertTrue(data_exists('erg_orb_l3_pos_iono_north_op'))
        self.assertTrue(data_exists('erg_orb_l3_pos_iono_south_op'))
        self.assertTrue('erg_orb_l3_pos_eq_op' in orb_vars)
        self.assertTrue('erg_orb_l3_pos_iono_north_op' in orb_vars)
        self.assertTrue('erg_orb_l3_pos_iono_south_op' in orb_vars)

    def test_load_mgf_data(self):
        del_data()
        mgf_vars = pyspedas.erg.mgf(time_clip=True)
        self.assertTrue(data_exists('erg_mgf_l2_mag_8sec_sm'))
        self.assertTrue('erg_mgf_l2_mag_8sec_sm' in mgf_vars)

    def test_load_lepe_data(self):
        del_data()
        lepe_vars = pyspedas.erg.lepe()
        self.assertTrue(data_exists('erg_lepe_l2_omniflux_FEDO'))
        self.assertTrue('erg_lepe_l2_omniflux_FEDO' in lepe_vars)

    def test_load_lepe_3dflux(self):
        del_data()
        lepe_vars = pyspedas.erg.lepe(datatype='3dflux')
        print(lepe_vars)
        tplot_names()

    def test_load_lepi_data(self):
        del_data()
        lepi_vars = pyspedas.erg.lepi()
        self.assertTrue(data_exists('erg_lepi_l2_omniflux_FPDO'))
        self.assertTrue(data_exists('erg_lepi_l2_omniflux_FHEDO'))
        self.assertTrue(data_exists('erg_lepi_l2_omniflux_FODO'))
        self.assertTrue('erg_lepi_l2_omniflux_FPDO' in lepi_vars)
        self.assertTrue('erg_lepi_l2_omniflux_FHEDO' in lepi_vars)
        self.assertTrue('erg_lepi_l2_omniflux_FODO' in lepi_vars)

    def test_load_mepe_data(self):
        del_data()
        mepe_vars = pyspedas.erg.mepe()
        self.assertTrue(data_exists('erg_mepe_l2_omniflux_FEDO'))
        self.assertTrue('erg_mepe_l2_omniflux_FEDO' in mepe_vars)

    def test_load_mepe_3dflux(self):
        del_data()
        mepe_vars = pyspedas.erg.mepe(datatype='3dflux')
        print(mepe_vars)
        tplot_names()

    def test_load_mepi_data(self):
        del_data()
        mepi_vars = pyspedas.erg.mepi_nml()
        self.assertTrue(data_exists('erg_mepi_l2_omniflux_epoch_tof'))
        self.assertTrue('erg_mepi_l2_omniflux_epoch_tof' in mepi_vars)
        mepi_vars = pyspedas.erg.mepi_tof()
        self.assertTrue(data_exists('erg_mepi_l2_tofflux_FPDU'))
        self.assertTrue(data_exists('erg_mepi_l2_tofflux_FODU'))
        self.assertTrue('erg_mepi_l2_tofflux_FPDU' in mepi_vars)
        self.assertTrue('erg_mepi_l2_tofflux_FODU' in mepi_vars)

    def test_load_pwe_ofa_data(self):
        del_data()
        pwe_vars = pyspedas.erg.pwe_ofa()
        self.assertTrue(data_exists('erg_pwe_ofa_l2_spec_E_spectra_132'))
        self.assertTrue(data_exists('erg_pwe_ofa_l2_spec_B_spectra_132'))
        self.assertTrue('erg_pwe_ofa_l2_spec_E_spectra_132' in pwe_vars)
        self.assertTrue('erg_pwe_ofa_l2_spec_B_spectra_132' in pwe_vars)

    def test_load_pwe_efd_data(self):
        del_data()
        pwe_vars = pyspedas.erg.pwe_efd()
        self.assertTrue(data_exists('erg_pwe_efd_l2_E_spin_Eu_dsi'))
        self.assertTrue(data_exists('erg_pwe_efd_l2_E_spin_Ev_dsi'))
        self.assertTrue(data_exists('erg_pwe_efd_l2_E_spin_Ev1_dsi'))
        self.assertTrue(data_exists('erg_pwe_efd_l2_E_spin_Eu2_dsi'))
        self.assertTrue('erg_pwe_efd_l2_E_spin_Eu_dsi' in pwe_vars)
        self.assertTrue('erg_pwe_efd_l2_E_spin_Ev_dsi' in pwe_vars)
        self.assertTrue('erg_pwe_efd_l2_E_spin_Ev1_dsi' in pwe_vars)
        self.assertTrue('erg_pwe_efd_l2_E_spin_Eu2_dsi' in pwe_vars)

    def test_load_pwe_hfa_data(self):
        del_data()
        pwe_vars = pyspedas.erg.pwe_hfa()
        self.assertTrue(data_exists('erg_pwe_hfa_l2_low_spectra_eu'))
        self.assertTrue(data_exists('erg_pwe_hfa_l2_low_spectra_ev'))
        self.assertTrue(data_exists('erg_pwe_hfa_l2_low_spectra_esum'))
        self.assertTrue(data_exists('erg_pwe_hfa_l2_low_spectra_er'))
        self.assertTrue('erg_pwe_hfa_l2_low_spectra_eu' in pwe_vars)
        self.assertTrue('erg_pwe_hfa_l2_low_spectra_ev' in pwe_vars)
        self.assertTrue('erg_pwe_hfa_l2_low_spectra_esum' in pwe_vars)
        self.assertTrue('erg_pwe_hfa_l2_low_spectra_er' in pwe_vars)

    def test_load_pwe_wfc_data(self):
        del_data()
        pwe_vars = pyspedas.erg.pwe_wfc(trange=['2017-04-01/12:00:00', '2017-04-01/13:00:00'])
        self.assertTrue(data_exists('erg_pwe_wfc_l2_e_65khz_Ex_waveform'))
        self.assertTrue('erg_pwe_wfc_l2_e_65khz_Ex_waveform' in pwe_vars)

    def test_downloadonly(self):
        del_data()
        files = pyspedas.erg.mgf(downloadonly=True, trange=['2017-03-27', '2017-03-28'])
        self.assertTrue(os.path.exists(files[0]))

if __name__ == '__main__':
    unittest.main()