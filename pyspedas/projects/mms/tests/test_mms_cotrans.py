import unittest
import pyspedas
from pyspedas.tplot_tools import data_exists, tplot_rename, set_coords
from pyspedas.projects.mms.cotrans.mms_qcotrans import mms_qcotrans
from pyspedas.projects.mms.cotrans.mms_cotrans_lmn import mms_cotrans_lmn
from numpy.testing import assert_allclose


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

    def test_qcotrans_fgm_srvy_gsm_to_gse(self):
        pyspedas.projects.mms.mec()
        pyspedas.projects.mms.fgm()
        mms_qcotrans('mms1_fgm_b_gsm_srvy_l2_bvec', 'mms1_fgm_b_gsm_srvy_l2_bvec_2gse', probe=1, out_coord='gse')
        #pyspedas.tplot(['mms1_fgm_b_gsm_srvy_l2_bvec_2gse','mms1_fgm_b_gse_srvy_l2_bvec'],trange=['2015-10-16/10:15','2015-10-16/10:45'])
        self.assertTrue(data_exists('mms1_fgm_b_gsm_srvy_l2_bvec_2gse'))
        d1=pyspedas.get_data('mms1_fgm_b_gsm_srvy_l2_bvec_2gse')
        d2=pyspedas.get_data('mms1_fgm_b_gse_srvy_l2_bvec')
        diff = d2.y - d1.y
        #pyspedas.store_data('diff',data={'x':d1.times, 'y':diff})
        #pyspedas.tplot(['mms1_fgm_b_gsm_srvy_l2_bvec_2gse','mms1_fgm_b_gse_srvy_l2_bvec','diff'])
        assert_allclose(d1.y, d2.y,atol=1.0, rtol=1e-6)
        # Test inverse transform
        mms_qcotrans('mms1_fgm_b_gsm_srvy_l2_bvec_2gse', out_name='mms1_fgm_b_gsm_srvy_l2_bvec_2gse2gsm', probe=1, out_coord='gsm')
        d3 = pyspedas.get_data('mms1_fgm_b_gsm_srvy_l2_bvec_2gse2gsm')
        d4 = pyspedas.get_data('mms1_fgm_b_gsm_srvy_l2_bvec')
        assert_allclose(d3.y, d4.y,atol=1.0, rtol=1e-6)

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
            mms_qcotrans(in_name='mmsx_mec_v_sm', out_name='mms1_mec_v_sm_2gse2', out_coord='gse')
            self.assertIn("Unknown probe for variable: mmsx_mec_v_sm", log.output[5])
            tplot_rename('mms1_mec_v_sm', 'smvar')
            mms_qcotrans(in_name='smvar', out_name='mms1_mec_v_sm_2gse', out_coord='gse')
            self.assertIn("Could not determine coordinate system for: smvar", log.output[6])

            # should warn when you're transforming to ssl/bcs coordinates
            mms_qcotrans(out_name='mms1_mec_v_sm_2ssl', out_coord='ssl')
            self.assertIn("Input variable name is missing", log.output[7])
            mms_qcotrans(out_name='mms1_mec_v_sm_2bcs', out_coord='bcs')
            self.assertIn("Input variable name is missing", log.output[8])

            # unsupported coordinate system
            mms_qcotrans(in_name='mms1_mec_v_sm', out_name='mms1_mec_v_sm_2gse', in_coord='unsupported', out_coord='gse')
            self.assertIn("Unsupported input coordinate system: unsupported", log.output[9])
            


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
