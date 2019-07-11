#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import numpy as np

from ...mms import mms_load_fgm, mms_load_scm, mms_load_fpi, mms_load_hpca, mms_load_eis, mms_load_feeps, mms_load_edp, mms_load_edi, mms_load_aspoc, mms_load_dsp
from ...utilities.data_exists import data_exists
from ..hpca.mms_hpca_calc_anodes import mms_hpca_calc_anodes
from ..hpca.mms_hpca_spin_sum import mms_hpca_spin_sum

from pytplot import get_data

class DSPLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_dsp(trange=['2015-08-01','2015-09-01'], datatype='swd', level='l2', data_rate='fast')
        self.assertTrue(data_exists('mms1_dsp_swd_E12_Counts'))

class FEEPSLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_feeps(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_epd_feeps_srvy_l2_electron_bottom_intensity_sensorid_12'))

class EISLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_eis(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_epd_eis_phxtof_proton_flux_omni'))

class FPILoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_fpi(trange=['2015-10-16/14:00', '2015-10-16/15:00'])
        self.assertTrue(data_exists('mms1_dis_energyspectr_omni_fast'))

    def test_load_small_brst_interval(self):
        data = mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', datatype='dis-moms')
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

class HPCALoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_hpca(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_hpca_hplus_number_density'))

    def test_load_ion_data(self):
        data = mms_load_hpca(trange=['2015-10-16/5:00', '2015-10-16/6:00'], datatype='ion')
        self.assertTrue(data_exists('mms1_hpca_hplus_number_density'))

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

class EDILoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_edi(trange=['2016-10-17/13:00', '2016-10-17/14:00'])
        self.assertTrue(data_exists('mms1_edi_e_gse_srvy_l2'))

class ASPOCLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_aspoc(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_aspoc_ionc'))

class EDPLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_edp(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_edp_dce_gse_fast_l2'))

    def test_load_multiple_sc(self):
        data = mms_load_edp(probe=['1', '2', '3', '4'], trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_edp_dce_gse_fast_l2'))
        self.assertTrue(data_exists('mms2_edp_dce_gse_fast_l2'))
        self.assertTrue(data_exists('mms3_edp_dce_gse_fast_l2'))
        self.assertTrue(data_exists('mms4_edp_dce_gse_fast_l2'))

    def test_load_brst_data(self):
        data = mms_load_edp(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'])
        self.assertTrue(data_exists('mms1_edp_dce_gse_brst_l2'))

class FGMLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_fgm(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_fgm_b_gse_srvy_l2'))

    def test_load_multiple_sc(self):
        data = mms_load_fgm(probe=['1', '2', '3', '4'], trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_fgm_b_gse_srvy_l2'))
        self.assertTrue(data_exists('mms2_fgm_b_gse_srvy_l2'))
        self.assertTrue(data_exists('mms3_fgm_b_gse_srvy_l2'))
        self.assertTrue(data_exists('mms4_fgm_b_gse_srvy_l2'))

    def test_load_brst_data(self):
        data = mms_load_fgm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'])
        self.assertTrue(data_exists('mms1_fgm_b_gse_brst_l2'))

    def test_load_int_probes(self):
        data = mms_load_fgm(probe=[1, 2, 3, 4], trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_fgm_b_gse_srvy_l2'))

class SCMLoadTestCases(unittest.TestCase):
    def test_load_default_data(self):
        data = mms_load_scm(trange=['2015-10-16', '2015-10-16/01:00'])
        self.assertTrue(data_exists('mms1_scm_acb_gse_scsrvy_srvy_l2'))

    def test_load_multiple_sc(self):
        data = mms_load_scm(probe=['1', '2', '3', '4'], trange=['2017-12-15', '2017-12-16'])
        # self.assertTrue(data_exists('mms1_scm_acb_gse_scsrvy_srvy_l2'))
        # self.assertTrue(data_exists('mms2_scm_acb_gse_scsrvy_srvy_l2'))
        self.assertTrue(data_exists('mms3_scm_acb_gse_scsrvy_srvy_l2'))
        self.assertTrue(data_exists('mms4_scm_acb_gse_scsrvy_srvy_l2'))

    def test_load_brst_data(self):
        data = mms_load_scm(data_rate='brst', trange=['2015-10-16/13:06', '2015-10-16/13:10'])
        self.assertTrue(data_exists('mms1_scm_acb_gse_scb_brst_l2'))

if __name__ == '__main__':
    unittest.main()