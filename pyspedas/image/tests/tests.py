
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_mena_data(self):
        mena_vars = pyspedas.image.mena()
        self.assertTrue(data_exists('Image0'))

if __name__ == '__main__':
    unittest.main()