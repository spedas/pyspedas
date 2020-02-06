
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_rep_data(self):
        rep_vars = pyspedas.csswe.reptile()
        self.assertTrue(data_exists('E1flux'))

if __name__ == '__main__':
    unittest.main()