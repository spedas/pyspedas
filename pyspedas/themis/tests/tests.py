
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_state_data(self):
        data = pyspedas.themis.state()
        self.assertTrue(data_exists('thc_pos'))
        self.assertTrue(data_exists('thc_vel'))
        self.assertTrue(data_exists('thc_pos_gsm'))
        self.assertTrue(data_exists('thc_vel_gse'))

    def test_load_gmag_data(self):
        data = pyspedas.themis.gmag()
        self.assertTrue(data_exists('thg_mag_amer'))
        self.assertTrue(data_exists('thg_mag_kil'))
        self.assertTrue(data_exists('thg_mag_eagl'))
        self.assertTrue(data_exists('thg_mag_leth'))
        self.assertTrue(data_exists('thg_mag_inuv'))
        self.assertTrue(data_exists('thg_mag_wrth'))

    def test_load_sst_data(self):
        data = pyspedas.themis.sst()
        self.assertTrue(data_exists('thc_psif_en_eflux'))
        self.assertTrue(data_exists('thc_psif_density'))
        self.assertTrue(data_exists('thc_psif_avgtemp'))
        self.assertTrue(data_exists('thc_psif_vthermal'))

    def test_load_fgm_data(self):
        data = pyspedas.themis.fgm()
        self.assertTrue(data_exists('thc_fgs_btotal'))
        self.assertTrue(data_exists('thc_fgs_gse'))
        self.assertTrue(data_exists('thc_fgs_gsm'))

    def test_load_fit_data(self):
        data = pyspedas.themis.fit()
        self.assertTrue(data_exists('thc_fgs_gse'))
        self.assertTrue(data_exists('thc_fgs_gsm'))

    def test_load_esa_data(self):
        data = pyspedas.themis.esa()
        self.assertTrue(data_exists('thc_peif_density'))
        self.assertTrue(data_exists('thc_peif_avgtemp'))
        self.assertTrue(data_exists('thc_peif_en_eflux'))
        self.assertTrue(data_exists('thc_peif_flux'))

    def test_load_fft_data(self):
        data = pyspedas.themis.fft()
        self.assertTrue(data_exists('thc_ffp_16_edc34'))
        self.assertTrue(data_exists('thc_ffp_16_edc56'))
        self.assertTrue(data_exists('thc_ffp_16_scm2'))

    def test_load_fft_l1_data(self):
        data = pyspedas.themis.fft(level='l1')
        self.assertTrue(data_exists('thc_ffp_16'))
        self.assertTrue(data_exists('thc_ffw_16'))

    def test_load_fbk_data(self):
        data = pyspedas.themis.fbk()
        self.assertTrue(data_exists('thc_fb_hff'))
        self.assertTrue(data_exists('thc_fb_edc12'))
        self.assertTrue(data_exists('thc_fb_scm1'))

    def test_load_mom_data(self):
        data = pyspedas.themis.mom()
        self.assertTrue(data_exists('thc_peim_density'))
        self.assertTrue(data_exists('thc_peim_ptot'))
        self.assertTrue(data_exists('thc_peim_flux'))
        self.assertTrue(data_exists('thc_peim_eflux'))
        self.assertTrue(data_exists('thc_peim_velocity_gse'))

    # the following isn't working for some reason
    # def test_load_gmom_data(self):
    #     data = pyspedas.themis.gmom()
    #     self.assertTrue(data_exists(''))

    def test_load_scm_data(self):
        data = pyspedas.themis.scm()
        self.assertTrue(data_exists('thc_scf_btotal'))
        self.assertTrue(data_exists('thc_scp_gsm'))
        self.assertTrue(data_exists('thc_scf_gsm'))

    def test_load_scm_l1_data(self):
        data = pyspedas.themis.scm(level='l1')
        self.assertTrue(data_exists('thc_scf'))
        self.assertTrue(data_exists('thc_scp'))
        self.assertTrue(data_exists('thc_scw'))

    def test_load_efi_l1_data(self):
        data = pyspedas.themis.efi(level='l1')
        self.assertTrue(data_exists('thc_eff'))
        self.assertTrue(data_exists('thc_efp'))
        self.assertTrue(data_exists('thc_efw'))
        self.assertTrue(data_exists('thc_vaf'))

    def test_load_efi_data(self):
        data = pyspedas.themis.efi(time_clip=True)
        self.assertTrue(data_exists('thc_eff_e12_efs'))
        self.assertTrue(data_exists('thc_eff_e34_efs'))

    def test_downloadonly(self):
        files = pyspedas.themis.efi(downloadonly=True,
                                    trange=['2014-2-15', '2014-2-16'])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()
