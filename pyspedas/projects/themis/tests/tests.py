"""Test gmag and themis load functions."""
import os
import unittest
import logging
import pyspedas
import pytplot
from pytplot import data_exists, get_coords



class GmagTestCases(unittest.TestCase):
    """Test GMAG functions."""

    def test_get_group(self):
        """Get gmag stations of a group."""
        from pyspedas.projects.themis.ground.gmag import get_group
        self.assertTrue(get_group('ccnv') == ['epo'])

    def test_gmag_list(self):
        """Get gmag list of stations."""
        from pyspedas.projects.themis.ground.gmag import gmag_list
        l = gmag_list()
        for site in ['abk', 'akul', 'amd', 'amer', 'amk']:
            self.assertTrue(site in l)

    def test_gmag_groups(self):
        """Get gmag groups."""
        from pyspedas.projects.themis.ground.gmag import gmag_groups
        gmag_table = gmag_groups()
        keylist = list(gmag_table.keys())
        for group in ['kyoto', 'sgu', 'autx', 'ae', 'aari']:
            self.assertTrue(group in keylist)

    def test_check_gmag(self):
        """Check a gmag station."""
        from pyspedas.projects.themis.ground.gmag import check_gmag
        self.assertTrue(check_gmag('ccnv') == 1)
        self.assertTrue(check_gmag('abcd') == 0)

    def test_load_gmag_data(self):
        """Load gmag."""
        pyspedas.projects.themis.gmag(varnames=['thg_mag_amer'], sites='amer')
        self.assertTrue(data_exists('thg_mag_amer'))


class LoadTestCases(unittest.TestCase):
    """Test themis load functions."""

    def test_load_state_data(self):
        """Load state."""
        pyspedas.projects.themis.state(varnames=['thc_pos'])
        self.assertTrue(data_exists('thc_pos'))

    def test_load_state_support_data(self):
        """Load state."""
        state_vars = pyspedas.projects.themis.state(probe='a',trange=['2023-03-23','2023-03-24'], get_support_data=True)
        self.assertTrue('tha_spinras' in state_vars)
        self.assertTrue(data_exists('tha_spinras'))

    def test_load_state_support_data_multiprobe(self):
        """Load state."""
        state_vars = pyspedas.projects.themis.state(probe=['a','b'],trange=['2023-03-23','2023-03-24'], get_support_data=True)
        self.assertTrue('tha_spinras' in state_vars)
        self.assertTrue(data_exists('tha_spinras'))
        self.assertTrue('thb_spinras' in state_vars)
        self.assertTrue(data_exists('thb_spinras'))

    def test_load_sst_data(self):
        """Load SST."""
        pyspedas.projects.themis.sst(varnames=['thc_psif_en_eflux'])
        self.assertTrue(data_exists('thc_psif_en_eflux'))

    def test_load_fgm_data(self):
        """Load FGM."""
        pyspedas.projects.themis.fgm(varnames=['thc_fgs_btotal'])
        self.assertTrue(data_exists('thc_fgs_btotal'))

    def test_load_fit_data(self):
        """Load FIT."""
        pyspedas.projects.themis.fit(varnames=['thc_fgs_gse'])
        self.assertTrue(data_exists('thc_fgs_gse'))

    def test_load_esa_data(self):
        """Load ESA."""
        pyspedas.projects.themis.esa(varnames=['thc_peif_density'])
        self.assertTrue(data_exists('thc_peif_density'))

    def test_load_fft_data(self):
        """Load FFT."""
        pyspedas.projects.themis.fft(varnames=['thc_ffp_16_edc34'])
        self.assertTrue(data_exists('thc_ffp_16_edc34'))

    def test_load_fft_l1_data(self):
        """Load L1 FFT."""
        pyspedas.projects.themis.fft(level='l1', varnames=['thc_ffp_16'])
        self.assertTrue(data_exists('thc_ffp_16'))

    def test_load_fbk_data(self):
        """Load FBK."""
        pyspedas.projects.themis.fbk(varnames=['thc_fb_hff'])
        self.assertTrue(data_exists('thc_fb_hff'))

    def test_load_mom_data(self):
        """Load MOM."""
        pyspedas.projects.themis.mom(varnames=['thc_peim_density'])
        self.assertTrue(data_exists('thc_peim_density'))

    def test_load_gmom_data(self):
        """Load GMOM."""
        pyspedas.projects.themis.gmom(trange=['2020-01-01', '2020-01-01'],
                             varnames=['thc_ptiff_density'])
        self.assertTrue(data_exists('thc_ptiff_density'))

    def test_load_scm_data(self):
        """Load SCM."""
        pyspedas.projects.themis.scm(varnames=['thc_scf_btotal'])
        self.assertTrue(data_exists('thc_scf_btotal'))

    def test_load_scm_l1_data(self):
        """Load L1 SCM."""
        pyspedas.projects.themis.scm(level='l1', varnames=['thc_scf'])
        self.assertTrue(data_exists('thc_scf'))

    def test_load_efi_l1_data(self):
        """Load L1 EFI."""
        pyspedas.projects.themis.efi(level='l1', varnames=['thc_eff'])
        self.assertTrue(data_exists('thc_eff'))

    def test_load_efi_data(self):
        """Load EFI."""
        pyspedas.projects.themis.efi(time_clip=True, varnames=['thc_eff_e12_efs'])
        self.assertTrue(data_exists('thc_eff_e12_efs'))

    def test_load_slp_data(self):
        pyspedas.projects.themis.slp()
        # Check that all data is loaded
        self.assertTrue(data_exists('slp_sun_ltime'))
        self.assertTrue(data_exists('slp_lun_ltime'))
        self.assertTrue(data_exists('slp_sun_pos'))
        self.assertTrue(data_exists('slp_lun_vel'))
        self.assertTrue(data_exists('slp_sun_ltime'))
        self.assertTrue(data_exists('slp_lun_ltime'))
        self.assertTrue(data_exists('slp_lun_vel'))
        self.assertTrue(data_exists('slp_sun_att_x'))
        self.assertTrue(data_exists('slp_sun_att_z'))
        self.assertTrue(data_exists('slp_lun_att_x'))
        self.assertTrue(data_exists('slp_lun_att_z'))
        # Check that coordinate systems are set properly
        self.assertEqual(get_coords('slp_sun_pos').lower(),'gei')
        self.assertEqual(get_coords('slp_sun_vel').lower(),'gei')
        self.assertEqual(get_coords('slp_sun_att_x').lower(),'gei')
        self.assertEqual(get_coords('slp_sun_att_z').lower(),'gei')
        self.assertEqual(get_coords('slp_lun_pos').lower(),'gei')
        self.assertEqual(get_coords('slp_lun_vel').lower(),'gei')
        self.assertEqual(get_coords('slp_lun_att_x').lower(),'gei')
        self.assertEqual(get_coords('slp_lun_att_z').lower(),'gei')

    def test_downloadonly(self):
        """Downloadonly keyword."""
        files = pyspedas.projects.themis.efi(downloadonly=True,
                                    trange=['2014-2-15', '2014-2-16'],
                                    varnames=['thc_eff_e12_efs'])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()
