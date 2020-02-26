
import unittest
import pyspedas
from pyspedas.utilities.data_exists import data_exists

class CurlTestCases(unittest.TestCase):
    def test_default(self):
        data = pyspedas.mms.fgm(probe=[1, 2, 3, 4], trange=['2015-10-30/05:15:45', '2015-10-30/05:15:48'], data_rate='brst', time_clip=True, varformat='*_gse_*')
        curl = pyspedas.mms.curlometer(positions=['mms1_fgm_r_gse_brst_l2', 'mms2_fgm_r_gse_brst_l2', 'mms3_fgm_r_gse_brst_l2', 'mms4_fgm_r_gse_brst_l2'], fields=['mms1_fgm_b_gse_brst_l2', 'mms2_fgm_b_gse_brst_l2', 'mms3_fgm_b_gse_brst_l2', 'mms4_fgm_b_gse_brst_l2'])
        self.assertTrue(data_exists('jtotal'))
        self.assertTrue(data_exists('curlB'))
        self.assertTrue(data_exists('divB'))
        self.assertTrue(data_exists('jpar'))
        self.assertTrue(data_exists('jperp'))

if __name__ == '__main__':
    unittest.main()