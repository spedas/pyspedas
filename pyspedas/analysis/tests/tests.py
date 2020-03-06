# -*- coding: utf-8 -*-
"""
File:
    test.py

Description:
    Automated tests for the analysis functions.

"""

import unittest
from pyspedas.analysis.tsmooth import smooth
from pyspedas import subtract_average, subtract_median
from pytplot import get_data, store_data

import numpy as np


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        store_data('test', data={'x': [1., 2., 3., 4., 5., 6.],
                                 'y': [3., 5., 8., 15., 20., 1.]})


class AnalysisTestCases(BaseTestCase):

    def test_subtract_median(self):
        subtract_median('test')
        t, d = get_data('test-m')
        self.assertTrue(d.tolist() == [-3.5, -1.5,  1.5,  8.5, 13.5, -5.5])

    def test_subtract_average(self):
        subtract_average('test')
        t, d = get_data('test-d')
        self.assertTrue((np.round(d.tolist()) == [-6., -4., -1.,
                         6., 11., -8.]).all())

    def test_tsmooth(self):
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


if __name__ == '__main__':
    unittest.main()
