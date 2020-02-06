
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_mgf_data(self):
        mgf_vars = pyspedas.geotail.mgf()
        self.assertTrue(data_exists('IB_vector'))

if __name__ == '__main__':
    unittest.main()