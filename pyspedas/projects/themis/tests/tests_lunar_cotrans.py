"""Tests of gse2sse and sse2sel functions."""
import unittest
from numpy.testing import assert_array_almost_equal_nulp, assert_array_max_ulp, assert_allclose
from copy import deepcopy
from pytplot import data_exists, get_data, store_data, cdf_to_tplot, del_data, tplot_restore, replace_metadata
from pytplot import get_coords,set_coords
from pyspedas.projects.themis import gse2sse,sse2sel



class LunCotransDataValidation(unittest.TestCase):
    """ Compares cotrans results between Python and IDL """

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The SPEDAS script that creates the file: projects/themis/state/cotrans/thm_cotrans_validate.pro
        """
        from pyspedas.utilities.download import download
        from pyspedas.projects.themis.config import CONFIG

        # Testing time range
        cls.t = ['2008-03-23', '2008-03-28']

        # Testing tolerance
        cls.tol = 1e-10

        # Download tplot files
        remote_server = 'https://github.com/spedas/test_data/raw/refs/heads/main/'
        #remote_name = 'testfiles/thm_cotrans_validate.cdf'
        remote_name = 'cotrans_tools/thm_cotrans_validate.tplot'
        datafile = download(remote_file=remote_name,
                            remote_path=remote_server,
                            local_path=CONFIG['local_data_dir'],
                            no_download=False)
        if not datafile:
            # Skip tests
            raise unittest.SkipTest("Cannot download data validation file")

        # Load validation variables from the test file
        del_data('*')
        filename = datafile[0]
        #cdf_to_tplot(filename)
        tplot_restore(filename)
        # pytplot.tplot_names()
        # Input variables
        #coord_set_coord('tha_state_pos_gse','gse')
        #coord_set_coord('tha_state_vel_gse','gse')
        cls.tha_state_pos_gse = get_data('tha_state_pos_gse')
        cls.tha_state_vel_gse = get_data('tha_state_vel_gse')
        #coord_set_coord('tha_fgs_gse','gse')
        cls.tha_fgs_gse = get_data('tha_fgs_gse')
        # GSE<->SSE results
        #coord_set_coord('tha_state_pos_sse','sse')
        #coord_set_coord('tha_state_vel_sse','sse')
        cls.tha_state_pos_sse = get_data('tha_state_pos_sse')
        cls.tha_state_vel_sse = get_data('tha_state_vel_sse')
        #coord_set_coord('tha_state_pos_sse_rotate_only','sse')
        #coord_set_coord('tha_state_vel_sse_rotate_only','sse')
        cls.tha_state_pos_sse_rotate_only = get_data('tha_state_pos_sse_rotate_only')
        cls.tha_state_vel_sse_rotate_only = get_data('tha_state_vel_sse_rotate_only')
        #coord_set_coord('tha_fgs_sse','sse')
        cls.tha_fgs_sse = get_data('tha_fgs_sse')
        #coord_set_coord('tha_fgs_sel','sel')
        cls.tha_fgs_sel = get_data('tha_fgs_sel')

        #coord_set_coord('tha_state_pos_gse_sse_gse','gse')
        #coord_set_coord('tha_state_vel_gse_sse_gse','gse')
        cls.tha_state_pos_gse_sse_gse = get_data('tha_state_pos_gse_sse_gse')
        cls.tha_state_vel_gse_sse_gse = get_data('tha_state_vel_gse_sse_gse')

        #coord_set_coord('tha_state_pos_gse_sse_gse_rotate_only','gse')
        #coord_set_coord('tha_state_vel_gse_sse_gse_rotate_only','gse')
        cls.tha_state_pos_gse_sse_gse_rotate_only = get_data('tha_state_pos_gse_sse_gse_rotate_only')
        cls.tha_state_vel_gse_sse_gse_rotate_only = get_data('tha_state_vel_gse_sse_gse_rotate_only')

        #coord_set_coord('tha_fgs_gse_sse_gse','gse')
        cls.tha_fgs_gse_sse_gse = get_data('tha_fgs_gse_sse_gse')

        # SSE<->SSL results
        #coord_set_coord('tha_state_pos_sel','sel')
        cls.tha_state_pos_sel = get_data('tha_state_pos_sel')

        #coord_set_coord('tha_state_pos_gse_sel_sse','sse')
        #coord_set_coord('tha_state_vel_gse_sel_sse','sse')
        cls.tha_state_pos_gse_sel_sse = get_data('tha_state_pos_gse_sel_sse')
        cls.sse_mat_cotrans = get_data('sse_mat_cotrans')
        cls.sel_mat_cotrans = get_data('sel_mat_cotrans')
        cls.sel_x_gei = get_data('sel_x_gei')
        cls.sel_x_gse = get_data('sel_x_gse')
        cls.sel_x_sse = get_data('sel_x_sse')
        cls.sel_y_sse = get_data('sel_y_sse')
        cls.sel_z_sse = get_data('sel_z_sse')

        # It is no longer necessary to load or pass support data when calling gse2sse and sse2sel
        # autoload_support(varname='tha_state_pos_gse', slp=True)

    def setUp(self):
        """ We need to clean tplot variables before each run"""
        # del_data('*')

    def test_replace_metadata(self):
        data = get_data('tha_state_pos_gse')
        orig_meta = deepcopy(get_data('tha_state_pos_gse',metadata=True))
        orig_coord = get_coords('tha_state_pos_gse')
        self.assertEqual(orig_coord.lower(), 'gse')
        store_data('newvar',data={'x':data[0],'y':data[1]})
        replace_metadata('newvar',orig_meta)
        self.assertEqual(get_coords('newvar').lower(),'gse')
        orig_meta['data_att']['coord_sys'] = 'goofy'  # won't affect tha_state_pos_gse, should not affect newvar either
        self.assertEqual(get_coords('newvar').lower(),'gse')
        self.assertEqual(get_coords('tha_state_pos_gse').lower(),'gse')

    def test_gse2sse_pos(self):
        """ Validate gse2sse position transform """
        result = gse2sse('tha_state_pos_gse', 'tha_state_pos_sse', variable_type='pos')
        self.assertEqual(result,1)
        py_sse_mat_cotrans = get_data('sse_mat_cotrans')
        assert_allclose(py_sse_mat_cotrans.y, self.sse_mat_cotrans.y, atol=1.0e-06)
        pos_sse = get_data('tha_state_pos_sse')
        pos_meta = get_data('tha_state_pos_sse',metadata=True)
        self.assertEqual(pos_meta['data_att']['units'],'km')
        assert_allclose(pos_sse.y, self.tha_state_pos_sse.y, atol=0.1)
        self.assertEqual(get_coords('tha_state_pos_sse').lower(),'sse')

    def test_gse2sse_pos_rotate_only(self):
        """ Validate gse2sse position transform """
        result = gse2sse('tha_state_pos_gse', 'tha_state_pos_sse_rotate_only', variable_type='pos',rotation_only=True)
        self.assertEqual(result,1)
        pos_sse = get_data('tha_state_pos_sse_rotate_only')
        pos_meta = get_data('tha_state_pos_sse',metadata=True)
        self.assertEqual(pos_meta['data_att']['units'],'km')
        assert_allclose(pos_sse.y, self.tha_state_pos_sse_rotate_only.y, atol=0.1)
        self.assertEqual(get_coords('tha_state_pos_sse_rotate_only').lower(),'sse')

    def test_gse2sse_vel(self):
        """ Validate gse2sse velocity transform """
        result = gse2sse('tha_state_vel_gse', 'tha_state_vel_sse',variable_type='vel')
        self.assertEqual(result,1)
        vel_sse = get_data('tha_state_vel_sse')
        vel_meta = get_data('tha_state_vel_sse',metadata=True)
        self.assertEqual(vel_meta['data_att']['units'],'km/s')
        assert_allclose(vel_sse.y, self.tha_state_vel_sse.y, atol=1.0e-03)
        self.assertEqual(get_coords('tha_state_vel_sse').lower(),'sse')

    def test_gse2sse_vel_rotate_only(self):
        """ Validate gse2sse position transform """
        result = gse2sse('tha_state_vel_gse', 'tha_state_vel_sse_rotate_only', variable_type='vel',rotation_only=True)
        self.assertEqual(result,1)
        vel_sse = get_data('tha_state_vel_sse_rotate_only')
        vel_meta = get_data('tha_state_vel_sse',metadata=True)
        self.assertEqual(vel_meta['data_att']['units'],'km/s')
        assert_allclose(vel_sse.y, self.tha_state_vel_sse_rotate_only.y, atol=1.0e-03)
        self.assertEqual(get_coords('tha_state_vel_sse_rotate_only').lower(),'sse')

    def test_gse2sse_field(self):
        """ Validate gse2sse field transform """
        result = gse2sse('tha_fgs_gse', 'tha_fgs_sse')
        self.assertEqual(result, 1)
        fgs_sse = get_data('tha_fgs_sse')
        fgs_meta = get_data('tha_fgs_sse',metadata=True)
        self.assertEqual(fgs_meta['data_att']['units'],'nT')
        assert_allclose(fgs_sse.y, self.tha_fgs_sse.y, atol=1.0e-02)
        self.assertEqual(get_coords('tha_fgs_sse').lower(), 'sse')

    def test_sse2gse_pos(self):
        """ Validate sse2gse position transform """
        store_data('tha_state_pos_sse',data={'x':self.tha_state_pos_sse.times, 'y':self.tha_state_pos_sse.y})
        set_coords('tha_state_pos_sse','sse')
        before_meta = get_data('tha_state_pos_sse',metadata=True)
        before_meta['data_att']['units'] = 'km'
        result = gse2sse('tha_state_pos_sse', 'tha_state_pos_gse_sse_gse',isssetogse=True,
                         variable_type='pos')
        self.assertEqual(result,1)
        pos_gse = get_data('tha_state_pos_gse_sse_gse')
        pos_meta = get_data('tha_state_pos_gse_sse_gse',metadata=True)
        self.assertEqual(pos_meta['data_att']['units'],'km')
        assert_allclose(pos_gse.y, self.tha_state_pos_gse_sse_gse.y, atol=0.1)
        self.assertEqual(get_coords('tha_state_pos_gse_sse_gse').lower(),'gse')

    def test_sse2gse_pos_rotate_only(self):
        """ Validate sse2gse position transform """
        store_data('tha_state_pos_sse_rotate_only',
                           data={'x':self.tha_state_pos_sse_rotate_only.times, 'y':self.tha_state_pos_sse_rotate_only.y})
        set_coords('tha_state_pos_sse_rotate_only','sse')
        result = gse2sse('tha_state_pos_sse_rotate_only', 'tha_state_pos_gse_sse_gse_rotation_only',isssetogse=True,
                         variable_type='pos', rotation_only=True)
        self.assertEqual(result,1)
        pos_gse = get_data('tha_state_pos_gse_sse_gse_rotation_only')
        assert_allclose(pos_gse.y, self.tha_state_pos_gse_sse_gse_rotate_only.y, atol=0.1)
        self.assertEqual(get_coords('tha_state_pos_gse_sse_gse_rotate_only').lower(),'gse')

    def test_sse2gse_vel(self):
        """ Validate sse2gse velocity transform """
        result = gse2sse('tha_state_vel_sse', 'tha_state_vel_gse_sse_gse',isssetogse=True,
                         variable_type='vel')
        self.assertEqual(result,1)
        vel_gse = get_data('tha_state_vel_gse_sse_gse')
        assert_allclose(vel_gse.y, self.tha_state_vel_gse_sse_gse.y, atol=1.0e-02)
        self.assertEqual(get_coords('tha_state_vel_gse_sse_gse').lower(),'gse')

    def test_sse2gse_vel_rotate_only(self):
        """ Validate sse2gse position transform """
        store_data('tha_state_vel_sse_rotate_only',
                           data={'x':self.tha_state_vel_sse_rotate_only.times, 'y':self.tha_state_vel_sse_rotate_only.y})
        set_coords('tha_state_vel_sse_rotate_only','sse')
        result = gse2sse('tha_state_vel_sse_rotate_only', 'tha_state_vel_gse_sse_gse_rotation_only',isssetogse=True,
                         variable_type='pos', rotation_only=True)
        self.assertEqual(result,1)
        vel_gse = get_data('tha_state_vel_gse_sse_gse_rotation_only')
        assert_allclose(vel_gse.y, self.tha_state_vel_gse_sse_gse_rotate_only.y, atol=1.0e-03)
        self.assertEqual(get_coords('tha_state_vel_gse_sse_gse_rotate_only').lower(),'gse')

    def test_sse2gse_field(self):
        """ Validate gse2sse field transform """
        result = gse2sse('tha_fgs_sse','tha_fgs_gse_sse_gse',isssetogse=True)
        self.assertEqual(result, 1)
        fgs_gse = get_data('tha_fgs_gse_sse_gse')
        assert_allclose(fgs_gse.y, self.tha_fgs_gse_sse_gse.y, atol=1.0e-02)
        self.assertEqual(get_coords('tha_fgs_gse_sse_gse').lower(), 'gse')

    def test_sse2sel_pos(self):
        """ Validate sse2sel position transform """
        result = sse2sel('tha_state_pos_sse','tha_state_pos_sel')
        self.assertEqual(result,1)
        py_sel_x_gse = get_data('slp_lun_att_x_gse')
        assert_allclose(self.sel_x_gse.y,py_sel_x_gse.y,atol=1.0e-06)
        py_sel_x_sse = get_data('sel_x_sse')
        assert_allclose(self.sel_x_sse.y,py_sel_x_sse.y,atol=1.0e-06)
        py_sel_y_sse = get_data('sel_y_sse')
        assert_allclose(self.sel_y_sse.y,py_sel_y_sse.y,atol=1.0e-06)
        py_sel_z_sse = get_data('sel_z_sse')
        assert_allclose(self.sel_z_sse.y,py_sel_z_sse.y,atol=1.0e-06)
        py_sel_mat_cotrans = get_data('sel_mat_cotrans')
        assert_allclose(py_sel_mat_cotrans.y, self.sel_mat_cotrans.y, atol=1.0e-06)
        pos_sel = get_data('tha_state_pos_sel')
        pos_meta = get_data('tha_state_pos_sel',metadata=True)
        self.assertEqual(pos_meta['data_att']['units'],'km')
        assert_allclose(pos_sel.y, self.tha_state_pos_sel.y, atol=0.1)
        self.assertEqual(get_coords('tha_state_pos_sel').lower(),'sel')

    def test_sse2sel_fgs(self):
        """ Validate sse2sel field transform """
        result = sse2sel('tha_fgs_sse', 'tha_fgs_sel')
        self.assertEqual(result,1)
        fgs_sel = get_data('tha_fgs_sel')
        assert_allclose(fgs_sel.y, self.tha_fgs_sel.y, atol=.005)
        self.assertEqual(get_coords('tha_fgs_sel').lower(),'sel')

    def test_sel2sse_pos(self):
        """ Validate sel2sse position transform """
        # Restore original baseline input tplot variable
        store_data('tha_state_pos_sel',data={'x':self.tha_state_pos_sel.times, 'y':self.tha_state_pos_sel.y})
        set_coords('tha_state_pos_sel','sel')

        result = sse2sel('tha_state_pos_sel', 'tha_state_pos_sel_sse', isseltosse=True)
        self.assertEqual(result,1)
        pos_sse = get_data('tha_state_pos_gse_sel_sse')
        assert_allclose(pos_sse.y, self.tha_state_pos_gse_sel_sse.y, atol=0.1)
        self.assertEqual(get_coords('tha_state_pos_gse_sel_sse').lower(),'sse')

    def test_sel2sse_field(self):
        """ Validate sel2sse field transform """
        # Restore original baseline input tplot variable
        store_data('tha_fgs_sel',data={'x':self.tha_fgs_sel.times, 'y':self.tha_fgs_sel.y})
        set_coords('tha_fgs_sel','sel')
        md_before = get_data('tha_fgs_sel',metadata=True)
        md_before['data_att']['units'] = 'nT'
        result = sse2sel('tha_fgs_sel', 'tha_fgs_sel_sse', isseltosse=True)
        self.assertEqual(result,1)
        fgs_sse = get_data('tha_fgs_sel_sse')
        fgs_meta = get_data('tha_fgs_sel_sse',metadata=True)
        self.assertEqual(fgs_meta['data_att']['units'],'nT')
        assert_allclose(fgs_sse.y, self.tha_fgs_sse.y, atol=0.1)
        self.assertEqual(get_coords('tha_fgs_sel_sse').lower(),'sse')

if __name__ == '__main__':
    unittest.main()
