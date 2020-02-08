
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        files = pyspedas.stereo.mag(trange=['2013-11-6', '2013-11-7'], downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_load_mag_data(self):
        mag_vars = pyspedas.stereo.mag(trange=['2013-11-5', '2013-11-6'], time_clip=True)
        self.assertTrue(data_exists('BFIELD'))

    def test_load_plastic_data(self):
        p_vars = pyspedas.stereo.plastic(trange=['2013-11-5', '2013-11-6'], probe='b')
        self.assertTrue(data_exists('proton_number_density'))
        self.assertTrue(data_exists('proton_bulk_speed'))
        self.assertTrue(data_exists('proton_temperature'))

if __name__ == '__main__':
    unittest.main()