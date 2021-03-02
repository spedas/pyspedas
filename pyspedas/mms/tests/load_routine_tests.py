import unittest
import numpy as np

from pyspedas.mms import mms_load_state, mms_load_mec, mms_load_fgm, mms_load_scm, mms_load_fpi, mms_load_hpca, mms_load_eis, mms_load_feeps, mms_load_edp, mms_load_edi, mms_load_aspoc, mms_load_dsp
from pyspedas.utilities.data_exists import data_exists
from pyspedas.mms.hpca.mms_hpca_calc_anodes import mms_hpca_calc_anodes
from pyspedas.mms.hpca.mms_hpca_spin_sum import mms_hpca_spin_sum

from pytplot import get_data, del_data

from pyspedas import tdpwrspc

class StateLoadTestCases(unittest.TestCase):
    def test_load_eph_no_update(self):
        data = mms_load_state(datatypes=['pos', 'vel']) # ensure the files are stored locally
        del_data('*') # remove the current tplot vars
        data = mms_load_state(datatypes=['pos', 'vel'], no_update=True) # ensure the files are stored locally
        self.assertTrue(data_exists('mms1_defeph_pos'))
        self.assertTrue(data_exists('mms1_defeph_vel'))

    def test_load_eph_data(self):
        data = mms_load_state(datatypes=['pos', 'vel'])
        self.assertTrue(data_exists('mms1_defeph_pos'))
        self.assertTrue(data_exists('mms1_defeph_vel'))

    def test_load_att_data(self):
        data = mms_load_state(trange=['2015-10-16', '2015-10-16/06:00'], datatypes=['spinras', 'spindec'])
        self.assertTrue(data_exists('mms1_defatt_spinras'))
        self.assertTrue(data_exists('mms1_defatt_spindec'))

############### DSP ############### 
class DSPLoadTestCases(unittest.TestCase):
    # def test_load_default_data(self):
    #     data = mms_load_dsp(trange=['2015-08-01','2015-09-01'], datatype='swd', level='l2', data_rate='fast')
    #     self.assertTrue(data_exists('mms1_dsp_swd_E12_Counts'))

    def test_load_epsd_bpsd_data(self):
        data = mms_load_dsp(trange=['2015-08-01','2015-08-02'], datatype=['epsd', 'bpsd'], level='l2', data_rate='fast')
        self.assertTrue(data_exists('mms1_dsp_epsd_omni'))
        self.assertTrue(data_exists('mms1_dsp_bpsd_omni'))

    def test_load_bpsd_data(self):
        data = mms_load_dsp(trange=['2015-10-16','2015-10-17'], datatype='bpsd', level='l2', data_rate='fast')
        self.assertTrue(data_exists('mms1_dsp_bpsd_omni_fast_l2'))

    def test_load_epsd_spdf(self):
        data = mms_load_dsp(trange=['2015-08-01','2015-08-02'], datatype='epsd', level='l2', data_rate='fast', spdf=True)
        self.assertTrue(data_exists('mms1_dsp_epsd_omni'))

    def test_load_epsd_suffix(self):
        data = mms_load_dsp(trange=['2015-08-01','2015-08-02'], datatype='epsd', level='l2', data_rate='fast', suffix='_test')
        self.assertTrue(data_exists('mms1_dsp_epsd_omni_test'))

