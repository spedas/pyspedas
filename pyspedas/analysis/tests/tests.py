"""Automated tests for the analysis functions."""

import unittest
from pyspedas.analysis.tsmooth import smooth
from pyspedas import (subtract_average, subtract_median, tsmooth, avg_data,
                      yclip, time_clip, deriv_data, tdeflag, clean_spikes,
                      tinterpol)
from pyspedas.analysis.tcrossp import tcrossp
from pyspedas.analysis.tdotp import tdotp
from pyspedas.analysis.tnormalize import tnormalize
from pytplot import get_data, store_data, replace_data

import numpy as np


class BaseTestCase(unittest.TestCase):
    """Data to be used in tests."""

    def setUp(self):
        """Create a tplot variable to be used in tests."""
        store_data('test', data={'x': [1., 2., 3., 4., 5., 6.],
                                 'y': [3., 5., 8., 15., 20., 1.]})


class AnalysisTestCases(BaseTestCase):
    """Test functions under analysis folder."""
    def test_tdotp(self):
        store_data('var1', data={'x': [0], 'y': [[3, -3, 1]]})
        store_data('var2', data={'x': [0], 'y': [[4, 9, 2]]})
        dp = tdotp('var1', 'var2')
        dpdata = get_data('var1_dot_var2')
        self.assertTrue(dpdata.y == np.array([-13]))

    def test_tcrossp(self):
        """ cross product tests"""
        cp = tcrossp([3, -3, 1], [4, 9, 2], return_data=True)
        self.assertTrue(cp.tolist() == [-15, -2, 39])
        cp = tcrossp([3, -3, 1], [4, 9, 2])
        cp = get_data(cp)
        self.assertTrue(cp.y[0, :].tolist() == [-15, -2, 39])
        store_data('var1', data={'x': [0], 'y': [[3, -3, 1]]})
        store_data('var2', data={'x': [0], 'y': [[4, 9, 2]]})
        cp = tcrossp('var1', 'var2', return_data=True)
        self.assertTrue(cp[0].tolist() == [-15, -2, 39])
        cp = tcrossp('var1', 'var2', newname='test_crossp')
        cp = get_data('test_crossp')
        self.assertTrue(cp.y[0, :].tolist() == [-15, -2, 39])

    def test_tnormalize(self):
        """ tests for normalizing tplot variables"""
        store_data('test_tnormalize', data={'x': [1, 2, 3, 4, 5], 'y': [[3, 2, 1], [1, 2, 3], [10, 5, 1], [8, 10, 14], [70, 20, 10]]})
        norm = tnormalize('test_tnormalize')
        normalized_data = get_data(norm)
        self.assertTrue(np.round(normalized_data.y[0, :], 4).tolist() == [0.8018, 0.5345, 0.2673])
        self.assertTrue(np.round(normalized_data.y[1, :], 4).tolist() == [0.2673, 0.5345, 0.8018])
        self.assertTrue(np.round(normalized_data.y[2, :], 4).tolist() == [0.8909, 0.4454, 0.0891])
        self.assertTrue(np.round(normalized_data.y[3, :], 4).tolist() == [0.4216, 0.527, 0.7379])
        self.assertTrue(np.round(normalized_data.y[4, :], 4).tolist() == [0.9526, 0.2722, 0.1361])

    def test_subtract_median(self):
        """Test subtract_median."""
        subtract_median('aaabbbccc')  # Test non-existent name
        subtract_median('test')
        d = get_data('test-m')
        self.assertTrue(d[1].tolist() == [-3.5, -1.5,  1.5,  8.5, 13.5, -5.5])
        dn = [[3., 5., 8.], [15., 20., 1.], [3., 5., 8.], [15., 20., 1.],
              [23., 15., 28.], [15., 20., float('nan')]]
        store_data('test1', data={'x': [1., 2., 3., 4., 5., 6.], 'y': dn})
        subtract_median('aaabbbcc')
        subtract_median('test1', new_names='aabb')
        d = get_data('aabb')
        subtract_median(['test', 'aabb'], new_names='aaabbb')
        subtract_median('test1', overwrite=1)
        subtract_average('test', new_names="testtest")
        subtract_average(['test-m', 'test'], new_names="testtest2")
        self.assertTrue(len(d[1]) == 6)

    def test_subtract_average(self):
        """Test subtract_average."""
        subtract_average('aaabbbccc')  # Test non-existent name
        subtract_average('test')
        d = get_data('test-d')
        self.assertTrue((np.round(d[1].tolist()) == [-6., -4., -1.,
                         6., 11., -8.]).all())
        dn = [[3., 5., 8.], [15., 20., 1.], [3., 5., 8.], [15., 20., 1.],
              [23., 15., 28.], [15., 20., float('nan')]]
        store_data('test1', data={'x': [1., 2., 3., 4., 5., 6.], 'y': dn})
        subtract_average('aaabbbcc')
        subtract_average('test1', new_names='aabb')
        d = get_data('aabb')
        subtract_average(['test', 'aabb'], new_names='aaabbb')
        subtract_average('test1', overwrite=1)
        subtract_average('test1', new_names="testtest")
        subtract_average(['test1', 'test'], new_names="testtest2")
        self.assertTrue(len(d[1]) == 6)

    def test_yclip(self):
        """Test yclip."""
        yclip('aaabbbccc', 0.0, 12.0)  # Test non-existent name
        yclip('aabb', 0.0, 12.0)
        yclip('test', 0.0, 12.0)
        d = get_data('test-clip')
        # Replace nan with -99.0
        dd = np.nan_to_num(d[1], nan=-99.)
        yclip('test', 0.0, 12.0, new_names='name-clip')
        yclip(['test', 'name-clip'], 0.0, 12.0, new_names='name1-clip')
        yclip('test', 0.0, 12.0, overwrite=1)
        yclip('test', 0.0, 12.0, new_names="testtest")
        yclip(['test', 'test-clip'], 0.0, 12.0, new_names="testtest2")
        self.assertTrue((dd == [3., 5., 8., -99., -99., 1.]).all())

    def test_timeclip(self):
        """Test time_clip."""
        time_clip('aaabbbccc', 1577308800, 1577598800)  # Test non-existent
        tn = [1577112800, 1577308800, 1577598800, 1577608800, 1577998800,
              1587998800]
        dn = [3., 5., 8., 15., 20., 1.]
        store_data('test1', data={'x': tn, 'y': dn})
        time_clip('aaabbb', 1577308800, 1577598800)
        time_clip('test1', 1577112800, 1577608800)
        d = get_data('test1-tclip')
        dd = d[1]
        time_clip('test', 1577308800, 1577598800, new_names='name-clip')
        time_clip(['test', 'name-clip'], 1577308800, 1577598800,
                  new_names='name1-ci')
        time_clip('test', 1577308800, 1577598800, overwrite=1)
        time_clip('test', 1577308800, 1577598800, new_names="testtest")
        time_clip(['test', 'test1'], 1577308800, 1577598800,
                  new_names="testtest2")
        time_clip('test1', 1677112800, 1577608800)
        self.assertTrue((dd == [3., 5., 8., 15.]).all())

    def test_avg_data(self):
        """Test avg_data."""
        avg_data('aaabbbccc', width=2)  # Test non-existent name
        avg_data('test', width=2)
        d = get_data('test-avg')
        self.assertTrue((d[1] == [4.0, 11.5, 10.5]).all())
        avg_data('test', width=2, overwrite=True)  # Test overwrite
        avg_data('test', dt=4.0, noremainder=False)  # Test dt option
        store_data('test', data={'x': [1., 2., 3., 4., 5., 6.],
                                 'y': [3., 5., 8., -4., 20., 1.]})
        avg_data('test', width=2, new_names='aabb')  # Test new_names
        d = get_data('aabb')
        # Test multiple names
        avg_data(['test', 'aabb'], new_names='aaabbb', width=2)
        dn = [[3., 5., 8.], [15., 20., 1.], [3., 5., 8.], [15., 20., 1.],
              [23., 15., 28.], [15., 20., 1.]]
        store_data('test1', data={'x': [1., 12., 13., 14., 15., 16.], 'y': dn})
        avg_data('test1', width=2)  # Test 3-d data
        avg_data('test1', new_names='test2', dt=2.)  # Test a reasonable dt
        avg_data('test1', dt=-1.)  # Test dt error
        avg_data('test1', dt=1.e8)  # Test dt error
        d2 = get_data('test2')
        self.assertTrue(len(d) > 0)
        self.assertTrue(d2[1][-1][0] == 19.0)

    def test_clean_spikes(self):
        """Test clean_spikes."""
        clean_spikes('aaabbbccc', nsmooth=3)  # Test non-existent name
        clean_spikes('test', nsmooth=3)
        d = get_data('test-despike')
        self.assertTrue(len(d[1]) == 6)
        # Now test 3 dim data.
        dn = [[3., 5., 8.], [15., 20., 1.], [3., 5., 8.], [15., 20., 1.],
              [23., 15., 28.], [15., 20., 1.]]
        store_data('test1', data={'x': [1., 2., 3., 4., 5., 6.], 'y': dn})
        clean_spikes('test1', nsmooth=3)
        d2 = get_data('test1-despike')
        clean_spikes('test', new_names='test_desp', nsmooth=3, sub_avg=True)
        clean_spikes(['test', 'test1'], new_names='test1-desp')
        clean_spikes('test1', overwrite=1)
        self.assertTrue(len(d2[1]) == 6)

    def test_tdeflag(self):
        """Test tdeflag."""
        tdeflag('aaabbbccc')  # Test non-existent name
        dn = [3., float('NaN'), 8., float('NaN'), 20., 1.]
        len_dn = len(dn)
        replace_data('test', dn)
        tdeflag('test')
        d = get_data('test-deflag')
        tdeflag('test', overwrite=1)
        tdeflag('test', new_names="testtest")
        tdeflag(['test', 'test-deflag'], new_names="testtest2")
        # Length should be two less, because NaNs were removed.
        self.assertTrue(len(d[1]) == len_dn - 2)

    def test_deriv_data(self):
        """Test deriv_data."""
        deriv_data('aaabbbccc')  # Test non-existent name
        deriv_data('test')
        d = get_data('test-der')
        deriv_data('test', overwrite=1)
        deriv_data('test', new_names="testtest")
        deriv_data(['test', 'test-der'], new_names="testtest2")
        self.assertTrue((d[1] == [2., 2.5, 5.,   6., -7., -19.]).all())

    def test_tsmooth(self):
        """Test smooth."""
        tsmooth('aaabbbccc')  # Test non-existent name
        a = [1.0, 1.0, 2.0, 3.0, 4.0, 1.0, 4.0, 3.0, 2.0, 1.0, 1.0]
        x = smooth(a, 3)
        r = [1.0, 1.3333333333333333, 2.0, 3.0, 2.6666666666666665,
             3.0, 2.6666666666666665, 3.0, 2.0, 1.3333333333333333, 1.0]
        self.assertTrue(x == r)
        b = [1.0, 1.0, 2.0, 3.0, np.NaN, np.NaN, np.NaN, np.NaN, 2.0, 1.0, 1.0]
        y = smooth(b, width=3)
        ry = [1.0, 1.3333333333333333, 2.0, 1.6666666666666665, 1.0,
              np.nan, np.nan, 0.6666666666666666, 1.0, 1.3333333333333333, 1.0]
        self.assertTrue(y == ry)
        tsmooth('test')
        d = get_data('test-s')
        tsmooth('test', overwrite=1)
        tsmooth('test', new_names="testtest")
        tsmooth(['test', 'test-s'], new_names="testtest2")
        self.assertTrue(d[1].tolist() == [3.,  5.,  8., 15., 20.,  1.])

    def test_tinterpol(self):
        """Test tinterpol."""
        tinterpol('aaabbbccc', 'test')  # Test non-existent name
        tn = [1., 1.5, 4.6, 5.8, 6.]
        dn = [10., 15., 46., 58., 60.]
        store_data('test1', data={'x': tn, 'y': dn})
        tinterpol('test1', 'test')
        d = get_data('test1-itrp')
        self.assertTrue(d[1][1] == 20.)


if __name__ == '__main__':
    unittest.main()
