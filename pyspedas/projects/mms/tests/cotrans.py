import unittest
import pyspedas
from pytplot import data_exists, tplot_rename, set_coords
from pyspedas.projects.mms.cotrans.mms_qcotrans import mms_qcotrans
from pyspedas.projects.mms.cotrans.mms_cotrans_lmn import mms_cotrans_lmn


class CotransTestCases(unittest.TestCase):
    def test_qcotrans_sm_to_gse(self):
        pyspedas.projects.mms.mec()
        ret1 = mms_qcotrans('mms1_mec_v_sm', 'mms1_mec_v_sm_2gse', out_coord='gse')
        ret2 = mms_qcotrans('mms1_mec_r_sm', 'mms1_mec_r_sm_2gse', out_coord='gse')
        self.assertTrue(data_exists('mms1_mec_v_sm_2gse'))
        self.assertTrue('mms1_mec_v_sm_2gse' in ret1)
        self.assertTrue('mms1_mec_r_sm_2gse' in ret2)
        self.assertTrue(data_exists('mms1_mec_r_sm_2gse'))
        mms_qcotrans(['mms1_mec_r_sm', 'mms1_mec_v_sm'], ['mms1_mec_r_sm_2gse', 'mms1_mec_v_sm_2gse'], out_coord=['gse', 'gse'])

    def test_qcotrans_fgm_sm_to_gse(self):
        pyspedas.projects.mms.mec()
        pyspedas.projects.mms.fgm()
        mms_qcotrans('mms1_fgm_b_gsm_srvy_l2_bvec', 'mms1_fgm_b_gsm_brst_l2_bvec_2gse', probe=1, out_coord='gse')
        self.assertTrue(data_exists('mms1_fgm_b_gsm_brst_l2_bvec_2gse'))

    def test_qcotrans_errors(self):
        with self.assertLogs(level='WARNING') as log:
            pyspedas.projects.mms.mec()

            # in_name not specified
            mms_qcotrans(out_name='mms1_mec_v_sm_2gse', out_coord='gse')
            self.assertIn("Input variable name is missing", log.output[0])

            # out_name not specified
            mms_qcotrans(in_name='mms1_mec_v_sm_2gse', out_coord='gse')
            self.assertIn("Output variable name is missing", log.output[1])

            # in_coord not specified, and not set in metadata
            set_coords('mms1_mec_v_sm', '')
            mms_qcotrans(in_name='mms1_mec_v_sm', out_name='mms1_mec_v_sm_2gse', out_coord='gse')
            self.assertIn("Could not determine coordinate system for: mms1_mec_v_sm", log.output[2])

            # invalid in_coord
            set_coords('mms1_mec_v_sm', '')
            mms_qcotrans(in_name='mms1_mec_v_sm', out_name='mms1_mec_v_sm_2gse2', out_coord='gse')
            self.assertIn("Could not determine coordinate system for: mms1_mec_v_sm", log.output[3])

            # invalid out_coord
            set_coords('mms1_mec_v_sm', 'sm')
            mms_qcotrans(in_name='mms1_mec_v_sm', out_name='mms1_mec_v_sm_2gse2', out_coord='gse2')
            self.assertIn("Unsupported output coordinate system: gse2", log.output[4])

            # trouble extracting probe from var name
            tplot_rename('mms1_mec_v_sm', 'mmsx_mec_v_sm')
            mms_qcotrans(in_name='mmsx_mec_v_sm', out_name='mms1_mec_v_sm_2gse2', out_coord='gse2')
            tplot_rename('mms1_mec_v_sm', 'smvar')
            mms_qcotrans(in_name='smvar', out_name='mms1_mec_v_sm_2gse', out_coord='gse')
            self.assertIn("Problem occurred during the transformation", log.output[5])
            self.assertIn("Unsupported output coordinate system: gse2", log.output[6])
            self.assertIn("Unknown probe for variable: mmsx_mec_v_sm", log.output[7])
            self.assertIn("Could not determine coordinate system for: smvar", log.output[8])

            # should warn when you're transforming to ssl/bcs coordinates
            mms_qcotrans(out_name='mms1_mec_v_sm_2ssl', out_coord='ssl')
            mms_qcotrans(out_name='mms1_mec_v_sm_2bcs', out_coord='bcs')
            self.assertIn("Input variable name is missing", log.output[9])
            self.assertIn("Input variable name is missing", log.output[10])

            # unsupported coordinate system
            mms_qcotrans(in_name='mms1_mec_v_sm', out_name='mms1_mec_v_sm_2gse', in_coord='unsupported', out_coord='gse')
            self.assertIn("Unsupported input coordinate system: unsupported", log.output[11])
            


    def test_lmn(self):
        pyspedas.projects.mms.fgm(trange=['2015-10-16/13:00', '2015-10-16/13:10'], data_rate='brst')
        mms_cotrans_lmn('mms1_fgm_b_gsm_brst_l2_bvec', 'mms1_fgm_b_gsm_brst_l2_bvec_2lmn')
        self.assertTrue(data_exists('mms1_fgm_b_gsm_brst_l2_bvec_2lmn'))

    def test_lmn_errors(self):
        with self.assertLogs(level='ERROR') as log:
            pyspedas.projects.mms.fgm(trange=['2015-10-16/13:00', '2015-10-16/13:10'], data_rate='brst')

            # invalid variable name
            mms_cotrans_lmn('mms1_fgm_b_gsm_brst_l2_bvec2', 'mms1_fgm_b_gsm_brst_l2_bvec_2lmn')
            self.assertIn("Error reading tplot variable: mms1_fgm_b_gsm_brst_l2_bvec2", log.output[0])

            # invalid coordinate system
            set_coords('mms1_fgm_b_gsm_brst_l2_bvec', 'gse2')
            mms_cotrans_lmn('mms1_fgm_b_gsm_brst_l2_bvec', 'mms1_fgm_b_gsm_brst_l2_bvec_2lmn')
            self.assertIn("Please specify the coordinate system of the input data", log.output[1])

            # problem extracting probe from variable name
            tplot_rename('mms1_fgm_b_gsm_brst_l2_bvec', 'mmsx_fgm_b_gsm_brst_l2_bvec')
            mms_cotrans_lmn('mmsx_fgm_b_gsm_brst_l2_bvec', 'mms1_fgm_b_gsm_brst_l2_bvec_2lmn')
            self.assertIn("Please specify the coordinate system of the input data", log.output[2])            


if __name__ == '__main__':
    unittest.main()
