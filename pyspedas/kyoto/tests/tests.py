
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_dst_data(self):
        dst_vars = pyspedas.kyoto.dst(trange=['2015-10-15', '2015-10-16'])
        self.assertTrue(data_exists('kyoto_dst'))

if __name__ == '__main__':
    unittest.main()