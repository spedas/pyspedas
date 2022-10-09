"""Test gmag and themis load functions."""
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas


class GmagTestCases(unittest.TestCase):
    """Test GMAG functions."""

    def test_get_group(self):
        """Get gmag stations of a group."""
        from pyspedas.themis.ground.gmag import get_group
        self.assertTrue(get_group('ccnv') == ['epo'])

    def test_gmag_list(self):
        """Get gmag list of stations."""
        from pyspedas.themis.ground.gmag import gmag_list
        self.assertTrue(gmag_list()[0:5] == ['abk', 'akul', 'amd', 'amer',
                                             'amk'])

    def test_gmag_groups(self):
        """Get gmag groups."""
        from pyspedas.themis.ground.gmag import gmag_groups
        gmag_table = gmag_groups()
        self.assertTrue(list(gmag_table.keys())[0:5] == ['kyoto', 'sgu',
                                                         'autx', 'ae', 'aari'])

    def test_check_gmag(self):
        """Check a gmag station."""
        from pyspedas.themis.ground.gmag import check_gmag
        self.assertTrue(check_gmag('ccnv') == 1)
        self.assertTrue(check_gmag('abcd') == 0)

    def test_load_gmag_data(self):
        """Load gmag."""
        pyspedas.themis.gmag(varnames=['thg_mag_amer'], sites='amer')
        self.assertTrue(data_exists('thg_mag_amer'))


class LoadTestCases(unittest.TestCase):
    """Test themis load functions."""

    def test_load_state_data(self):
        """Load state."""
        pyspedas.themis.state(varnames=['thc_pos'])
        self.assertTrue(data_exists('thc_pos'))

    def test_load_sst_data(self):
        """Load SST."""
        pyspedas.themis.sst(varnames=['thc_psif_en_eflux'])
        self.assertTrue(data_exists('thc_psif_en_eflux'))

    def test_load_fgm_data(self):
        """Load FGM."""
        pyspedas.themis.fgm(varnames=['thc_fgs_btotal'])
        self.assertTrue(data_exists('thc_fgs_btotal'))

    def test_load_fit_data(self):
        """Load FIT."""
        pyspedas.themis.fit(varnames=['thc_fgs_gse'])
        self.assertTrue(data_exists('thc_fgs_gse'))

    def test_load_esa_data(self):
        """Load ESA."""
        pyspedas.themis.esa(varnames=['thc_peif_density'])
        self.assertTrue(data_exists('thc_peif_density'))

    def test_load_fft_data(self):
        """Load FFT."""
        pyspedas.themis.fft(varnames=['thc_ffp_16_edc34'])
        self.assertTrue(data_exists('thc_ffp_16_edc34'))

    def test_load_fft_l1_data(self):
        """Load L1 FFT."""
        pyspedas.themis.fft(level='l1', varnames=['thc_ffp_16'])
        self.assertTrue(data_exists('thc_ffp_16'))

    def test_load_fbk_data(self):
        """Load FBK."""
        pyspedas.themis.fbk(varnames=['thc_fb_hff'])
        self.assertTrue(data_exists('thc_fb_hff'))

    def test_load_mom_data(self):
        """Load MOM."""
        pyspedas.themis.mom(varnames=['thc_peim_density'])
        self.assertTrue(data_exists('thc_peim_density'))

    def test_load_gmom_data(self):
        """Load GMOM."""
        pyspedas.themis.gmom(trange=['2020-01-01', '2020-01-01'],
                             varnames=['thc_ptiff_density'])
        self.assertTrue(data_exists('thc_ptiff_density'))

    def test_load_scm_data(self):
        """Load SCM."""
        pyspedas.themis.scm(varnames=['thc_scf_btotal'])
        self.assertTrue(data_exists('thc_scf_btotal'))

    def test_load_scm_l1_data(self):
        """Load L1 SCM."""
        pyspedas.themis.scm(level='l1', varnames=['thc_scf'])
        self.assertTrue(data_exists('thc_scf'))

    def test_load_efi_l1_data(self):
        """Load L1 EFI."""
        pyspedas.themis.efi(level='l1', varnames=['thc_eff'])
        self.assertTrue(data_exists('thc_eff'))

    def test_load_efi_data(self):
        """Load EFI."""
        pyspedas.themis.efi(time_clip=True, varnames=['thc_eff_e12_efs'])
        self.assertTrue(data_exists('thc_eff_e12_efs'))

    def test_downloadonly(self):
        """Downloadonly keyword."""
        files = pyspedas.themis.efi(downloadonly=True,
                                    trange=['2014-2-15', '2014-2-16'],
                                    varnames=['thc_eff_e12_efs'])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()
