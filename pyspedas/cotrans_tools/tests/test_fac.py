"""
Unit Tests for minvar function.
"""
import pyspedas

from pyspedas import fac_matrix_make
from pytplot import data_exists, tplot_names, tplot, get_data, tplot_copy, del_data, store_data
import numpy as np
import unittest
from pyspedas import tplot_restore
from numpy.testing import assert_allclose
from pyspedas import tvector_rotate
from pyspedas import download



class TestFac(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #  Test tolerance
        cls.tol = 1e-10

        # Define a random data array
        rng = np.random.default_rng(seed=31415)
        cls.rdata = rng.random((10, 3))


        # Download tplot files
        # Comparison data was generated using both thm_fac_matrix_make and fac_matrix_make, using the script
        # general/cotrans/special/fac/fac_matrix_make_python_validate
        remote_server = 'https://github.com/spedas/test_data/raw/refs/heads/main/'
        remote_name = 'cotrans_tools/fac_python_validate.tplot'
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

        cls.fgm = get_data('thc_fgs_gse')
        tplot_copy('thc_fgs_gse', 'idl_thc_fgs_gse')
        cls.fgm_sm = get_data('thc_fgs_gse_sm601')
        tplot_copy('thc_fgs_gse_sm601', 'idl_thc_fgs_gse_sm601')
        cls.pos = get_data('thc_state_pos')
        tplot_copy('thc_state_pos', 'idl_thc_state_pos')

        cls.mat_xgse = get_data('thc_fgs_gse_sm601_fac_mat_xgse')
        tplot_copy('thc_fgs_gse_sm601_fac_mat_xgse', 'idl_thc_fgs_gse_sm601_fac_mat_xgse')
        cls.mat_rgeo = get_data('thc_fgs_gse_sm601_fac_mat_rgeo')
        tplot_copy('thc_fgs_gse_sm601_fac_mat_rgeo', 'idl_thc_fgs_gse_sm601_fac_mat_rgeo')
        cls.mat_phigeo = get_data('thc_fgs_gse_sm601_fac_mat_phigeo')
        tplot_copy('thc_fgs_gse_sm601_fac_mat_phigeo', 'idl_thc_fgs_gse_sm601_fac_mat_phigeo')
        cls.mat_mphigeo = get_data('thc_fgs_gse_sm601_fac_mat_mphigeo')
        tplot_copy('thc_fgs_gse_sm601_fac_mat_phism', 'idl_thc_fgs_gse_sm601_fac_mat_phism')
        cls.mat_phism = get_data('thc_fgs_gse_sm601_fac_mat_phism')
        tplot_copy('thc_fgs_gse_sm601_fac_mat_phism', 'idl_thc_fgs_gse_sm601_fac_mat_phism')
        cls.mat_mphism = get_data('thc_fgs_gse_sm601_fac_mat_mphism')
        tplot_copy('thc_fgs_gse_sm601_fac_mat_phism', 'idl_thc_fgs_gse_sm601_fac_mat_phism')
        cls.mat_ygsm = get_data('thc_fgs_gse_sm601_fac_mat_ygsm')
        tplot_copy('thc_fgs_gse_sm601_fac_mat_ygsm', 'idl_thc_fgs_gse_sm601_fac_mat_ygsm')

        cls.mat_xgse_thm = get_data('thc_fgs_gse_sm601_fac_mat_xgse_thm')
        tplot_copy('thc_fgs_gse_sm601_fac_mat_xgse_thm', 'idl_thc_fgs_gse_sm601_fac_mat_xgse_thm')
        cls.mat_rgeo_thm = get_data('thc_fgs_gse_sm601_fac_mat_rgeo_thm')
        tplot_copy('thc_fgs_gse_sm601_fac_mat_rgeo_thm', 'idl_thc_fgs_gse_sm601_fac_mat_rgeo_thm')
        cls.mat_phigeo_thm = get_data('thc_fgs_gse_sm601_fac_mat_phigeo_thm')
        tplot_copy('thc_fgs_gse_sm601_fac_mat_phigeo_thm', 'idl_thc_fgs_gse_sm601_fac_mat_phigeo_thm')
        cls.mat_mphigeo_thm = get_data('thc_fgs_gse_sm601_fac_mat_mphigeo_thm')
        tplot_copy('thc_fgs_gse_sm601_fac_mat_mphigeo_thm', 'idl_thc_fgs_gse_sm601_fac_mat_mphigeo_thm')
        cls.mat_phism_thm = get_data('thc_fgs_gse_sm601_fac_mat_phism_thm')
        tplot_copy('thc_fgs_gse_sm601_fac_mat_phism_thm', 'idl_thc_fgs_gse_sm601_fac_mat_phism_thm')
        cls.mat_mphism_thm = get_data('thc_fgs_gse_sm601_fac_mat_mphism_thm')
        tplot_copy('thc_fgs_gse_sm601_fac_mat_mphism_thm', 'idl_thc_fgs_gse_sm601_fac_mat_mphism_thm')
        cls.mat_ygsm_thm = get_data('thc_fgs_gse_sm601_fac_mat_ygsm_thm')
        tplot_copy('thc_fgs_gse_sm601_fac_mat_ygsm_thm', 'idl_thc_fgs_gse_sm601_fac_mat_ygsm_thm')

        cls.vec_xgse = get_data('thc_fgs_fac_xgse')
        tplot_copy('thc_fgs_fac_xgse', 'idl_thc_fgs_fac_xgse')
        cls.vec_rgeo = get_data('thc_fgs_fac_rgeo')
        tplot_copy('thc_fgs_fac_rgeo', 'idl_thc_fgs_fac_rgeo')
        cls.vec_phigeo = get_data('thc_fgs_fac_phigeo')
        tplot_copy('thc_fgs_fac_phigeo', 'idl_thc_fgs_fac_phigeo')
        cls.vec_mphigeo = get_data('thc_fgs_fac_mphigeo')
        tplot_copy('thc_fgs_fac_mphigeo', 'idl_thc_fgs_fac_mphigeo')
        cls.vec_phism = get_data('thc_fgs_fac_phism')
        tplot_copy('thc_fgs_fac_phism', 'idl_thc_fgs_fac_phism')
        cls.vec_mphism = get_data('thc_fgs_fac_mphism')
        tplot_copy('thc_fgs_fac_mphism', 'idl_thc_fgs_fac_mphism')
        cls.vec_ygsm = get_data('thc_fgs_fac_ygsm')
        tplot_copy('thc_fgs_fac_ygsm', 'idl_thc_fgs_fac_ygsm')

        cls.vec_xgse_thm = get_data('thc_fgs_fac_xgse_thm')
        tplot_copy('thc_fgs_fac_xgse_thm', 'idl_thc_fgs_fac_xgse_thm')
        cls.vec_rgeo_thm = get_data('thc_fgs_fac_rgeo_thm')
        tplot_copy('thc_fgs_fac_rgeo_thm', 'idl_thc_fgs_fac_rgeo_thm')
        cls.vec_phigeo_thm = get_data('thc_fgs_fac_phigeo_thm')
        tplot_copy('thc_fgs_fac_phigeo_thm', 'idl_thc_fgs_fac_phigeo_thm')
        cls.vec_mphigeo_thm = get_data('thc_fgs_fac_mphigeo_thm')
        tplot_copy('thc_fgs_fac_mphigeo_thm', 'idl_thc_fgs_fac_mphigeo_thm')
        cls.vec_phism_thm = get_data('thc_fgs_fac_phism')
        tplot_copy('thc_fgs_fac_phism_thm', 'idl_thc_fgs_fac_phism_thm')
        cls.vec_mphism_thm = get_data('thc_fgs_fac_mphism')
        tplot_copy('thc_fgs_fac_mphism_thm', 'idl_thc_fgs_fac_mphism_thm')
        cls.vec_ygsm_thm = get_data('thc_fgs_fac_ygsm_thm')
        tplot_copy('thc_fgs_fac_ygsm_thm', 'idl_thc_fgs_fac_ygsm_thm')

        del_data('thc_*')



    def test_fac_xgse(self):
        """Test of other_dim = xgse"""

        fac_matrix_make('idl_thc_fgs_gse_sm601',other_dim='xgse',newname='mat_xgse')
        tvector_rotate('mat_xgse', 'idl_thc_fgs_gse', newname='vec_xgse')
        dat1 = get_data('mat_xgse')
        dat2 = get_data('vec_xgse')
        store_data('vecdiff',data={'x':dat2.times, 'y':self.vec_xgse.y - dat2.y})
        assert_allclose(dat1.y, self.mat_xgse.y, atol=1.0e-06)
        assert_allclose(dat2.y, self.vec_xgse.y, atol=1.0e-06)
        store_data('vecdiff',data={'x':dat2.times, 'y':self.vec_xgse.y - dat2.y})
        #tplot('vec_xgse idl_thc_fgs_fac_xgse vecdiff')

    def test_fac_xgse_thm(self):
        """Test of other_dim = xgse"""

        fac_matrix_make('idl_thc_fgs_gse_sm601',other_dim='xgse',newname='mat_xgse')
        tvector_rotate('mat_xgse', 'idl_thc_fgs_gse', newname='vec_xgse')
        dat1 = get_data('mat_xgse')
        dat2 = get_data('vec_xgse')
        store_data('vecdiff',data={'x':dat2.times, 'y':self.vec_xgse_thm.y - dat2.y})
        assert_allclose(dat1.y, self.mat_xgse_thm.y, atol=1.0e-06)
        assert_allclose(dat2.y, self.vec_xgse_thm.y, atol=1.0e-06)
        store_data('vecdiff',data={'x':dat2.times, 'y':self.vec_xgse_thm.y - dat2.y})
        #tplot('vec_xgse idl_thc_fgs_fac_xgse vecdiff')

    def test_fac_rgeo(self):
        """Test of other_dim = xgse"""

        fac_matrix_make('idl_thc_fgs_gse_sm601',other_dim='rgeo',pos_var_name='idl_thc_state_pos', newname='mat_rgeo')
        tvector_rotate('mat_rgeo', 'idl_thc_fgs_gse', newname='vec_rgeo')
        dat1 = get_data('mat_rgeo')
        dat2 = get_data('vec_rgeo')
        assert_allclose(dat1.y, self.mat_rgeo.y, atol=.002)
        assert_allclose(dat2.y, self.vec_rgeo.y, atol=.002)

    def test_fac_rgeo_thm(self):
        """Test of other_dim = xgse"""

        fac_matrix_make('idl_thc_fgs_gse_sm601',other_dim='rgeo',pos_var_name='idl_thc_state_pos', newname='mat_rgeo')
        tvector_rotate('mat_rgeo', 'idl_thc_fgs_gse', newname='vec_rgeo')
        dat1 = get_data('mat_rgeo')
        dat2 = get_data('vec_rgeo')
        assert_allclose(dat1.y, self.mat_rgeo_thm.y, atol=.002)
        assert_allclose(dat2.y, self.vec_rgeo_thm.y, atol=.002)

    @unittest.skip('skipping, IDL results are probably wrong')
    def test_fac_phigeo(self):
        """Test of other_dim = phigeo"""

        fac_matrix_make('idl_thc_fgs_gse_sm601',other_dim='phigeo',pos_var_name='idl_thc_state_pos', newname='mat_phigeo')
        tvector_rotate('mat_phigeo', 'idl_thc_fgs_gse', newname='vec_phigeo')
        dat1 = get_data('mat_phigeo')
        dat2 = get_data('vec_phigeo')
        assert_allclose(dat1.y, self.mat_phigeo.y, atol=.002)
        assert_allclose(dat2.y, self.vec_phigeo.y, atol=.002)

    def test_fac_phigeo_thm(self):
        """Test of other_dim = phigeo"""

        fac_matrix_make('idl_thc_fgs_gse_sm601',other_dim='phigeo',pos_var_name='idl_thc_state_pos', newname='mat_phigeo')
        tvector_rotate('mat_phigeo', 'idl_thc_fgs_gse', newname='vec_phigeo')
        dat1 = get_data('mat_phigeo')
        dat2 = get_data('vec_phigeo')
        assert_allclose(dat1.y, self.mat_phigeo_thm.y, atol=.002)
        assert_allclose(dat2.y, self.vec_phigeo_thm.y, atol=.002)

    @unittest.skip('skipping, IDL results are probably wrong')
    def test_fac_mphigeo(self):
        """Test of other_dim = phigeo"""

        fac_matrix_make('idl_thc_fgs_gse_sm601',other_dim='mphigeo',pos_var_name='idl_thc_state_pos', newname='mat_mphigeo')
        tvector_rotate('mat_mphigeo', 'idl_thc_fgs_gse', newname='vec_mphigeo')
        dat1 = get_data('mat_mphigeo')
        dat2 = get_data('vec_mphigeo')
        assert_allclose(dat1.y, self.mat_mphigeo.y, atol=.002)
        assert_allclose(dat2.y, self.vec_mphigeo.y, atol=.002)

    def test_fac_mphigeo_thm(self):
        """Test of other_dim = phigeo"""

        fac_matrix_make('idl_thc_fgs_gse_sm601',other_dim='mphigeo',pos_var_name='idl_thc_state_pos', newname='mat_mphigeo')
        tvector_rotate('mat_mphigeo', 'idl_thc_fgs_gse', newname='vec_mphigeo')
        dat1 = get_data('mat_mphigeo')
        dat2 = get_data('vec_mphigeo')
        assert_allclose(dat1.y, self.mat_mphigeo_thm.y, atol=.002)
        assert_allclose(dat2.y, self.vec_mphigeo_thm.y, atol=.002)

    def test_fac_phism(self):
        """Test of other_dim = phigeo"""

        fac_matrix_make('idl_thc_fgs_gse_sm601',other_dim='phism',pos_var_name='idl_thc_state_pos', newname='mat_phism')
        tvector_rotate('mat_phism', 'idl_thc_fgs_gse', newname='vec_phism')
        dat1 = get_data('mat_phism')
        dat2 = get_data('vec_phism')
        assert_allclose(dat1.y, self.mat_phism.y, atol=.002)
        assert_allclose(dat2.y, self.vec_phism.y, atol=.002)

    def test_fac_phism_thm(self):
        """Test of other_dim = phigeo"""

        fac_matrix_make('idl_thc_fgs_gse_sm601',other_dim='phism',pos_var_name='idl_thc_state_pos', newname='mat_phism')
        tvector_rotate('mat_phism', 'idl_thc_fgs_gse', newname='vec_phism')
        dat1 = get_data('mat_phism')
        dat2 = get_data('vec_phism')
        assert_allclose(dat1.y, self.mat_phism_thm.y, atol=.002)
        assert_allclose(dat2.y, self.vec_phism_thm.y, atol=.002)

    def test_fac_mphism(self):
        """Test of other_dim = phigeo"""

        fac_matrix_make('idl_thc_fgs_gse_sm601',other_dim='mphism',pos_var_name='idl_thc_state_pos', newname='mat_mphism')
        tvector_rotate('mat_mphism', 'idl_thc_fgs_gse', newname='vec_mphism')
        dat1 = get_data('mat_mphism')
        dat2 = get_data('vec_mphism')
        assert_allclose(dat1.y, self.mat_mphism.y, atol=.002)
        assert_allclose(dat2.y, self.vec_mphism.y, atol=.002)

    def test_fac_mphism_thm(self):
        """Test of other_dim = phigeo"""

        fac_matrix_make('idl_thc_fgs_gse_sm601',other_dim='mphism',pos_var_name='idl_thc_state_pos', newname='mat_mphism')
        tvector_rotate('mat_mphism', 'idl_thc_fgs_gse', newname='vec_mphism')
        dat1 = get_data('mat_mphism')
        dat2 = get_data('vec_mphism')
        assert_allclose(dat1.y, self.mat_mphism_thm.y, atol=.002)
        assert_allclose(dat2.y, self.vec_mphism_thm.y, atol=.002)

    def test_fac_ygsm(self):
        """Test of other_dim = ygsm"""

        fac_matrix_make('idl_thc_fgs_gse_sm601',other_dim='ygsm',pos_var_name='idl_thc_state_pos', newname='mat_ygsm')
        tvector_rotate('mat_ygsm', 'idl_thc_fgs_gse', newname='vec_ygsm')
        dat1 = get_data('mat_ygsm')
        dat2 = get_data('vec_ygsm')
        assert_allclose(dat1.y, self.mat_ygsm.y, atol=.002)
        assert_allclose(dat2.y, self.vec_ygsm.y, atol=.002)

    def test_fac_ygsm_thm(self):
        """Test of other_dim = ygsm"""

        fac_matrix_make('idl_thc_fgs_gse_sm601',other_dim='ygsm',pos_var_name='idl_thc_state_pos', newname='mat_ygsm')
        tvector_rotate('mat_ygsm', 'idl_thc_fgs_gse', newname='vec_ygsm')
        dat1 = get_data('mat_ygsm')
        dat2 = get_data('vec_ygsm')
        assert_allclose(dat1.y, self.mat_ygsm_thm.y, atol=.002)
        assert_allclose(dat2.y, self.vec_ygsm_thm.y, atol=.002)


if __name__ == '__main__':
    unittest.main()