############### FEEPS ############### 
class FEEPSLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_feeps(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_epd_feeps_srvy_l2_electron_intensity_omni'))
        self.assertTrue(data_exists('mms1_epd_feeps_srvy_l2_electron_intensity_omni_spin'))

    def test_load_spdf_data(self):
        del_data('*')
        data = mms_load_feeps(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', spdf=True)
        self.assertTrue(data_exists('mms1_epd_feeps_brst_l2_electron_intensity_omni'))
        self.assertTrue(data_exists('mms1_epd_feeps_brst_l2_electron_intensity_omni_spin'))

    def test_load_suffix(self):
        data = mms_load_feeps(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', suffix='_test')
        self.assertTrue(data_exists('mms1_epd_feeps_brst_l2_electron_intensity_omni_test'))
        self.assertTrue(data_exists('mms1_epd_feeps_brst_l2_electron_intensity_omni_spin_test'))

    def test_load_brst_ion_data(self):
        del_data('*')
        data = mms_load_feeps(probe=4, data_rate='brst', datatype='ion', trange=['2015-10-01/10:48:16', '2015-10-01/10:49:16'])
        self.assertTrue(data_exists('mms4_epd_feeps_brst_l2_ion_intensity_omni'))
        self.assertTrue(data_exists('mms4_epd_feeps_brst_l2_ion_intensity_omni_spin'))

    def test_load_brst_multi_probe(self):
        del_data('*')
        data = mms_load_feeps(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', probe=[1, 2, 3, 4])
        self.assertTrue(data_exists('mms1_epd_feeps_brst_l2_electron_intensity_omni'))
        self.assertTrue(data_exists('mms1_epd_feeps_brst_l2_electron_intensity_omni_spin'))
        self.assertTrue(data_exists('mms2_epd_feeps_brst_l2_electron_intensity_omni'))
        self.assertTrue(data_exists('mms2_epd_feeps_brst_l2_electron_intensity_omni_spin'))
        self.assertTrue(data_exists('mms3_epd_feeps_brst_l2_electron_intensity_omni'))
        self.assertTrue(data_exists('mms3_epd_feeps_brst_l2_electron_intensity_omni_spin'))
        self.assertTrue(data_exists('mms4_epd_feeps_brst_l2_electron_intensity_omni'))
        self.assertTrue(data_exists('mms4_epd_feeps_brst_l2_electron_intensity_omni_spin'))

############### FPI ############### 
class FPILoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'])
        self.assertTrue(data_exists('mms1_dis_energyspectr_omni_fast'))

    def test_load_spdf_data(self):
        data = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'], spdf=True)
        self.assertTrue(data_exists('mms1_dis_energyspectr_omni_fast'))

    def test_load_small_brst_interval(self):
        data = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', datatype=['dis-moms', 'dis-dist'], time_clip=True)
        self.assertTrue(data_exists('mms1_dis_energyspectr_omni_brst'))

    def test_center_fast_ion_data_notplot(self):
        data = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'], notplot=True)
        centered = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'], center_measurement=True, suffix='_centered', notplot=True)

        self.assertTrue(np.round(centered['mms1_dis_bulkv_gse_fast_centered']['x'][0]-data['mms1_dis_bulkv_gse_fast']['x'][0], decimals=3) == 2.25)

    def test_center_fast_ion_data(self):
        data = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'])
        centered = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'], center_measurement=True, suffix='_centered')
        
        t, d = get_data('mms1_dis_bulkv_gse_fast')
        c, d = get_data('mms1_dis_bulkv_gse_fast_centered')
        self.assertTrue(np.round(c[0]-t[0], decimals=3) == 2.25)

    def test_center_fast_electron_data(self):
        data = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'])
        centered = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'], center_measurement=True, suffix='_centered')
        
        t, d = get_data('mms1_des_bulkv_gse_fast')
        c, d = get_data('mms1_des_bulkv_gse_fast_centered')
        self.assertTrue(np.round(c[0]-t[0], decimals=3) == 2.25)

    def test_center_brst_ion_data(self):
        data = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst')
        centered = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', center_measurement=True, suffix='_centered')
        
        t, d = get_data('mms1_dis_bulkv_gse_brst')
        c, d = get_data('mms1_dis_bulkv_gse_brst_centered')
        self.assertTrue(np.round(c[0]-t[0], decimals=3) == 0.075)

    def test_center_brst_electron_data(self):
        data = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst')
        centered = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', center_measurement=True, suffix='_centered')
        
        t, d = get_data('mms1_des_bulkv_gse_brst')
        c, d = get_data('mms1_des_bulkv_gse_brst_centered')
        self.assertTrue(np.round(c[0]-t[0], decimals=3) == 0.015)

############### HPCA ############### 
class HPCALoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_hpca(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_hpca_hplus_number_density'))

    def test_load_spdf_data(self):
        data = mms_load_hpca(trange=['2015-10-16', '2015-10-16/01:00'], spdf=True)
        self.assertTrue(data_exists('mms1_hpca_hplus_number_density'))

    def test_load_ion_omni_suffix(self):
        del_data('*')
        data = mms_load_hpca(probe=2, trange=['2016-08-09/09:10', '2016-08-09/10:10:00'], datatype='ion', data_rate='brst', suffix='_brst')
        mms_hpca_calc_anodes(fov=[0, 360], probe=2, suffix='_brst')
        mms_hpca_spin_sum(probe=2, suffix='_brst', avg=True)
        self.assertTrue(data_exists('mms2_hpca_hplus_flux_brst_elev_0-360_spin'))

    def test_load_ion_omni(self):
        del_data('*')
        data = mms_load_hpca(trange=['2016-10-16/5:00', '2016-10-16/6:00'], datatype='ion')
        mms_hpca_calc_anodes(fov=[0, 360], probe='1')
        mms_hpca_spin_sum()
        self.assertTrue(data_exists('mms1_hpca_hplus_flux_elev_0-360_spin'))
        self.assertTrue(data_exists('mms1_hpca_heplus_flux_elev_0-360_spin'))
        self.assertTrue(data_exists('mms1_hpca_heplusplus_flux_elev_0-360_spin'))
        self.assertTrue(data_exists('mms1_hpca_oplus_flux_elev_0-360_spin'))

    def test_center_fast_moments_data(self):
        data = mms_load_hpca(trange=['2015-10-16/14:00', '2015-10-16/15:00'])
        centered = mms_load_hpca(trange=['2015-10-16/14:00', '2015-10-16/15:00'], center_measurement=True, suffix='_centered')
        
        t, d = get_data('mms1_hpca_hplus_ion_bulk_velocity')
        c, d = get_data('mms1_hpca_hplus_ion_bulk_velocity_centered')
        self.assertTrue(np.round(c[0]-t[0], decimals=3) == 5.0)

    def test_center_brst_moments_data(self):
        data = mms_load_hpca(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst')
        centered = mms_load_hpca(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', center_measurement=True, suffix='_centered')
        
        t, d = get_data('mms1_hpca_hplus_ion_bulk_velocity')
        c, d = get_data('mms1_hpca_hplus_ion_bulk_velocity_centered')
        self.assertTrue(np.round(c[0]-t[0], decimals=3) == 5.0)

############### EDI ############### 
class EDILoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_edi(trange=['2016-10-17/13:00', '2016-10-17/14:00'])
        self.assertTrue(data_exists('mms1_edi_e_gse_srvy_l2'))

    def test_load_spdf_data(self):
        data = mms_load_edi(trange=['2016-10-17/13:00', '2016-10-17/14:00'], spdf=True)
        self.assertTrue(data_exists('mms1_edi_e_gse_srvy_l2'))

    def test_load_suffix(self):
        data = mms_load_edi(trange=['2016-10-17/13:00', '2016-10-17/14:00'], suffix='_test')
        self.assertTrue(data_exists('mms1_edi_e_gse_srvy_l2_test'))

############### ASPOC ############### 
class ASPOCLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_aspoc(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_aspoc_ionc_l2'))

    def test_load_spdf_data(self):
        data = mms_load_aspoc(trange=['2015-10-16', '2015-10-16/01:00'], spdf=True)
        self.assertTrue(data_exists('mms1_aspoc_ionc_l2'))

    def test_load_suffix(self):
        data = mms_load_aspoc(trange=['2015-10-16', '2015-10-16/01:00'], suffix='_test')
        self.assertTrue(data_exists('mms1_aspoc_ionc_l2_test'))

############### EDP ############### 
class EDPLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_edp(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_edp_dce_gse_fast_l2'))

    def test_load_hfesp_data(self):
        data = mms_load_edp(trange=['2015-10-16', '2015-10-16/01:00'], datatype='hfesp', data_rate='srvy')
        self.assertTrue(data_exists('mms1_edp_hfesp_srvy_l2'))

    def test_load_spdf_data(self):
        data = mms_load_edp(trange=['2015-10-16', '2015-10-16/01:00'], spdf=True)
        self.assertTrue(data_exists('mms1_edp_dce_gse_fast_l2'))

    def test_load_suffix(self):
        data = mms_load_edp(trange=['2015-10-16', '2015-10-16/01:00'], suffix='_test')
        self.assertTrue(data_exists('mms1_edp_dce_gse_fast_l2'))

    # def test_load_multiple_sc(self):
    #     data = mms_load_edp(probe=['1', '2', '3', '4'], trange=['2015-10-16', '2015-10-16/01:00'])
    #     self.assertTrue(data_exists('mms1_edp_dce_gse_fast_l2'))
    #     self.assertTrue(data_exists('mms2_edp_dce_gse_fast_l2'))
    #     self.assertTrue(data_exists('mms3_edp_dce_gse_fast_l2'))
    #     self.assertTrue(data_exists('mms4_edp_dce_gse_fast_l2'))

    def test_load_brst_data(self):
        data = mms_load_edp(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'])
        self.assertTrue(data_exists('mms1_edp_dce_gse_brst_l2'))

############### FGM ############### 
class FGMLoadTestCases(unittest.TestCase):
    def test_regression_multi_imports_spdf(self):
        data = mms_load_fgm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'], spdf=True)
        t1, d1 = get_data('mms1_fgm_b_gse_brst_l2')
        data = mms_load_fgm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'], spdf=True)
        t2, d2 = get_data('mms1_fgm_b_gse_brst_l2')
        self.assertTrue(t1.shape == t2.shape)
        self.assertTrue(d1.shape == d2.shape)

    def test_load_default_data(self):
        data = mms_load_fgm(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_fgm_b_gse_srvy_l2'))
        self.assertTrue(data_exists('Epoch'))
        self.assertTrue(data_exists('Epoch_state'))

    def test_load_spdf_data(self):
        data = mms_load_fgm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'], spdf=True)
        self.assertTrue(data_exists('mms1_fgm_b_gse_brst_l2'))

    def test_load_suffix(self):
        data = mms_load_fgm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'], suffix='_test')
        self.assertTrue(data_exists('mms1_fgm_b_gse_brst_l2_test'))

    def test_load_multiple_sc(self):
        data = mms_load_fgm(probe=[1, 2, 3, 4], data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'])
        self.assertTrue(data_exists('mms1_fgm_b_gse_brst_l2'))
        self.assertTrue(data_exists('mms2_fgm_b_gse_brst_l2'))
        self.assertTrue(data_exists('mms3_fgm_b_gse_brst_l2'))
        self.assertTrue(data_exists('mms4_fgm_b_gse_brst_l2'))

    def test_load_brst_data(self):
        data = mms_load_fgm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'])
        self.assertTrue(data_exists('mms1_fgm_b_gse_brst_l2'))

    def test_load_data_no_update(self):
        data = mms_load_fgm(trange=['2015-10-16', '2015-10-16/01:00']) # make sure the files exist locally
        del_data('*') 
        data = mms_load_fgm(trange=['2015-10-16', '2015-10-16/01:00'], no_update=True) # load the file from the local cache
        self.assertTrue(data_exists('mms1_fgm_b_gse_srvy_l2'))

############### MEC ############### 
class MECLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_mec(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_mec_r_sm'))

    def test_load_spdf_data(self):
        data = mms_load_mec(trange=['2015-10-16', '2015-10-16/01:00'], spdf=True)
        self.assertTrue(data_exists('mms1_mec_r_sm'))

    def test_load_suffix(self):
        data = mms_load_mec(trange=['2015-10-16', '2015-10-16/01:00'], suffix='_test')
        self.assertTrue(data_exists('mms1_mec_r_sm_test'))

class SCMLoadTestCases(unittest.TestCase):
    def test_brst_dpwrspc_data(self):
        data = mms_load_scm(probe=4, data_rate='brst', datatype='scb', trange=['2015-10-01/10:48:16', '2015-10-01/10:49:16'])
        tdpwrspc('mms4_scm_acb_gse_scb_brst_l2')
        self.assertTrue(data_exists('mms4_scm_acb_gse_scb_brst_l2'))
        self.assertTrue(data_exists('mms4_scm_acb_gse_scb_brst_l2_x_dpwrspc'))
        self.assertTrue(data_exists('mms4_scm_acb_gse_scb_brst_l2_y_dpwrspc'))
        self.assertTrue(data_exists('mms4_scm_acb_gse_scb_brst_l2_z_dpwrspc'))

    def test_load_default_data(self):
        data = mms_load_scm(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_scm_acb_gse_scsrvy_srvy_l2'))

    def test_load_suffix(self):
        data = mms_load_scm(trange=['2015-10-16', '2015-10-16/01:00'], suffix='_test')
        self.assertTrue(data_exists('mms1_scm_acb_gse_scsrvy_srvy_l2_test'))

    def test_load_multiple_sc(self):
        data = mms_load_scm(probe=['1', '2', '3', '4'], trange=['2017-12-15', '2017-12-16'])
        # self.assertTrue(data_exists('mms1_scm_acb_gse_scsrvy_srvy_l2'))
        # self.assertTrue(data_exists('mms2_scm_acb_gse_scsrvy_srvy_l2'))
        self.assertTrue(data_exists('mms3_scm_acb_gse_scsrvy_srvy_l2'))
        self.assertTrue(data_exists('mms4_scm_acb_gse_scsrvy_srvy_l2'))

    def test_load_brst_data(self):
        data = mms_load_scm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'], datatype='scb')
        self.assertTrue(data_exists('mms1_scm_acb_gse_scb_brst_l2'))

if __name__ == '__main__':
    unittest.main()