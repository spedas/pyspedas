import os
import unittest
from pytplot import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_celias_data(self):
        out_vars = pyspedas.projects.soho.celias(time_clip=True)
        self.assertTrue(data_exists('V_p'))
        self.assertTrue(data_exists('N_p'))
    
    def test_load_celias_data_prefix_none(self):
        out_vars = pyspedas.projects.soho.celias(time_clip=True, prefix=None)
        self.assertTrue(data_exists('V_p'))
        self.assertTrue(data_exists('N_p'))
    
    def test_load_celias_data_suffix_none(self):
        out_vars = pyspedas.projects.soho.celias(time_clip=True, suffix=None)
        self.assertTrue(data_exists('V_p'))
        self.assertTrue(data_exists('N_p'))

    def test_load_celias_data_prefix_suffix(self):
        out_vars = pyspedas.projects.soho.celias(time_clip=True, prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_V_p_suf'))
        self.assertTrue(data_exists('pre_N_p_suf'))

    def test_load_cosp_data(self):
        out_vars = pyspedas.projects.soho.costep(time_clip=True)
        self.assertTrue(data_exists('P_int'))
        self.assertTrue(data_exists('He_int'))

    def test_load_cosp_data_prefix_none(self):
        out_vars = pyspedas.projects.soho.costep(time_clip=True, prefix=None)
        self.assertTrue(data_exists('P_int'))
        self.assertTrue(data_exists('He_int'))

    def test_load_cosp_data_suffix_none(self):
        out_vars = pyspedas.projects.soho.costep(time_clip=True, suffix=None)
        self.assertTrue(data_exists('P_int'))
        self.assertTrue(data_exists('He_int'))

    def test_load_cosp_data_prefix_suffix(self):
        out_vars = pyspedas.projects.soho.costep(time_clip=True, prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_P_int_suf'))
        self.assertTrue(data_exists('pre_He_int_suf'))    

    def test_load_erne_data(self):
        out_vars = pyspedas.projects.soho.erne(time_clip=True)
        self.assertTrue(data_exists('PH'))

    def test_load_erne_data_prefix_none(self):
        out_vars = pyspedas.projects.soho.erne(time_clip=True, prefix=None)
        self.assertTrue(data_exists('PH'))

    def test_load_erne_data_suffix_none(self):
        out_vars = pyspedas.projects.soho.erne(time_clip=True, suffix=None)
        self.assertTrue(data_exists('PH'))

    def test_load_erne_data_prefix_suffix(self):
        out_vars = pyspedas.projects.soho.erne(time_clip=True, prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_PH_suf'))

    def test_load_orbit_data(self):
        out_vars = pyspedas.projects.soho.orbit(time_clip=True)
        self.assertTrue(data_exists('GSE_POS'))
        self.assertTrue(data_exists('GSE_VEL'))

    def test_load_orbit_data_prefix_none(self):
        out_vars = pyspedas.projects.soho.orbit(time_clip=True, prefix=None)
        self.assertTrue(data_exists('GSE_POS'))
        self.assertTrue(data_exists('GSE_VEL'))

    def test_load_orbit_data_suffix_none(self):
        out_vars = pyspedas.projects.soho.orbit(time_clip=True, suffix=None)
        self.assertTrue(data_exists('GSE_POS'))
        self.assertTrue(data_exists('GSE_VEL'))

    def test_load_orbit_data_prefix_suffix(self):
        out_vars = pyspedas.projects.soho.orbit(time_clip=True, prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_GSE_POS_suf'))
        self.assertTrue(data_exists('pre_GSE_VEL_suf'))

    def test_load_notplot(self):
        out_vars = pyspedas.projects.soho.erne(notplot=True)
        self.assertTrue('PH' in out_vars)

    def test_downloadonly(self):
        files = pyspedas.projects.soho.erne(downloadonly=True, trange=['2006-06-01', '2006-06-02'])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()

    