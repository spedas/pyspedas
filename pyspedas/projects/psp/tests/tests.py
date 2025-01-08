import os
import unittest
from pytplot import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_unpublished_data(self):
        """
            this test doesn't load any data, since the username/pw is invalid
        """
        # no password
        fields_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_RTN', username='hello')
        # invalid password
        fields_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_RTN', username='hello', password='world')
        fields_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_SC', username='hello', password='world')
        fields_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_SC_1min', username='hello', password='world')
        fields_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_RTN_1min', username='hello', password='world')
        fields_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_RTN_4_Sa_per_Cyc', username='hello', password='world')
        fields_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_SC_4_Sa_per_Cyc', username='hello', password='world')
        fields_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='sqtn_rfs_V1V2', username='hello', password='world')
        spc = pyspedas.projects.psp.spc(trange=['2018-11-5', '2018-11-5/06:00'], username='hello', password='world')
        spi = pyspedas.projects.psp.spi(trange=['2018-11-5', '2018-11-5/06:00'], username='hello', password='world')

    def test_load_dfb_dbm_dvac(self):
        fields_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='dfb_dbm_dvac', level='l2')
        self.assertTrue(data_exists('psp_fld_l2_dfb_dbm_dvac12'))

    def test_load_fld_data(self):
        fields_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_rtn', level='l2', time_clip=True)
        self.assertTrue(data_exists('psp_fld_l2_mag_RTN'))
        filtered = pyspedas.projects.psp.filter_fields('psp_fld_l2_mag_RTN', [4, 16])
        self.assertTrue(data_exists('psp_fld_l2_mag_RTN_004016'))
        filtered = pyspedas.projects.psp.filter_fields('psp_fld_l2_mag_RTN', 0)
        self.assertTrue(data_exists('psp_fld_l2_mag_RTN_000'))
        filtered = pyspedas.projects.psp.filter_fields('psp_fld_l2_mag_RTN', [4, 16], keep=True)
    
    def test_load_fld_data_prefix_none(self):
        fields_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_rtn', level='l2', time_clip=True, prefix=None)
        self.assertTrue(data_exists('psp_fld_l2_mag_RTN'))

    def test_load_fld_data_suffix_none(self):
        fields_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_rtn', level='l2', time_clip=True, suffix=None)
        self.assertTrue(data_exists('psp_fld_l2_mag_RTN'))

    def test_load_fld_data_prefix_suffix(self):
        fields_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_rtn', level='l2', time_clip=True, prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_psp_fld_l2_mag_RTN_suf'))

    def test_load_fld_1min(self):
        fields_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_rtn_1min', level='l2')
        filtered = pyspedas.projects.psp.filter_fields('psp_fld_l2_mag_RTN_1min', [4, 16])
        self.assertTrue(data_exists('psp_fld_l2_mag_RTN_1min'))
        self.assertTrue(data_exists('psp_fld_l2_quality_flags'))
        notplot = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_rtn_1min', level='l2', notplot=True)
        self.assertTrue('psp_fld_l2_mag_RTN_1min' in notplot.keys())

    def test_load_fld_rtn_4_per_cyc(self):
        fields = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_rtn_4_per_cycle', level='l2')
        filtered = pyspedas.projects.psp.filter_fields('psp_fld_l2_mag_RTN_4_Sa_per_Cyc', [4, 16])
        self.assertTrue(data_exists('psp_fld_l2_mag_RTN_4_Sa_per_Cyc'))
        self.assertTrue(data_exists('psp_fld_l2_quality_flags'))

    def test_load_fld_sc_4_per_cyc(self):
        fields = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_sc_4_per_cycle',
                                     level='l2')
        filtered = pyspedas.projects.psp.filter_fields('psp_fld_l2_mag_SC_4_Sa_per_Cyc', [4, 16])
        self.assertTrue(data_exists('psp_fld_l2_mag_SC_4_Sa_per_Cyc'))
        self.assertTrue(data_exists('psp_fld_l2_quality_flags'))

    def test_load_sqtn_rfs_v1v2(self):
        fields = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='sqtn_rfs_v1v2')
        filtered = pyspedas.projects.psp.filter_fields('electron_density', [4, 16])
        self.assertTrue(data_exists('electron_density'))
        self.assertTrue(data_exists('electron_core_temperature'))

    def test_load_dfb_dc_spec(self):
        fields = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='dfb_dc_spec')
        filtered = pyspedas.projects.psp.filter_fields('psp_fld_l2_dfb_dc_spec_dV12hg', [4, 16])
        self.assertTrue(data_exists('psp_fld_l2_dfb_dc_spec_dV12hg'))
        self.assertTrue(data_exists('psp_fld_l2_dfb_dc_spec_SCMdlfhg'))

    def test_load_dfb_ac_xspec(self):
        fields = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='dfb_ac_xspec')
        filtered = pyspedas.projects.psp.filter_fields('psp_fld_l2_dfb_ac_xspec_power_ch1_SCMdlfhg', [4, 16])
        self.assertTrue(data_exists('psp_fld_l2_dfb_ac_xspec_power_ch1_SCMdlfhg'))
        self.assertTrue(data_exists('psp_fld_l2_dfb_ac_xspec_power_ch1_SCMdlfhg'))

    def test_load_spc_data(self):
        spc_vars = pyspedas.projects.psp.spc(trange=['2018-11-5', '2018-11-6'], datatype='l3i', level='l3')
        self.assertTrue(data_exists('psp_spc_np_fit'))
        self.assertTrue(data_exists('psp_spc_np_fit_uncertainty'))
        self.assertTrue(data_exists('psp_spc_wp_fit'))
        self.assertTrue(data_exists('psp_spc_vp_fit_SC'))
        self.assertTrue(data_exists('psp_spc_vp_fit_RTN'))
        self.assertTrue(data_exists('psp_spc_np1_fit'))

    def test_load_spc_data_prefix_none(self):
        spc_vars = pyspedas.projects.psp.spc(trange=['2018-11-5', '2018-11-6'], datatype='l3i', level='l3', prefix=None)
        self.assertTrue(data_exists('psp_spc_np_fit'))

    def test_load_spc_data_suffix_none(self):
        spc_vars = pyspedas.projects.psp.spc(trange=['2018-11-5', '2018-11-6'], datatype='l3i', level='l3', suffix=None)
        self.assertTrue(data_exists('psp_spc_np_fit'))
    
    def test_load_spc_data_suffix(self):
        spc_vars = pyspedas.projects.psp.spc(trange=['2018-11-5', '2018-11-6'], datatype='l3i', level='l3', prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_psp_spc_np_fit_suf'))

    def test_load_spc_data_varnames(self):
        spc_vars = pyspedas.projects.psp.spc(trange=['2018-11-5', '2018-11-6'], datatype='l3i', level='l3', varnames=['np_fit'])
        self.assertTrue(data_exists('psp_spc_np_fit'))

    def test_load_spe_data(self):
        spe_vars = pyspedas.projects.psp.spe(trange=['2018-11-5', '2018-11-6'], datatype='spa_sf1_32e', level='l2')
        self.assertTrue(data_exists('psp_spe_EFLUX'))
        self.assertTrue(data_exists('psp_spe_QUALITY_FLAG'))
    
    def test_load_spe_data_prefix_none(self):
        spe_vars = pyspedas.projects.psp.spe(trange=['2018-11-5', '2018-11-6'], datatype='spa_sf1_32e', level='l2', prefix=None)
        self.assertTrue(data_exists('psp_spe_EFLUX'))
    
    def test_load_spe_data_suffix_none(self):
        spe_vars = pyspedas.projects.psp.spe(trange=['2018-11-5', '2018-11-6'], datatype='spa_sf1_32e', level='l2', suffix=None)
        self.assertTrue(data_exists('psp_spe_EFLUX'))
    
    def test_load_spe_data_prefix_suffix(self):
        spe_vars = pyspedas.projects.psp.spe(trange=['2018-11-5', '2018-11-6'], datatype='spa_sf1_32e', level='l2', prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_psp_spe_EFLUX_suf'))

    def test_load_spi_data(self):
        spi_vars = pyspedas.projects.psp.spi(trange=['2018-11-5', '2018-11-6'], datatype='spi_sf0a_mom_inst', level='l3')
        self.assertTrue(data_exists('psp_spi_DENS'))
        self.assertTrue(data_exists('psp_spi_VEL'))
        self.assertTrue(data_exists('psp_spi_T_TENSOR'))
        self.assertTrue(data_exists('psp_spi_TEMP'))
        self.assertTrue(data_exists('psp_spi_EFLUX_VS_ENERGY'))
        self.assertTrue(data_exists('psp_spi_EFLUX_VS_THETA'))
        self.assertTrue(data_exists('psp_spi_EFLUX_VS_PHI'))

    def test_load_spi_data_prefix_none(self):
        spi_vars = pyspedas.projects.psp.spi(trange=['2018-11-5', '2018-11-6'], datatype='spi_sf0a_mom_inst', level='l3', prefix=None)
        self.assertTrue(data_exists('psp_spi_DENS'))
    
    def test_load_spi_data_suffix_none(self):
        spi_vars = pyspedas.projects.psp.spi(trange=['2018-11-5', '2018-11-6'], datatype='spi_sf0a_mom_inst', level='l3', suffix=None)
        self.assertTrue(data_exists('psp_spi_DENS'))
    
    def test_load_spi_data_prefix_suffix(self):
        spi_vars = pyspedas.projects.psp.spi(trange=['2018-11-5', '2018-11-6'], datatype='spi_sf0a_mom_inst', level='l3', prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_psp_spi_DENS_suf'))

    def test_load_epihi_data(self):
        epihi_vars = pyspedas.projects.psp.epihi(trange=['2018-11-5', '2018-11-5/06:00'], datatype='let1_rates1h', level='l2')
        self.assertTrue(data_exists('psp_epihi_B_He_Rate'))
        self.assertTrue(data_exists('psp_epihi_R1A_He_BIN'))
        self.assertTrue(data_exists('psp_epihi_R3B_He_BIN'))
        self.assertTrue(data_exists('psp_epihi_R6A_He_BIN'))
    
    def test_load_epihi_data_prefix_none(self):
        epihi_vars = pyspedas.projects.psp.epihi(trange=['2018-11-5', '2018-11-5/06:00'], datatype='let1_rates1h', level='l2', prefix=None)
        self.assertTrue(data_exists('psp_epihi_B_He_Rate'))
    
    def test_load_epihi_data_suffix_none(self):
        epihi_vars = pyspedas.projects.psp.epihi(trange=['2018-11-5', '2018-11-5/06:00'], datatype='let1_rates1h', level='l2', suffix=None)
        self.assertTrue(data_exists('psp_epihi_B_He_Rate'))

    def test_load_epihi_data_prefix_suffix(self):
        epihi_vars = pyspedas.projects.psp.epihi(trange=['2018-11-5', '2018-11-5/06:00'], datatype='let1_rates1h', level='l2', prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_psp_epihi_B_He_Rate_suf'))

    def test_load_epi_data(self):
        epilo_vars = pyspedas.projects.psp.epi()
        self.assertTrue(data_exists('psp_isois_HET_A_Electrons_Rate_TS'))
        self.assertTrue(data_exists('psp_isois_HET_A_H_Rate_TS'))
        self.assertTrue(data_exists('psp_isois_A_H_Rate_TS'))
        self.assertTrue(data_exists('psp_isois_A_Heavy_Rate_TS'))
        self.assertTrue(data_exists('psp_isois_H_CountRate_ChanP_SP'))
        self.assertTrue(data_exists('psp_isois_Electron_CountRate_ChanE'))

    def test_load_epi_data_prefix_none(self):
        epilo_vars = pyspedas.projects.psp.epi(prefix=None)
        self.assertTrue(data_exists('psp_isois_HET_A_Electrons_Rate_TS'))

    def test_load_epi_data_suffix_none(self):
        epilo_vars = pyspedas.projects.psp.epi(suffix=None)
        self.assertTrue(data_exists('psp_isois_HET_A_Electrons_Rate_TS'))

    def test_load_epi_data_prefix_suffix(self):
        epilo_vars = pyspedas.projects.psp.epi(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_psp_isois_HET_A_Electrons_Rate_TS_suf'))

    def test_downloadonly(self):
        files = pyspedas.projects.psp.epilo(downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()
