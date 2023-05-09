import unittest
import pyspedas
from pytplot import data_exists
from pyspedas.mms.cotrans.mms_qcotrans import mms_qcotrans
from pyspedas.mms.cotrans.mms_cotrans_lmn import mms_cotrans_lmn


class CotransTestCases(unittest.TestCase):
    def test_qcotrans_sm_to_gse(self):
        pyspedas.mms.mec()
        mms_qcotrans('mms1_mec_v_sm', 'mms1_mec_v_sm_2gse', out_coord='gse')
        mms_qcotrans('mms1_mec_r_sm', 'mms1_mec_r_sm_2gse', out_coord='gse')
        self.assertTrue(data_exists('mms1_mec_v_sm_2gse'))
        self.assertTrue(data_exists('mms1_mec_r_sm_2gse'))

    def test_lmn(self):
        pyspedas.mms.fgm(trange=['2015-10-16/13:00', '2015-10-16/13:10'], data_rate='brst')
        mms_cotrans_lmn('mms1_fgm_b_gsm_brst_l2_bvec', 'mms1_fgm_b_gsm_brst_l2_bvec_2lmn')
        self.assertTrue(data_exists('mms1_fgm_b_gsm_brst_l2_bvec_2lmn'))


if __name__ == '__main__':
    unittest.main()
