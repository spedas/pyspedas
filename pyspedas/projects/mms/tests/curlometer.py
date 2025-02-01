
import unittest
import pyspedas
from pytplot import data_exists
from pyspedas.projects.mms.fgm_tools.mms_lingradest import mms_lingradest

class CurlTestCases(unittest.TestCase):
    def test_default(self):
        data = pyspedas.projects.mms.fgm(probe=[1, 2, 3, 4], trange=['2015-10-30/05:15:45', '2015-10-30/05:15:48'], data_rate='brst', time_clip=True, varformat='*_gse_*', get_fgm_ephemeris=True)
        curl = pyspedas.projects.mms.curlometer(positions=['mms1_fgm_r_gse_brst_l2', 'mms2_fgm_r_gse_brst_l2', 'mms3_fgm_r_gse_brst_l2', 'mms4_fgm_r_gse_brst_l2'], fields=['mms1_fgm_b_gse_brst_l2', 'mms2_fgm_b_gse_brst_l2', 'mms3_fgm_b_gse_brst_l2', 'mms4_fgm_b_gse_brst_l2'])
        self.assertTrue(data_exists('jtotal'))
        self.assertTrue(data_exists('curlB'))
        self.assertTrue(data_exists('divB'))
        self.assertTrue(data_exists('jpar'))
        self.assertTrue(data_exists('jperp'))

    def test_lingradest(self):
        data = pyspedas.projects.mms.fgm(probe=[1, 2, 3, 4], trange=['2015-10-30/05:15:45', '2015-10-30/05:15:48'], data_rate='brst', time_clip=True, varformat='*_gse_*', get_fgm_ephemeris=True)
        fields = ['mms'+prb+'_fgm_b_gse_brst_l2' for prb in ['1', '2', '3', '4']]
        positions = ['mms'+prb+'_fgm_r_gse_brst_l2' for prb in ['1', '2', '3', '4']]
        curl = mms_lingradest(fields=fields, positions=positions, suffix='_lingradest')
        self.assertTrue(data_exists('Bx_lingradest'))
        self.assertTrue(data_exists('By_lingradest'))
        self.assertTrue(data_exists('Bz_lingradest'))
        self.assertTrue(data_exists('gradBx_lingradest'))
        self.assertTrue(data_exists('gradBy_lingradest'))
        self.assertTrue(data_exists('gradBz_lingradest'))
        self.assertTrue(data_exists('jx_lingradest'))
        self.assertTrue(data_exists('jy_lingradest'))
        self.assertTrue(data_exists('jz_lingradest'))
        self.assertTrue(data_exists('absCB_lingradest'))
        self.assertTrue(data_exists('CxB_lingradest'))
        self.assertTrue(data_exists('CyB_lingradest'))
        self.assertTrue(data_exists('CzB_lingradest'))
        self.assertTrue(data_exists('curvx_lingradest'))
        self.assertTrue(data_exists('curvy_lingradest'))
        self.assertTrue(data_exists('curvz_lingradest'))

    def test_lingradest_wrapper(self):
        data = pyspedas.projects.mms.fgm(probe=[1, 2, 3, 4], trange=['2015-10-30/05:15:45', '2015-10-30/05:15:48'], data_rate='brst', time_clip=True, varformat='*_gse_*', get_fgm_ephemeris=True)
        fields = ['mms'+prb+'_fgm_b_gse_brst_l2' for prb in ['1', '2', '3', '4']]
        positions = ['mms'+prb+'_fgm_r_gse_brst_l2' for prb in ['1', '2', '3', '4']]
        curl = pyspedas.projects.mms.lingradest(fields=fields, positions=positions, suffix='_lingradest')
        self.assertTrue(data_exists('Bx_lingradest'))
        self.assertTrue(data_exists('By_lingradest'))
        self.assertTrue(data_exists('Bz_lingradest'))
        self.assertTrue(data_exists('gradBx_lingradest'))
        self.assertTrue(data_exists('gradBy_lingradest'))
        self.assertTrue(data_exists('gradBz_lingradest'))
        self.assertTrue(data_exists('jx_lingradest'))
        self.assertTrue(data_exists('jy_lingradest'))
        self.assertTrue(data_exists('jz_lingradest'))
        self.assertTrue(data_exists('absCB_lingradest'))
        self.assertTrue(data_exists('CxB_lingradest'))
        self.assertTrue(data_exists('CyB_lingradest'))
        self.assertTrue(data_exists('CzB_lingradest'))
        self.assertTrue(data_exists('curvx_lingradest'))
        self.assertTrue(data_exists('curvy_lingradest'))
        self.assertTrue(data_exists('curvz_lingradest'))

if __name__ == '__main__':
    unittest.main()