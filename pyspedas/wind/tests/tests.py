
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_mfi_data(self):
        mfi_vars = pyspedas.wind.mfi(trange=['2013-11-5', '2013-11-6'])
        self.assertTrue(data_exists('BGSE'))

if __name__ == '__main__':
    unittest.main()