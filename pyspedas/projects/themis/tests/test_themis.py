"""Test gmag and themis load functions."""
import os
import unittest
import logging
import pyspedas
import pyspedas
from pyspedas.tplot_tools import data_exists, get_coords



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

    def test_check_greenland(self):
        """Check if a gmag station is in the greenland group."""
        from pyspedas.projects.themis.ground.gmag import check_greenland
        self.assertTrue(check_greenland('bfe') == 1)
        self.assertTrue(check_greenland('bou') == 0)

    def test_check_variometer(self):
        """Check if a gmag station is in the 1 Hz variometer group or 10 Hz variometer group or not."""
        from pyspedas.projects.themis.ground.gmag import check_variometer
        self.assertTrue(check_variometer('anmo') == 1)
        self.assertTrue(check_variometer('anmo_100ms') == 10)
        self.assertTrue(check_variometer('bou') == 0)

    def test_load_gmag_data(self):
        """Load gmag."""
        pyspedas.projects.themis.gmag(varnames=['thg_mag_amer'], sites='amer')
        self.assertTrue(data_exists('thg_mag_amer'))

    def test_load_gmag_variometer_1_hz_data(self):
        """Load gmag variometer 1 Hz data."""
        pyspedas.projects.themis.gmag(varnames=['thg_mag_s61a'], sites='s61a',trange=['2026-02-24', '2026-02-25'])
        self.assertTrue(data_exists('thg_mag_s61a'))
    
    def test_load_gmag_variometer_10_hz_data_notag(self):
        """Load gmag variometer 10 Hz data using the sampling_rate argument and not the time resolution tag."""
        pyspedas.projects.themis.gmag(varnames=['thg_mag_s61a_100ms'], sites='s61a',sampling_rate=10,trange=['2026-02-24', '2026-02-25'])
        self.assertTrue(data_exists('thg_mag_s61a_100ms'))

    def test_load_gmag_variometer_10_hz_data_tag(self):
        """Load gmag variometer 10 Hz data using the time resolution tag and not the sampling_rate argument."""
        pyspedas.projects.themis.gmag(varnames=['thg_mag_s61a_100ms'], sites='s61a_100ms',trange=['2026-02-24', '2026-02-25'])
        self.assertTrue(data_exists('thg_mag_s61a_100ms'))
    


