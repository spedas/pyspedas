
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_mag_data(self):
        mag_vars = pyspedas.solo.mag(time_clip=True)
        self.assertTrue(data_exists('B_RTN'))

    def test_downloadonly(self):
        files = pyspedas.solo.mag(downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

if __name__ == '__main__':
    unittest.main()