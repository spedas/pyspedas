
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_mag_data(self):
        mag_vars = pyspedas.solo.mag(time_clip=True)
        self.assertTrue(data_exists('B_RTN'))

    def test_load_epd_data(self):
        epd_vars = pyspedas.solo.epd()
        self.assertTrue(data_exists('Magnet_Rows_Flux'))
        self.assertTrue(data_exists('Integral_Rows_Flux'))
        self.assertTrue(data_exists('Magnet_Cols_Flux'))
        self.assertTrue(data_exists('Integral_Cols_Flux'))

    def test_load_rpw_data(self):
        rpw_vars = pyspedas.solo.rpw()
        self.assertTrue(data_exists('AVERAGE_NR'))
        self.assertTrue(data_exists('TEMPERATURE'))
        self.assertTrue(data_exists('FLUX_DENSITY1'))
        self.assertTrue(data_exists('FLUX_DENSITY2'))

    def test_load_swa_data(self):
        swa_vars = pyspedas.solo.swa()
        self.assertTrue(data_exists('eflux'))

    def test_downloadonly(self):
        files = pyspedas.solo.mag(downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

if __name__ == '__main__':
    unittest.main()