class LoadTestCases(unittest.TestCase):
    """Test themis load functions."""

    def test_load_state_data(self):
        """Load state."""
        vars = pyspedas.projects.themis.state(varnames=['thc_pos'])
        self.assertTrue(data_exists('thc_pos'))
        self.assertTrue('thc_pos' in vars)

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
        sst_vars = pyspedas.projects.themis.sst(varnames=['thc_psif_en_eflux'])
        self.assertTrue(data_exists('thc_psif_en_eflux'))
        self.assertTrue('thc_psif_en_eflux' in sst_vars)

    def test_load_sst_eclipse(self):
        """Load SST."""
        trange=['2026-01-01','2026-01-03']
        probe='b'
        sst_vars = pyspedas.projects.themis.sst(probe=probe, trange=trange, level='l2', apply_eclipse_corrections=True)
        self.assertTrue(data_exists('thb_psif_mftens'))
        self.assertTrue('thb_psif_mftens' in sst_vars)

    def test_load_fgm_data(self):
        """Load FGM."""
        fgm_vars = pyspedas.projects.themis.fgm(varnames=['thc_fgs_btotal'])
        self.assertTrue(data_exists('thc_fgs_btotal'))
        self.assertTrue('thc_fgs_btotal' in fgm_vars)

    def test_load_fgm_data_eclipse(self):
        """Load FGM."""
        trange=['2026-01-01','2026-01-03']
        probe='b'
        fgm_vars = pyspedas.projects.themis.fgm(probe=probe, trange=trange, level='l2', apply_eclipse_corrections=True)
        self.assertTrue(data_exists('thb_fgs_dsl'))
        self.assertTrue('thb_fgs_dsl' in fgm_vars)

    def test_load_fit_data(self):
        """Load FIT."""
        fit_vars = pyspedas.projects.themis.fit(varnames=['thc_fgs_gse'])
        self.assertTrue(data_exists('thc_fgs_gse'))
        self.assertTrue('thc_fgs_gse' in fit_vars)

    def test_load_fit_eclipse(self):
        """Load FIT."""
        trange=['2026-01-01','2026-01-03']
        probe='b'
        fit_vars = pyspedas.projects.themis.fit(probe=probe, trange=trange, level='l2', apply_eclipse_corrections=True)
        self.assertTrue(data_exists('thb_fgs_gse'))
        self.assertTrue('thb_fgs_gse' in fit_vars)

    def test_load_esa_data(self):
        """Load ESA."""
        esa_vars = pyspedas.projects.themis.esa(varnames=['thc_peif_density'])
        self.assertTrue(data_exists('thc_peif_density'))
        self.assertTrue('thc_peif_density' in esa_vars)

    def test_load_esa_eclipse(self):
        """Load ESA."""
        trange=['2026-01-01','2026-01-03']
        probe='b'
        esa_vars = pyspedas.projects.themis.esa(probe=probe, trange=trange, level='l2', apply_eclipse_corrections=True)
        self.assertTrue(data_exists('thb_peif_mftens'))
        self.assertTrue('thb_peif_mftens' in esa_vars)

    def test_load_fft_data(self):
        """Load FFT."""
        fft_vars = pyspedas.projects.themis.fft(varnames=['thc_ffp_16_edc34'])
        self.assertTrue(data_exists('thc_ffp_16_edc34'))
        self.assertTrue('thc_ffp_16_edc34' in fft_vars)

    def test_load_fft_l1_data(self):
        """Load L1 FFT."""
        fft_vars = pyspedas.projects.themis.fft(level='l1', varnames=['thc_ffp_16'])
        self.assertTrue(data_exists('thc_ffp_16'))
        self.assertTrue('thc_ffp_16' in fft_vars)

    def test_load_fbk_data(self):
        """Load FBK."""
        fbk_vars = pyspedas.projects.themis.fbk(varnames=['thc_fb_hff'])
        self.assertTrue(data_exists('thc_fb_hff'))
        self.assertTrue('thc_fb_hff' in fbk_vars)

    def test_load_mom_data(self):
        """Load MOM."""
        mom_vars = pyspedas.projects.themis.mom(varnames=['thc_peim_density'])
        self.assertTrue(data_exists('thc_peim_density'))
        self.assertTrue('thc_peim_density' in mom_vars)

    def test_load_mom_eclipse(self):
        """Load MOM."""
        trange=['2026-01-01','2026-01-03']
        probe='b'
        mom_vars = pyspedas.projects.themis.mom(probe='b', trange=trange, level='l2', apply_eclipse_corrections=True)
        self.assertTrue(data_exists('thb_peim_mftens'))
        self.assertTrue('thb_peim_mftens' in mom_vars)

    def test_load_gmom_data(self):
        """Load GMOM."""
        gmom_vars = pyspedas.projects.themis.gmom(trange=['2020-01-01', '2020-01-01'],
                             varnames=['thc_ptiff_density'])
        self.assertTrue(data_exists('thc_ptiff_density'))
        self.assertTrue('thc_ptiff_density' in gmom_vars)

    def test_load_gmom_eclipse(self):
        """Load GMOM."""
        trange=['2026-01-01','2026-01-03']
        probe='b'
        gmom_vars = pyspedas.projects.themis.gmom(probe='b', trange=trange, level='l2', apply_eclipse_corrections=True)
        self.assertTrue(data_exists('thb_ptiff_velocity_gse'))
        self.assertTrue('thb_ptiff_velocity_gse' in gmom_vars)

    def test_load_scm_data(self):
        """Load SCM."""
        scm_vars = pyspedas.projects.themis.scm(varnames=['thc_scf_btotal'])
        self.assertTrue(data_exists('thc_scf_btotal'))
        self.assertTrue('thc_scf_btotal' in scm_vars)

    def test_load_scm_eclipse(self):
        """Load SCM."""
        trange=['2026-01-01','2026-01-03']
        probe='b'
        scm_vars = pyspedas.projects.themis.scm(probe=probe,trange=trange,level='l2',apply_eclipse_corrections=True)
        self.assertTrue(data_exists('thb_scf_gse'))
        self.assertTrue('thb_scf_gse' in scm_vars)

    def test_load_scm_l1_data(self):
        """Load L1 SCM."""
        scm_vars = pyspedas.projects.themis.scm(level='l1', varnames=['thc_scf'])
        self.assertTrue(data_exists('thc_scf'))
        self.assertTrue('thc_scf' in scm_vars)

    def test_load_efi_l1_data(self):
        """Load L1 EFI."""
        vars = pyspedas.projects.themis.efi(level='l1', varnames=['thc_eff','thc_efp'])
        self.assertTrue(data_exists('thc_eff'))
        self.assertTrue(data_exists('thc_efp'))
        self.assertFalse('thc_efw' in vars)
        self.assertTrue('thc_eff' in vars)

    def test_load_efi_l1_datatype(self):
        """Load L1 EFI."""
        vars = pyspedas.projects.themis.efi(level='l1', datatype=['eff', 'efp'])
        self.assertTrue(data_exists('thc_eff'))
        self.assertTrue(data_exists('thc_efp'))
        self.assertFalse('thc_efw' in vars)
        self.assertTrue('thc_eff' in vars)

    def test_load_efi_data(self):
        """Load EFI."""
        vars = pyspedas.projects.themis.efi(time_clip=True, varnames=['thc_eff_e12_efs'])
        self.assertTrue(data_exists('thc_eff_e12_efs'))
        self.assertFalse('thc_efw_gse' in vars)

    def test_load_efi_eclipse(self):
        """Load EFI."""
        trange=['2026-01-01','2026-01-03']
        probe='b'
        vars = pyspedas.projects.themis.efi(probe=probe,trange=trange,level='l2',apply_eclipse_corrections=True)
        self.assertTrue(data_exists('thb_eff_e12_efs'))
        self.assertTrue('thb_eff_e12_efs' in vars)

    def test_load_l2_efw_data(self):
        """Load EFI L2 wave burst data"""
        vars = pyspedas.projects.themis.efi(trange=['2017-01-01','2017-01-02'], probe='a',time_clip=True, datatype='efw')
        self.assertTrue(data_exists('tha_efw_gse'))
        self.assertTrue('tha_efw_gse' in vars)

    def test_load_l2_efp_data(self):
        """Load EFI L2 particle burst data"""
        vars = pyspedas.projects.themis.efi(trange=['2017-01-01','2017-01-02'], probe='a',time_clip=True, datatype='efp')
        self.assertTrue(data_exists('tha_efp_gse'))
        self.assertTrue('tha_efp_gse' in vars)

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
