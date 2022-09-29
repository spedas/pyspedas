import unittest
import pyspedas
from pyspedas.utilities.data_exists import data_exists
from pyspedas.mms.hpca.mms_hpca_calc_anodes import mms_hpca_calc_anodes
from pyspedas.mms.hpca.mms_hpca_spin_sum import mms_hpca_spin_sum


class LoadTestCases(unittest.TestCase):
    def test_load_fgm_ql(self):
        data = pyspedas.mms.fgm(probe=1, level='ql', instrument='dfg', trange=['2015-12-15', '2015-12-16']) 
        self.assertTrue(data_exists('mms1_dfg_srvy_dmpa'))
        self.assertTrue(data_exists('mms1_dfg_srvy_gsm_dmpa'))

    def test_load_dfg_l2pre(self):
        data = pyspedas.mms.fgm(probe=1, level='l2pre', instrument='dfg', trange=['2015-12-15', '2015-12-16']) 
        self.assertTrue(data_exists('mms1_dfg_b_gse_srvy_l2pre'))
        self.assertTrue(data_exists('mms1_dfg_b_gsm_srvy_l2pre'))
        self.assertTrue(data_exists('mms1_dfg_b_dmpa_srvy_l2pre'))

    def test_load_afg_l2pre(self):
        data = pyspedas.mms.fgm(probe=1, level='l2pre', instrument='afg', trange=['2015-12-15', '2015-12-16']) 
        self.assertTrue(data_exists('mms1_afg_b_gse_srvy_l2pre'))
        self.assertTrue(data_exists('mms1_afg_b_gsm_srvy_l2pre'))
        self.assertTrue(data_exists('mms1_afg_b_dmpa_srvy_l2pre'))

    def test_load_scm_l1a(self):
        data = pyspedas.mms.scm(probe=1, level='l1a', trange=['2015-12-15', '2015-12-16'])
        self.assertTrue(data_exists('mms1_scm_acb_scm123_scsrvy_srvy_l1a'))

    def test_load_scm_l1a_brst(self):
        data = pyspedas.mms.scm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'], level='l1a')
        self.assertTrue(data_exists('mms1_scm_acb_scm123_scb_brst_l1a'))
        self.assertTrue(data_exists('mms1_scm_acb_scm123_schb_brst_l1a'))

    def test_load_scm_l1b(self):
        data = pyspedas.mms.scm(probe=4, level='l1b', trange=['2015-12-15', '2015-12-16'])
        self.assertTrue(data_exists('mms4_scm_acb_scm123_scsrvy_srvy_l1b'))

    def test_load_edp_l1b(self):
        data = pyspedas.mms.edp(probe=1, level='l1b', trange=['2015-12-15', '2015-12-16'])
        self.assertTrue(data_exists('mms1_edp_dce_sensor'))
        self.assertTrue(data_exists('mms1_edp_dcv_sensor'))

    def test_load_edi_ql(self):
        data = pyspedas.mms.edi(probe=1, level='ql', trange=['2015-12-15', '2015-12-16'])
        self.assertTrue(data_exists('mms1_edi_E_dmpa'))
        self.assertTrue(data_exists('mms1_edi_v_ExB_dmpa'))

    def test_load_fpi_sitl(self):
        data = pyspedas.mms.fpi(probe=4, level='sitl', trange=['2015-12-15', '2015-12-16']) 
        self.assertTrue(data_exists('mms4_fpi_ePitchAngDist_avg'))

    def test_load_fpi_ql(self):
        data = pyspedas.mms.fpi(probe=1, level='ql', trange=['2015-12-15', '2015-12-16']) 
        self.assertTrue(data_exists('mms1_des_energyspectr_omni_fast'))
        self.assertTrue(data_exists('mms1_des_energyspectr_py_fast'))

    def test_load_hpca_l1b(self):
        trange = ['2015-10-16/13:06', '2015-10-16/13:07']
        data = pyspedas.mms.hpca(probe=1, level='l1b', trange=trange, data_rate='brst')
        data = pyspedas.mms.hpca(probe=1, level='l1b', trange=trange, data_rate='brst', datatype='ion')
        data = pyspedas.mms.hpca(probe=1, level='l1b', trange=trange, data_rate='brst', datatype='combined')
        data = pyspedas.mms.hpca(probe=1, level='l1b', trange=trange, data_rate='brst', datatype='rf_corr')
        data = pyspedas.mms.hpca(probe=1, level='l1b', trange=trange, data_rate='brst', datatype='count_rate')
        data = pyspedas.mms.hpca(probe=1, level='l1b', trange=trange, data_rate='brst', datatype='flux')
        data = pyspedas.mms.hpca(probe=1, level='l1b', trange=trange, data_rate='brst', datatype='vel_dist')
        data = pyspedas.mms.hpca(probe=1, level='l1b', trange=trange, data_rate='brst', datatype='bkgd_corr')
        mms_hpca_calc_anodes(fov=[0, 360])
        self.assertTrue(data_exists('mms1_hpca_hplus_number_density'))
        self.assertTrue(data_exists('mms1_hpca_heplus_number_density'))
        self.assertTrue(data_exists('mms1_hpca_heplusplus_number_density'))
        self.assertTrue(data_exists('mms1_hpca_oplus_number_density'))
        self.assertTrue(data_exists('mms1_hpca_heplusplus_RF_corrected'))
        self.assertTrue(data_exists('mms1_hpca_oplusplus_count_rate_elev_0-360'))


if __name__ == '__main__':
    unittest.main()