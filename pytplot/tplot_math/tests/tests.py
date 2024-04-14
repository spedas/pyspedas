"""Automated tests for tplot math and utility functions."""

import unittest
from pytplot.tplot_math import (clean_spikes, smooth, tsmooth, tdotp, tcrossp, tnormalize, subtract_median,
    subtract_average, time_clip)
from pytplot import get_data, store_data, time_double, time_string, time_datetime
from datetime import datetime,timezone
import numpy as np


class BaseTestCase(unittest.TestCase):
    """Data to be used in tests."""

    def setUp(self):
        """Create a tplot variable to be used in tests."""
        store_data('test', data={'x': [1., 2., 3., 4., 5., 6.],
                                 'y': [3., 5., 8., 15., 20., 1.]})


class AnalysisTestCases(BaseTestCase):
    """Test functions under tplot_math, and some other utilities."""

    def test_tdotp(self):
        store_data('var1', data={'x': [0], 'y': [[3, -3, 1]]})
        store_data('var2', data={'x': [0], 'y': [[4, 9, 2]]})
        dp = tdotp('var1', 'var2')
        dpdata = get_data('var1_dot_var2')
        self.assertTrue(dpdata.y == np.array([-13]))
        dp = tdotp('var1_doesnt_exist', 'var2')
        dp = tdotp('var1', 'var2_doesnt_exist')

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
        self.assertTrue(len(d[1]) == 6)
        subtract_median(['test', 'aabb'], new_names='aaabbb')
        subtract_median('test1', overwrite=1)
        subtract_average('test', new_names="testtest")
        subtract_average(['test-m', 'test'], new_names="testtest2")

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
        self.assertTrue(len(d[1]) == 6)
        subtract_average(['test', 'aabb'], new_names='aaabbb')
        subtract_average('test1', overwrite=1)
        subtract_average('test1', new_names="testtest")
        subtract_average(['test1', 'test'], new_names="testtest2")


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
        clean_spikes('test', newname='test_desp', nsmooth=3, sub_avg=True)
        clean_spikes(['test', 'test1'], newname='test1-desp')
        clean_spikes('test1', overwrite=1)
        self.assertTrue(len(d2[1]) == 6)

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

    def test_time_datetime(self):
        """Test time_datetime function."""
        now = time_datetime()
        self.assertTrue(time_datetime('2015-12-15/00:00') == datetime(2015, 12, 15, 0, 0, tzinfo=timezone.utc))
        self.assertTrue(time_datetime(1450137600.0000000) == datetime(2015, 12, 15, 0, 0, tzinfo=timezone.utc))
        self.assertTrue([time_datetime(1450137600.0000000), time_datetime(1444953600.0000000)]
            == [datetime(2015, 12, 15, 0, 0, tzinfo=timezone.utc), datetime(2015, 10, 16, 0, 0, tzinfo=timezone.utc)])
        self.assertTrue(time_datetime([1450137600.0000000, 1444953600.0000000])
            == [datetime(2015, 12, 15, 0, 0, tzinfo=timezone.utc), datetime(2015, 10, 16, 0, 0, tzinfo=timezone.utc)])


    def test_time_string(self):
        """Test time_string function."""
        self.assertTrue(time_string(fmt='%Y-%m-%d') == datetime.now().strftime('%Y-%m-%d'))
        self.assertTrue(time_string(1450181243.767, fmt='%Y-%m-%d') == '2015-12-15')
        self.assertTrue(time_string(1450181243.767, fmt='%Y-%m-%d/%H:%M:%S') == '2015-12-15/12:07:23')
        self.assertTrue(time_string(1450181243.767) == '2015-12-15 12:07:23.767000')
        self.assertTrue(time_string([1450181243.767, 1450181263.767]) == ['2015-12-15 12:07:23.767000', '2015-12-15 12:07:43.767000'])

    def test_time_double(self):
        """Test time_double function."""
        self.assertTrue(time_string(time_double(), fmt='%Y-%m-%d') == datetime.now().strftime('%Y-%m-%d'))
        self.assertTrue(time_double('2015-12-15/12:00') == 1450180800.0000000)
        self.assertTrue(time_double('2015-12-15/12') == 1450180800.0000000)
        #self.assertTrue(time_double('2015-12-15/6') == 1450159200.0000000) #this one doesn't work
        self.assertTrue(time_double('2015-12-15/6:00') == 1450159200.0000000)
        self.assertTrue(time_double('2015-12-15/06:00') == 1450159200.0000000)
        self.assertTrue(time_double('2015-12-15') == 1450137600.0000000)
        self.assertTrue(time_double('2015 12 15') == 1450137600.0000000)
        self.assertTrue(time_double('2015-12') == 1448928000.0000000)
        self.assertTrue(time_double('2015') == 1420070400.0000000)
        self.assertTrue(time_double('2015-12-15 12:07:23.767000') == 1450181243.767)
        self.assertTrue(time_double(['2015-12-15 12:07:23.767000', '2015-12-15 12:07:43.767000']) == [1450181243.767, 1450181263.767])


if __name__ == '__main__':
    unittest.main()
