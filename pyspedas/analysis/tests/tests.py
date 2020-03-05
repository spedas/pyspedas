
import unittest
from pyspedas.utilities.data_exists import data_exists

from pyspedas import subtract_average, subtract_median, yclip, tdeflag, time_clip, tinterpol, tdpwrspc, time_double, time_string
from pytplot import get_data, store_data

import numpy as np

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        store_data('test', data={'x': [1., 2., 3., 4., 5., 6.], 'y': [3., 5., 8., 15., 20., 1.]})

class AnalysisTestCases(BaseTestCase):
    def test_subtract_median(self):
        subtract_median('test')
        t, d = get_data('test-m')
        self.assertTrue(d.tolist() == [-3.5, -1.5,  1.5,  8.5, 13.5, -5.5])

    def test_subtract_average(self):
        subtract_average('test')
        t, d = get_data('test-d')
        self.assertTrue((np.round(d.tolist()) == [-6., -4., -1.,  6., 11., -8.]).all())

if __name__ == '__main__':
    unittest.main()
