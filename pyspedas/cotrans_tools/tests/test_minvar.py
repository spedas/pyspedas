"""
Unit Tests for minvar function.
"""
import pyspedas
from pyspedas.cotrans_tools.minvar import minvar
from pyspedas.cotrans_tools.minvar_matrix_make import minvar_matrix_make
from pytplot import data_exists, tplot_names, tplot, get_data, tplot_copy, del_data, store_data
import numpy as np
import unittest
from pyspedas import tplot_restore
from numpy.testing import assert_allclose
from pyspedas import tvector_rotate
from pyspedas import download



class TestMinvar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #  Test tolerance
        cls.tol = 1e-10

        # Define a random data array
        rng = np.random.default_rng(seed=31415)
        cls.rdata = rng.random((10, 3))

        # Download tplot files
        remote_server = 'https://github.com/spedas/test_data/raw/refs/heads/main/'
        remote_name = 'cotrans_tools/mva_python_validate.tplot'
        datafile = download(remote_file=remote_name,
                            remote_path=remote_server,
                            local_path='testdata',
                            no_download=False)
        if not datafile:
            # Skip tests
            raise unittest.SkipTest("Cannot download data validation file")

        # Load validation variables from the test file
        del_data('*')
        filename = datafile[0]
        tplot_restore(filename)

        cls.fgm = get_data('thb_fgs_gsm_mvaclipped1')
        cls.mat = get_data('thb_fgs_gsm_mvaclipped1_mva_mat')
        cls.vals = get_data('mva_vals')
        cls.min = get_data('mva_min')
        cls.int = get_data('mva_int')
        cls.max = get_data('mva_max')
        cls.rot = get_data('thb_fgs_gsm_mvaclipped1_rot')
        tplot_copy('thb_fgs_gsm_mvaclipped1','idl_thb_fgs_gsm_mvaclipped1')
        tplot_copy('thb_fgs_gsm_mvaclipped1_mva_mat','idl_thb_fgs_gsm_mvaclipped1_mva_mat')
        tplot_copy('mva_min','idl_mva_min')
        tplot_copy('mva_int','idl_mva_int')
        tplot_copy('mva_max','idl_mva_max')
        tplot_copy('mva_vals','idl_mva_vals')
        tplot_copy('thb_fgs_gsm_mvaclipped1_rot','idl_thb_fgs_gsm_mvaclipped1_rot')

        cls.fgm2 = get_data('mms1_fgm_b_gsm_srvy_l2_bvec_hp4minvar')
        cls.mat2 = get_data('mms1_fgm_b_gsm_srvy_l2_bvec_hp4minvar_mva_mat')
        cls.inp2 = get_data('mms1_fgm_b_gsm_srvy_l2_bvec_bp')
        cls.vals2 = get_data('mva_vals2')
        cls.min2 = get_data('mva_min2')
        cls.int2 = get_data('mva_int2')
        cls.max2 = get_data('mva_max2')
        cls.rot2 = get_data('mms1_fgm_b_gsm_srvy_l2_bvec_bp_rot')
        tplot_copy('mms1_fgm_b_gsm_srvy_l2_bvec_hp4minvar','idl_mms1_fgm_b_gsm_srvy_l2_bvec_hp4minvar')
        tplot_copy('mms1_fgm_b_gsm_srvy_l2_bvec_hp4minvar_mva_mat','idl_mms1_fgm_b_gsm_srvy_l2_bvec_hp4minvar_mva_mat')
        tplot_copy('mva_min2','idl_mva_min2')
        tplot_copy('mva_int2','idl_mva_int2')
        tplot_copy('mva_max2','idl_mva_max2')
        tplot_copy('mva_vals2','idl_mva_vals2')
        tplot_copy('mms1_fgm_b_gsm_srvy_l2_bvec_bp','idl_mms1_fgm_b_gsm_srvy_l2_bvec_bp')
        tplot_copy('mms1_fgm_b_gsm_srvy_l2_bvec_bp_rot','idl_mms1_fgm_b_gsm_srvy_l2_bvec_bp_rot')

        del_data('thb_*')
        del_data('mms1_*')
        del_data('mva*')



    def test_minvar_basic(self):
        """Test of basic input and output"""

        # Synthetic data of zeros
        data = np.zeros([2, 3])
        vrot, v, w = minvar(data)
        self.assertTrue(np.sum(vrot - data) < self.tol)
        self.assertTrue(np.sum(v - np.diag(np.ones(3))) < self.tol)
        self.assertTrue(np.sum(w - np.zeros(3)) < self.tol)

    def test_minvar_rotation(self):
        """Test of the rotation matrix"""
        vrot, v, w = minvar(self.rdata)
        # Determinant of rotation matrix should be = 1
        self.assertTrue((np.linalg.det(v) - 1) < self.tol)

    def test_minvar_total(self):
        """Test of same square root of total of squares """
        vrot, v, w = minvar(self.rdata)
        total1 = (self.rdata**2).sum(axis=1)
        total2 = (vrot ** 2).sum(axis=1)
        # Compare totals
        self.assertTrue(np.sum(total1 - total2) < self.tol)

    def test_minrar_code_coverage(self):
        """Test to cover the code from IDL"""
        data = np.array([[0, 0, 1], [0, 0, 1]])
        vrot, v, w = minvar(data)
        # Case of np.sum(w) == 0.0
        self.assertTrue(w.sum() < self.tol)

        # This should be not Right Handed (?...)
        data = np.array([[0, -1, 1], [-1, -1, 1]])
        # case if YcrossZdotX < 0
        vrot, v, w = minvar(data)
        YcrossZdotX = v[0, 0] * (v[1, 1] * v[2, 2] - v[2, 1] * v[1, 2])
        # YcrossZdotX Should be positive after that
        self.assertTrue(YcrossZdotX > 0)

        # should tigger case if v[2, 2] < 0: (?...)
        data = np.array([[-0.1, -0.9, 0.5], [-1, 1, -0.9]])
        vrot, v, w = minvar(data)
        # v[2,2] Should be positive after that
        self.assertTrue(v[2, 2] > 0)

    def test_minvar_matrix_make_day(self):
        trange=['2007-07-10', '2007-07-11']
        pyspedas.projects.themis.fgm(probe='c', trange=trange, level='l2', coord='gse')
        minvar_matrix_make('thc_fgs_gse',tstart='2007-07-10/07:54:00',tstop='2007-07-10/07:56:30')
        self.assertTrue(data_exists('thc_fgs_gse_mva_mat'))
        pyspedas.tvector_rotate('thc_fgs_gse_mva_mat','thc_fgs_gse',newname='mva_data_day')
        self.assertTrue((data_exists('mva_data_day')))

    def test_minvar_matrix_extra_outputs(self):
        trange=['2007-07-10', '2007-07-11']
        pyspedas.projects.themis.fgm(probe='c', trange=trange, level='l2', coord='gse')
        minvar_matrix_make('thc_fgs_gse',tstart='2007-07-10/07:54:00',tstop='2007-07-10/07:56:30',
                           evname='mva_lambdas',tminname='mva_min',tmidname='mva_mid',tmaxname='mva_max')
        self.assertTrue(data_exists('thc_fgs_gse_mva_mat'))
        pyspedas.tvector_rotate('thc_fgs_gse_mva_mat','thc_fgs_gse',newname='mva_data_day')
        self.assertTrue((data_exists('mva_data_day')))
        self.assertTrue(data_exists('mva_lambdas'))
        self.assertTrue(data_exists('mva_min'))
        self.assertTrue(data_exists('mva_min'))
        self.assertTrue(data_exists('mva_max'))

    def test_minvar_matrix_make_hour(self):
        trange=['2007-07-10', '2007-07-11']
        pyspedas.projects.themis.fgm(probe='c', trange=trange, level='l2', coord='gse')
        minvar_matrix_make('thc_fgs_gse', twindow=3600, tslide=300)
        self.assertTrue(data_exists('thc_fgs_gse_mva_mat'))
        pyspedas.tvector_rotate('thc_fgs_gse_mva_mat','thc_fgs_gse',newname='mva_data_hour')
        self.assertTrue((data_exists('mva_data_hour')))

    def test_minvar_matrix_make_hour_interp(self):
        trange=['2007-07-10', '2007-07-11']
        pyspedas.projects.themis.fgm(probe='c', trange=trange, level='l2', coord='gse')
        minvar_matrix_make('thc_fgs_gse', twindow=3600, tslide=300)
        self.assertTrue(data_exists('thc_fgs_gse_mva_mat'))
        pyspedas.tvector_rotate('thc_fgs_gse_mva_mat','thc_fgl_gse',newname='mva_data_hour_interp')
        self.assertTrue((data_exists('mva_data_hour_interp')))

    def test_minvar_matrix_make_idl_single(self):
        """ Test a minvar_matrix_make call with only a single window """
        minvar_matrix_make('idl_thb_fgs_gsm_mvaclipped1',newname='thb_fgs_gsm_mvaclipped1_mva_mat',
                           evname='mva_vals', tminname='mva_min', tmidname='mva_int', tmaxname='mva_max')

        tvector_rotate('thb_fgs_gsm_mvaclipped1_mva_mat', 'idl_thb_fgs_gsm_mvaclipped1',newname='thb_fgs_gsm_mvaclipped1_rot')
        vals = get_data('mva_vals')
        assert_allclose(vals.y, self.vals.y, rtol=1e-05, atol=1e-03)
        assert_allclose(vals.times, self.vals.times,  atol=1e-06)
        mva_mat = get_data('thb_fgs_gsm_mvaclipped1_mva_mat')
        assert_allclose(mva_mat.y, self.mat.y, rtol=1e-05, atol=1e-03)
        mva_min = get_data('mva_min')
        assert_allclose(mva_min.y, self.min.y, rtol=1e-05, atol=1e-03)
        mva_int = get_data('mva_int')
        assert_allclose(mva_int.y, self.int.y, rtol=1e-05, atol=1e-03)
        mva_max = get_data('mva_max')
        assert_allclose(mva_max.y, self.max.y, rtol=1e-05, atol=1e-03)
        mva_rot = get_data('thb_fgs_gsm_mvaclipped1_rot')
        assert_allclose(mva_rot.y, self.rot.y, rtol=1e-05, atol=1e-03)

    def test_minvar_matrix_make_idl_multi(self):
        """ Test a minvar_matrix_make call that returns multiple matrices """
        minvar_matrix_make('idl_mms1_fgm_b_gsm_srvy_l2_bvec_hp4minvar',newname='mms1_fgm_b_gsm_srvy_l2_bvec_hp4minvar_mva_mat',
                           twindow=16.0, tslide=4.0, evname='mva_vals2', tminname='mva_min2', tmidname='mva_int2', tmaxname='mva_max2')
        tvector_rotate('mms1_fgm_b_gsm_srvy_l2_bvec_hp4minvar_mva_mat', 'idl_mms1_fgm_b_gsm_srvy_l2_bvec_bp',newname='mms1_fgm_b_gsm_srvy_l2_bvec_bp_rot')
        vals = get_data('mva_vals2')
        assert_allclose(vals.times, self.vals2.times, atol=1e-06)
        assert_allclose(vals.y, self.vals2.y, rtol=1e-05, atol=1e-06)
        mva_mat = get_data('mms1_fgm_b_gsm_srvy_l2_bvec_hp4minvar_mva_mat')
        assert_allclose(mva_mat.y, self.mat2.y, rtol=1e-03, atol=1e-05)
        mva_min = get_data('mva_min2')
        assert_allclose(mva_min.y, self.min2.y, rtol=1e-03, atol=1e-06)
        mva_int = get_data('mva_int2')
        assert_allclose(mva_int.y, self.int2.y, rtol=1e-03, atol=1e-06)
        mva_max = get_data('mva_max2')
        assert_allclose(mva_max.y, self.max2.y, rtol=1e-03, atol=1e-06)
        mva_rot = get_data('mms1_fgm_b_gsm_srvy_l2_bvec_bp_rot')
        assert_allclose(mva_rot.y, self.rot2.y, rtol=1e-05, atol=1e-06)


if __name__ == '__main__':
    unittest.main()

