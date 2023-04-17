"""Tests of gse2sse and sse2sel functions."""
import pytplot.get_data
from pytplot.importers.cdf_to_tplot import cdf_to_tplot
import unittest
import pytplot
from numpy.testing import assert_array_almost_equal_nulp, assert_array_max_ulp, assert_allclose

from pyspedas.utilities.data_exists import data_exists
from pyspedas.themis.cotrans.gse2sse import gse2sse
from pyspedas.themis.cotrans.sse2sel import sse2sel
from pyspedas.themis.state.autoload_support import autoload_support
from pyspedas.cotrans.cotrans_get_coord import cotrans_get_coord
from pyspedas.cotrans.cotrans_set_coord import cotrans_set_coord


class LunCotransDataValidation(unittest.TestCase):
    """ Compares cotrans results between Python and IDL """

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The SPEDAS script that creates the file: projects/themis/state/cotrans/thm_cotrans_validate.pro
        """
        from pyspedas.utilities.download import download
        from pyspedas.themis.config import CONFIG

        # Testing time range
        cls.t = ['2008-03-23', '2008-03-28']

        # Testing tolerance
        cls.tol = 1e-10

        # Download tplot files
        remote_server = 'https://spedas.org/'
        remote_name = 'testfiles/thm_cotrans_validate.cdf'
        # remote_name = 'testfiles/thm_cotrans_validate.tplot'
        datafile = download(remote_file=remote_name,
                            remote_path=remote_server,
                            local_path=CONFIG['local_data_dir'],
                            no_download=False)
        if not datafile:
            # Skip tests
            raise unittest.SkipTest("Cannot download data validation file")

        # Load validation variables from the test file
        pytplot.del_data('*')
        filename = datafile[0]
        pytplot.cdf_to_tplot(filename)
        # pytplot.tplot_restore(filename)
        # pytplot.tplot_names()
        # Input variables
        cotrans_set_coord('tha_state_pos_gse','gse')
        cotrans_set_coord('tha_state_vel_gse','gse')
        cls.tha_state_pos_gse = pytplot.get_data('tha_state_pos_gse')
        cls.tha_state_vel_gse = pytplot.get_data('tha_state_vel_gse')
        cotrans_set_coord('tha_fgs_gse','gse')
        cls.tha_fgs_gse = pytplot.get_data('tha_fgs_gse')
        # GSE<->SSE results
        cotrans_set_coord('tha_state_pos_sse','sse')
        cotrans_set_coord('tha_state_vel_sse','sse')
        cls.tha_state_pos_sse = pytplot.get_data('tha_state_pos_sse')
        cls.tha_state_vel_sse = pytplot.get_data('tha_state_vel_sse')
        cotrans_set_coord('tha_state_pos_sse_rotate_only','sse')
        cotrans_set_coord('tha_state_vel_sse_rotate_only','sse')
        cls.tha_state_pos_sse_rotate_only = pytplot.get_data('tha_state_pos_sse_rotate_only')
        cls.tha_state_vel_sse_rotate_only = pytplot.get_data('tha_state_vel_sse_rotate_only')
        cotrans_set_coord('tha_fgs_sse','sse')
        cls.tha_fgs_sse = pytplot.get_data('tha_fgs_sse')

        cotrans_set_coord('tha_state_pos_gse_sse_gse','gse')
        cotrans_set_coord('tha_state_vel_gse_sse_gse','gse')
        cls.tha_state_pos_gse_sse_gse = pytplot.get_data('tha_state_pos_gse_sse_gse')
        cls.tha_state_vel_gse_sse_gse = pytplot.get_data('tha_state_vel_gse_sse_gse')

        cotrans_set_coord('tha_state_pos_gse_sse_gse_rotate_only','gse')
        cotrans_set_coord('tha_state_vel_gse_sse_gse_rotate_only','gse')
        cls.tha_state_pos_gse_sse_gse_rotate_only = pytplot.get_data('tha_state_pos_gse_sse_gse_rotate_only')
        cls.tha_state_vel_gse_sse_gse_rotate_only = pytplot.get_data('tha_state_vel_gse_sse_gse_rotate_only')

        cotrans_set_coord('tha_fgs_gse_sse_gse','gse')
        cls.tha_fgs_gse_sse_gse = pytplot.get_data('tha_fgs_gse_sse_gse')

        # SSE<->SSL results
        cotrans_set_coord('tha_state_pos_sel','sel')
        cotrans_set_coord('tha_state_vel_sel','sel')
        cls.tha_state_pos_sel = pytplot.get_data('tha_state_pos_sel')
        cls.tha_state_vel_sel = pytplot.get_data('tha_state_vel_sel')

        cotrans_set_coord('tha_state_pos_gse_sel_sse','sse')
        cotrans_set_coord('tha_state_vel_gse_sel_sse','sse')
        cls.tha_state_pos_gse_sel_sse = pytplot.get_data('tha_state_pos_gse_sel_sse')
        cls.tha_state_vel_gse_sel_sse = pytplot.get_data('tha_state_vel_gse_sel_sse')

        cls.sse_mat_cotrans = pytplot.get_data('sse_mat_cotrans')
        cls.sel_mat_cotrans = pytplot.get_data('sel_mat_cotrans')
        cls.sel_x_gei = pytplot.get_data('sel_x_gei')
        cls.sel_x_gse = pytplot.get_data('sel_x_gse')
        cls.sel_x_sse = pytplot.get_data('sel_x_sse')
        cls.sel_y_sse = pytplot.get_data('sel_y_sse')
        cls.sel_z_sse = pytplot.get_data('sel_z_sse')

        autoload_support(varname='tha_state_pos_gse', slp=True)

    def setUp(self):
        """ We need to clean tplot variables before each run"""
        # pytplot.del_data('*')


    def test_gse2sse_pos(self):
        """ Validate gse2sse position transform """
        result = gse2sse('tha_state_pos_gse', 'slp_sun_pos', 'slp_lun_pos', 'tha_state_pos_sse', variable_type='pos')
        self.assertEqual(result,1)
        py_sse_mat_cotrans = pytplot.get_data('sse_mat_cotrans')
        assert_allclose(py_sse_mat_cotrans.y, self.sse_mat_cotrans.y, atol=1.0e-06)
        pos_sse = pytplot.get_data('tha_state_pos_sse')
        assert_allclose(pos_sse.y, self.tha_state_pos_sse.y, atol=0.1)
        self.assertEqual(cotrans_get_coord('tha_state_pos_sse').lower(),'sse')

    def test_sse2sel_pos(self):
        """ Validate sse2sel position transform """
        result = sse2sel('tha_state_pos_sse', 'slp_sun_pos', 'slp_lun_pos', 'slp_lun_att_x', 'slp_lun_att_z', 'tha_state_pos_sel', variable_type='pos')
        self.assertEqual(result,1)
        py_sel_x_gse = pytplot.get_data('slp_lun_att_x_gse')
        assert_allclose(self.sel_x_gse.y,py_sel_x_gse.y,atol=1.0e-06)
        py_sel_x_sse = pytplot.get_data('sel_x_sse')
        assert_allclose(self.sel_x_sse.y,py_sel_x_sse.y,atol=1.0e-06)
        py_sel_y_sse = pytplot.get_data('sel_y_sse')
        assert_allclose(self.sel_y_sse.y,py_sel_y_sse.y,atol=1.0e-06)
        py_sel_z_sse = pytplot.get_data('sel_z_sse')
        assert_allclose(self.sel_z_sse.y,py_sel_z_sse.y,atol=1.0e-06)
        py_sel_mat_cotrans = pytplot.get_data('sel_mat_cotrans')
        assert_allclose(py_sel_mat_cotrans.y, self.sel_mat_cotrans.y, atol=1.0e-06)
        pos_sse = pytplot.get_data('tha_state_pos_sel')
        assert_allclose(pos_sse.y, self.tha_state_pos_sel.y, atol=0.1)
        self.assertEqual(cotrans_get_coord('tha_state_pos_sel').lower(),'sel')

    def test_gse2sse_pos_rotate_only(self):
        """ Validate gse2sse position transform """
        result = gse2sse('tha_state_pos_gse', 'slp_sun_pos', 'slp_lun_pos', 'tha_state_pos_sse_rotate_only', variable_type='pos',rotation_only=True)
        self.assertEqual(result,1)
        pos_sse = pytplot.get_data('tha_state_pos_sse_rotate_only')
        assert_allclose(pos_sse.y, self.tha_state_pos_sse_rotate_only.y, atol=0.1)
        self.assertEqual(cotrans_get_coord('tha_state_pos_sse_rotate_only').lower(),'sse')

    def test_gse2sse_vel(self):
        """ Validate gse2sse velocity transform """
        result = gse2sse('tha_state_vel_gse', 'slp_sun_pos', 'slp_lun_pos', 'tha_state_vel_sse',variable_type='vel')
        self.assertEqual(result,1)
        vel_sse = pytplot.get_data('tha_state_vel_sse')
        assert_allclose(vel_sse.y, self.tha_state_vel_sse.y, atol=1.0e-03)
        self.assertEqual(cotrans_get_coord('tha_state_vel_sse').lower(),'sse')

    def test_gse2sse_vel_rotate_only(self):
        """ Validate gse2sse position transform """
        result = gse2sse('tha_state_vel_gse', 'slp_sun_pos', 'slp_lun_pos', 'tha_state_vel_sse_rotate_only', variable_type='vel',rotation_only=True)
        self.assertEqual(result,1)
        pos_sse = pytplot.get_data('tha_state_vel_sse_rotate_only')
        assert_allclose(pos_sse.y, self.tha_state_vel_sse_rotate_only.y, atol=1.0e-03)
        self.assertEqual(cotrans_get_coord('tha_state_vel_sse_rotate_only').lower(),'sse')

    def test_gse2sse_field(self):
        """ Validate gse2sse field transform """
        result = gse2sse('tha_fgs_gse', 'slp_sun_pos', 'slp_lun_pos', 'tha_fgs_sse')
        self.assertEqual(result, 1)
        fgs_sse = pytplot.get_data('tha_fgs_sse')
        assert_allclose(fgs_sse.y, self.tha_fgs_sse.y, atol=1.0e-02)
        self.assertEqual(cotrans_get_coord('tha_fgs_sse').lower(), 'sse')

    def test_sse2gse_pos(self):
        """ Validate sse2gse position transform """
        pytplot.store_data('tha_state_pos_sse',data={'x':self.tha_state_pos_sse.times, 'y':self.tha_state_pos_sse.y})
        cotrans_set_coord('tha_state_pos_sse','sse')
        result = gse2sse('tha_state_pos_sse', 'slp_sun_pos', 'slp_lun_pos', 'tha_state_pos_gse_sse_gse',isssetogse=True,
                         variable_type='pos')
        self.assertEqual(result,1)
        pos_gse = pytplot.get_data('tha_state_pos_gse_sse_gse')
        assert_allclose(pos_gse.y, self.tha_state_pos_gse_sse_gse.y, atol=0.1)
        self.assertEqual(cotrans_get_coord('tha_state_pos_gse_sse_gse').lower(),'gse')

    def test_sse2gse_pos_rotate_only(self):
        """ Validate sse2gse position transform """
        pytplot.store_data('tha_state_pos_sse_rotate_only',
                           data={'x':self.tha_state_pos_sse_rotate_only.times, 'y':self.tha_state_pos_sse_rotate_only.y})
        cotrans_set_coord('tha_state_pos_sse_rotate_only','sse')
        result = gse2sse('tha_state_pos_sse_rotate_only', 'slp_sun_pos', 'slp_lun_pos', 'tha_state_pos_gse_sse_gse_rotation_only',isssetogse=True,
                         variable_type='pos', rotation_only=True)
        self.assertEqual(result,1)
        pos_gse = pytplot.get_data('tha_state_pos_gse_sse_gse_rotation_only')
        assert_allclose(pos_gse.y, self.tha_state_pos_gse_sse_gse_rotate_only.y, atol=0.1)
        self.assertEqual(cotrans_get_coord('tha_state_pos_gse_sse_gse_rotate_only').lower(),'gse')

    def test_sse2gse_vel(self):
        """ Validate sse2gse velocity transform """
        result = gse2sse('tha_state_vel_sse', 'slp_sun_pos', 'slp_lun_pos', 'tha_state_vel_gse_sse_gse',isssetogse=True,
                         variable_type='vel')
        self.assertEqual(result,1)
        vel_gse = pytplot.get_data('tha_state_vel_gse_sse_gse')
        assert_allclose(vel_gse.y, self.tha_state_vel_gse_sse_gse.y, atol=1.0e-02)
        self.assertEqual(cotrans_get_coord('tha_state_vel_gse_sse_gse').lower(),'gse')

    def test_sse2gse_vel_rotate_only(self):
        """ Validate sse2gse position transform """
        pytplot.store_data('tha_state_vel_sse_rotate_only',
                           data={'x':self.tha_state_vel_sse_rotate_only.times, 'y':self.tha_state_vel_sse_rotate_only.y})
        cotrans_set_coord('tha_state_vel_sse_rotate_only','sse')
        result = gse2sse('tha_state_vel_sse_rotate_only', 'slp_sun_pos', 'slp_lun_pos', 'tha_state_vel_gse_sse_gse_rotation_only',isssetogse=True,
                         variable_type='pos', rotation_only=True)
        self.assertEqual(result,1)
        vel_gse = pytplot.get_data('tha_state_vel_gse_sse_gse_rotation_only')
        assert_allclose(vel_gse.y, self.tha_state_vel_gse_sse_gse_rotate_only.y, atol=1.0e-03)
        self.assertEqual(cotrans_get_coord('tha_state_vel_gse_sse_gse_rotate_only').lower(),'gse')

    def test_sse2gse_field(self):
        """ Validate gse2sse field transform """
        result = gse2sse('tha_fgs_sse', 'slp_sun_pos', 'slp_lun_pos', 'tha_fgs_gse_sse_gse',isssetogse=True)
        self.assertEqual(result, 1)
        fgs_gse = pytplot.get_data('tha_fgs_gse_sse_gse')
        assert_allclose(fgs_gse.y, self.tha_fgs_gse_sse_gse.y, atol=1.0e-02)
        self.assertEqual(cotrans_get_coord('tha_fgs_gse_sse_gse').lower(), 'gse')

if __name__ == '__main__':
    unittest.main()
