import unittest
import pyspedas
from pytplot import data_exists, tplot_rename, set_coords
from pyspedas.mms.cotrans.mms_qcotrans import mms_qcotrans
from pyspedas.mms.cotrans.mms_cotrans_lmn import mms_cotrans_lmn


class CotransTestCases(unittest.TestCase):
    def test_qcotrans_sm_to_gse(self):
        pyspedas.mms.mec()
        mms_qcotrans('mms1_mec_v_sm', 'mms1_mec_v_sm_2gse', out_coord='gse')
        mms_qcotrans('mms1_mec_r_sm', 'mms1_mec_r_sm_2gse', out_coord='gse')
        self.assertTrue(data_exists('mms1_mec_v_sm_2gse'))
        self.assertTrue(data_exists('mms1_mec_r_sm_2gse'))
        mms_qcotrans(['mms1_mec_r_sm', 'mms1_mec_v_sm'], ['mms1_mec_r_sm_2gse', 'mms1_mec_v_sm_2gse'], out_coord=['gse', 'gse'])

    def test_qcotrans_fgm_sm_to_gse(self):
        pyspedas.mms.mec()
        pyspedas.mms.fgm()
        mms_qcotrans('mms1_fgm_b_gsm_srvy_l2_bvec', 'mms1_fgm_b_gsm_brst_l2_bvec_2gse', probe=1, out_coord='gse')
        self.assertTrue(data_exists('mms1_fgm_b_gsm_brst_l2_bvec_2gse'))

    def test_qcotrans_errors(self):
        pyspedas.mms.mec()
        # in_name not specified
        mms_qcotrans(out_name='mms1_mec_v_sm_2gse', out_coord='gse')
        # out_name not specified
        mms_qcotrans(in_name='mms1_mec_v_sm_2gse', out_coord='gse')
        # in_coord not specified, and not set in metadata
        set_coords('mms1_mec_v_sm', '')
        mms_qcotrans(in_name='mms1_mec_v_sm', out_name='mms1_mec_v_sm_2gse', out_coord='gse')
        # invalid in_coord
        set_coords('mms1_mec_v_sm', '')
        mms_qcotrans(in_name='mms1_mec_v_sm', out_name='mms1_mec_v_sm_2gse2', out_coord='gse')
        # invalid out_coord
        set_coords('mms1_mec_v_sm', 'sm')
        mms_qcotrans(in_name='mms1_mec_v_sm', out_name='mms1_mec_v_sm_2gse2', out_coord='gse2')
        # trouble extracting probe from var name
        tplot_rename('mms1_mec_v_sm', 'mmsx_mec_v_sm')
        mms_qcotrans(in_name='mmsx_mec_v_sm', out_name='mms1_mec_v_sm_2gse2', out_coord='gse2')
        tplot_rename('mms1_mec_v_sm', 'smvar')
        mms_qcotrans(in_name='smvar', out_name='mms1_mec_v_sm_2gse', out_coord='gse')
        # should warn when you're transforming to ssl/bcs coordinates
        mms_qcotrans(out_name='mms1_mec_v_sm_2ssl', out_coord='ssl')
        mms_qcotrans(out_name='mms1_mec_v_sm_2bcs', out_coord='bcs')
        # unsupported coordinate system
        mms_qcotrans(in_name='mms1_mec_v_sm', out_name='mms1_mec_v_sm_2gse', in_coord='unsupported', out_coord='gse')


    def test_lmn(self):
        pyspedas.mms.fgm(trange=['2015-10-16/13:00', '2015-10-16/13:10'], data_rate='brst')
        mms_cotrans_lmn('mms1_fgm_b_gsm_brst_l2_bvec', 'mms1_fgm_b_gsm_brst_l2_bvec_2lmn')
        self.assertTrue(data_exists('mms1_fgm_b_gsm_brst_l2_bvec_2lmn'))

    def test_lmn_errors(self):
        pyspedas.mms.fgm(trange=['2015-10-16/13:00', '2015-10-16/13:10'], data_rate='brst')
        # invalid variable name
        mms_cotrans_lmn('mms1_fgm_b_gsm_brst_l2_bvec2', 'mms1_fgm_b_gsm_brst_l2_bvec_2lmn')
        # invalid coordinate system
        set_coords('mms1_fgm_b_gsm_brst_l2_bvec', 'gse2')
        mms_cotrans_lmn('mms1_fgm_b_gsm_brst_l2_bvec', 'mms1_fgm_b_gsm_brst_l2_bvec_2lmn')
        # problem extracting probe from variable name
        tplot_rename('mms1_fgm_b_gsm_brst_l2_bvec', 'mmsx_fgm_b_gsm_brst_l2_bvec')
        mms_cotrans_lmn('mmsx_fgm_b_gsm_brst_l2_bvec', 'mms1_fgm_b_gsm_brst_l2_bvec_2lmn')


if __name__ == '__main__':
    unittest.main()
