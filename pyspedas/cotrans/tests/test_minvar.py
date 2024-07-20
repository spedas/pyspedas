"""
Unit Tests for minvar function.
"""
import pyspedas
from pyspedas.cotrans.minvar import minvar
from pyspedas.cotrans.minvar_matrix_make import minvar_matrix_make
from pytplot import data_exists, tplot_names, tplot
import numpy as np
import unittest



class TestMinvar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #  Test tolerance
        cls.tol = 1e-10

        # Define a random data array
        rng = np.random.default_rng(seed=31415)
        cls.rdata = rng.random((10, 3))

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
        pyspedas.themis.fgm(probe='c', trange=trange, level='l2', coord='gse')
        minvar_matrix_make('thc_fgs_gse',tstart='2007-07-10/07:54:00',tstop='2007-07-10/07:56:30')
        self.assertTrue(data_exists('thc_fgs_gse_mva_mat'))
        pyspedas.tvector_rotate('thc_fgs_gse_mva_mat','thc_fgs_gse',newname='mva_data_day')
        self.assertTrue((data_exists('mva_data_day')))
        # TODO: Verify against IDL SPEDAS results

    def test_minvar_matrix_make_hour(self):
        trange=['2007-07-10', '2007-07-11']
        pyspedas.themis.fgm(probe='c', trange=trange, level='l2', coord='gse')
        minvar_matrix_make('thc_fgs_gse', twindow=3600, tslide=300)
        self.assertTrue(data_exists('thc_fgs_gse_mva_mat'))
        pyspedas.tvector_rotate('thc_fgs_gse_mva_mat','thc_fgs_gse',newname='mva_data_hour')
        self.assertTrue((data_exists('mva_data_hour')))
        # TODO: Verify against IDL SPEDAS results

    def test_minvar_matrix_make_hour_interp(self):
        trange=['2007-07-10', '2007-07-11']
        pyspedas.themis.fgm(probe='c', trange=trange, level='l2', coord='gse')
        minvar_matrix_make('thc_fgs_gse', twindow=3600, tslide=300)
        self.assertTrue(data_exists('thc_fgs_gse_mva_mat'))
        pyspedas.tvector_rotate('thc_fgs_gse_mva_mat','thc_fgl_gse',newname='mva_data_hour_interp')
        self.assertTrue((data_exists('mva_data_hour_interp')))
        # TODO: Verify against IDL SPEDAS results

if __name__ == '__main__':
    unittest.main()

