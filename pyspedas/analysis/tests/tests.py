"""Automated tests for the analysis functions."""

import unittest
from pyspedas.analysis.tsmooth import smooth
from pyspedas import (subtract_average, subtract_median, tsmooth, avg_data,
                      yclip, deriv_data, version, tdeflag, clean_spikes,
                      tcopy)
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

    def test_version(self):
        """Test pyspedas.version()."""
        version()
        self.assertTrue(1. == 1.)

    def test_subtract_median(self):
        """Test subtract_median."""
        subtract_median('test')
        d = get_data('test-m')
        self.assertTrue(d[1].tolist() == [-3.5, -1.5,  1.5,  8.5, 13.5, -5.5])

    def test_subtract_average(self):
        """Test subtract_average."""
        subtract_average('test')
        d = get_data('test-d')
        self.assertTrue((np.round(d[1].tolist()) == [-6., -4., -1.,
                         6., 11., -8.]).all())

    def test_yclip(self):
        """Test yclip."""
        yclip('test', 0.0, 12.0)
        d = get_data('test-clip')
        # Replace nan with -99.0
        dd = np.nan_to_num(d[1], nan=-99.)
        self.assertTrue((dd == [3., 5., 8., -99., -99., 1.]).all())

    def test_avg_data(self):
        """Test avg_data."""
        avg_data('test', width=2)
        d = get_data('test-avg')
        self.assertTrue((d[1] == [4.0, 11.5, 10.5]).all())

    def test_clean_spikes(self):
        """Test clean_spikes."""
        clean_spikes('test', nsmooth=3)
        d = get_data('test-despike')
        self.assertTrue(len(d[1]) == 6)
        # Now test 3 dim data.
        dn = [[3., 5., 8.],[ 15., 20., 1.], [3., 5., 8.], [15., 20., 1.],
              [23., 15., 28.], [15., 20., 1.]]
        store_data('test1', data={'x': [1., 2., 3., 4., 5., 6.],
                                 'y': dn})
        replace_data('test1', dn)
        clean_spikes('test1', nsmooth=3)
        d2 = get_data('test1-despike')
        self.assertTrue(len(d2[1]) == 6)

    def test_tdeflag(self):
        """Test tdeflag."""
        dn = [3., float('NaN'), 8., float('NaN'), 20., 1.]
        len_dn = len(dn)
        replace_data('test', dn)
        tdeflag('test')
        d = get_data('test-deflag')
        # Length should be two less, because NaNs were removed.
        self.assertTrue(len(d[1]) == len_dn - 2)

    def test_deriv_data(self):
        """Test deriv_data."""
        deriv_data('test')
        d = get_data('test-der')
        version()
        self.assertTrue((d[1] == [2., 2.5, 5.,   6., -7., -19.]).all())

    def test_tsmooth(self):
        """Test smooth."""
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
        self.assertTrue(d[1].tolist() == [3.,  5.,  8., 15., 20.,  1.])


if __name__ == '__main__':
    unittest.main()
