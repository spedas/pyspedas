"""Satellite loader integration tests against the SPDF Arase mirror."""
import tempfile
import unittest
from unittest.mock import patch

import pyspedas
from pyspedas.projects.erg.config import CONFIG
from pyspedas.tplot_tools import data_exists, del_data, tplot_names

class LoadTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # A fresh cache ensures these tests really exercise SPDF URLs.
        cls.cache = tempfile.TemporaryDirectory()
        cls.config_patch = patch.dict(CONFIG, {
            'satellite_remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/arase/',
            'local_data_dir': cls.cache.name,
            'no_download': False,
        })
        cls.config_patch.start()

    @classmethod
    def tearDownClass(cls):
        cls.config_patch.stop()
        cls.cache.cleanup()
        del_data()

    def test_load_att_data(self):
        del_data()
        att_vars = pyspedas.projects.erg.att(version='v03')
        tplot_names()
        self.assertTrue(data_exists('erg_att_sprate'))
        self.assertTrue(data_exists('erg_att_spphase'))
        self.assertTrue('erg_att_sprate' in att_vars)
        self.assertTrue('erg_att_spphase' in att_vars)

    def test_load_att_data_notplot(self):
        del_data()
        att_dict = pyspedas.projects.erg.att(notplot=True, version='v03')
        self.assertTrue('erg_att_sprate' in att_dict)
        self.assertTrue('erg_att_spphase' in att_dict)

    def test_load_hep_data(self):
        del_data()
        hep_vars = pyspedas.projects.erg.hep(version='v03_01', ror=False)
        self.assertTrue(data_exists('erg_hep_l2_FEDO_L'))
        self.assertTrue(data_exists('erg_hep_l2_FEDO_H'))
        self.assertTrue('erg_hep_l2_FEDO_L' in hep_vars)
        self.assertTrue('erg_hep_l2_FEDO_H' in hep_vars)

    def test_load_xep_l2_omniflux_data(self):
        del_data()
        xep_vars = pyspedas.projects.erg.xep(level='l2', version='v01_00', ror=False)
        self.assertTrue('erg_xep_l2_FEDO_SSD' in xep_vars)
        self.assertTrue(data_exists('erg_xep_l2_FEDO_SSD'))

    def test_load_orb_data(self):
        del_data()
        orb_vars = pyspedas.projects.erg.orb(version='v05', ror=False)
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

    def test_load_mgf_data(self):
        del_data()
        mgf_vars = pyspedas.projects.erg.mgf(time_clip=True, ror=False)
        self.assertTrue(data_exists('erg_mgf_l2_mag_8sec_sm'))
        self.assertTrue('erg_mgf_l2_mag_8sec_sm' in mgf_vars)

    def test_load_lepe_data_latest(self):
        del_data()
        lepe_vars = pyspedas.projects.erg.lepe(ror=False)
        self.assertTrue(data_exists('erg_lepe_l2_omniflux_FEDO'))
        self.assertTrue('erg_lepe_l2_omniflux_FEDO' in lepe_vars)

    def test_load_lepi_data(self):
        del_data()
        lepi_vars = pyspedas.projects.erg.lepi(version='v03_00', ror=False)
        self.assertTrue(data_exists('erg_lepi_l2_omniflux_FPDO'))
        self.assertTrue(data_exists('erg_lepi_l2_omniflux_FHEDO'))
        self.assertTrue(data_exists('erg_lepi_l2_omniflux_FODO'))
        self.assertTrue('erg_lepi_l2_omniflux_FPDO' in lepi_vars)
        self.assertTrue('erg_lepi_l2_omniflux_FHEDO' in lepi_vars)
        self.assertTrue('erg_lepi_l2_omniflux_FODO' in lepi_vars)

    def test_load_mepe_data(self):
        del_data()
        mepe_vars = pyspedas.projects.erg.mepe(version='v01_02', ror=False)
        self.assertTrue(data_exists('erg_mepe_l2_omniflux_FEDO'))
        self.assertTrue('erg_mepe_l2_omniflux_FEDO' in mepe_vars)

    def test_load_mepi_nml_data(self):
        del_data()
        mepi_vars = pyspedas.projects.erg.mepi_nml(ror=False)
        self.assertTrue(data_exists('erg_mepi_l2_omniflux_epoch_tof'))
        self.assertTrue('erg_mepi_l2_omniflux_epoch_tof' in mepi_vars)

    def test_load_mepi_tof_data(self):
        del_data()
        mepi_vars = pyspedas.projects.erg.mepi_tof(ror=False)
        self.assertTrue(data_exists('erg_mepi_l2_tofflux_FPDU'))
        self.assertTrue(data_exists('erg_mepi_l2_tofflux_FODU'))
        self.assertTrue('erg_mepi_l2_tofflux_FPDU' in mepi_vars)
        self.assertTrue('erg_mepi_l2_tofflux_FODU' in mepi_vars)

    def test_load_pwe_ofa_data(self):
        del_data()
        pwe_vars = pyspedas.projects.erg.pwe_ofa(ror=False)
        self.assertTrue(data_exists('erg_pwe_ofa_l2_spec_E_spectra_132'))
        self.assertTrue(data_exists('erg_pwe_ofa_l2_spec_B_spectra_132'))
        self.assertTrue('erg_pwe_ofa_l2_spec_E_spectra_132' in pwe_vars)
        self.assertTrue('erg_pwe_ofa_l2_spec_B_spectra_132' in pwe_vars)

    def test_load_pwe_efd_data(self):
        del_data()
        pwe_vars = pyspedas.projects.erg.pwe_efd(ror=False)
        self.assertTrue(data_exists('erg_pwe_efd_l2_E_spin_Eu_dsi'))
        self.assertTrue('erg_pwe_efd_l2_E_spin_Eu_dsi' in pwe_vars)

    def test_load_pwe_efd_e64hz_data(self):
        del_data()
        pwe_vars = pyspedas.projects.erg.pwe_efd(datatype='E64Hz', ror=False)
        self.assertTrue(data_exists('erg_pwe_efd_l2_E64Hz_dsi_Ex_waveform'))
        self.assertTrue('erg_pwe_efd_l2_E64Hz_dsi_Ex_waveform' in pwe_vars)

    def test_load_pwe_hfa_data(self):
        del_data()
        pwe_vars = pyspedas.projects.erg.pwe_hfa(version='v01_02', ror=False)
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
        pwe_vars = pyspedas.projects.erg.pwe_wfc(trange=['2017-04-01/12:00:00', '2017-04-01/13:00:00'], ror=False)
        self.assertTrue(data_exists('erg_pwe_wfc_l2_e_65khz_Ex_waveform'))
        self.assertTrue('erg_pwe_wfc_l2_e_65khz_Ex_waveform' in pwe_vars)

    def test_load_pwe_wfc_spec_data(self):
        del_data()
        pwe_vars = pyspedas.projects.erg.pwe_wfc(trange=['2017-04-01/12:00:00', '2017-04-01/13:00:00'], datatype='spec', ror=False)
        self.assertTrue(data_exists('erg_pwe_wfc_l2_e_65khz_E_spectra'))
        self.assertTrue('erg_pwe_wfc_l2_e_65khz_E_spectra' in pwe_vars)

    def test_latest_version(self):
        for instrument, variable in [
            ('att', 'erg_att_sprate'),
            ('mepe', 'erg_mepe_l2_omniflux_FEDO'),
            ('pwe_hfa', 'erg_pwe_hfa_l2_low_spectra_eu'),
        ]:
            with self.subTest(instrument=instrument):
                del_data()
                kwargs = {} if instrument == 'att' else {'ror': False}
                names = getattr(pyspedas.projects.erg, instrument)(version=None, **kwargs)
                self.assertIn(variable, names)
                self.assertTrue(data_exists(variable))

if __name__ == '__main__':
    unittest.main()
