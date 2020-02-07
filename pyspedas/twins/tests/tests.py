
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_img_data(self):
        img_vars = pyspedas.twins.imager()
        self.assertTrue(data_exists('smooth_image_val'))

if __name__ == '__main__':
    unittest.main()