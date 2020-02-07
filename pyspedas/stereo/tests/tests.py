
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_mag_data(self):
        mag_vars = pyspedas.stereo.mag(trange=['2013-11-5', '2013-11-6'])
        self.assertTrue(data_exists('BFIELD'))

if __name__ == '__main__':
    unittest.main()