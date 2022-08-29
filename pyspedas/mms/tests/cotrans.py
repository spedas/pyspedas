import unittest
import pyspedas
from pyspedas.utilities.data_exists import data_exists
from pyspedas.mms.cotrans.mms_qcotrans import mms_qcotrans

class CotransTestCases(unittest.TestCase):
    def test_qcotrans_sm_to_gse(self):
        pyspedas.mms.mec()
        mms_qcotrans('mms1_mec_v_sm', 'mms1_mec_v_sm_2gse', out_coord='gse')
        mms_qcotrans('mms1_mec_r_sm', 'mms1_mec_r_sm_2gse', out_coord='gse')
        self.assertTrue(data_exists('mms1_mec_v_sm_2gse'))
        self.assertTrue(data_exists('mms1_mec_r_sm_2gse'))

if __name__ == '__main__':
    unittest.main()