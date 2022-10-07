import os
import unittest
from pyspedas.utilities.data_exists import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        files = pyspedas.twins.imager(downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_load_img_data(self):
        img_vars = pyspedas.twins.imager()
        self.assertTrue(data_exists('smooth_image_val'))
        img_vars = pyspedas.twins.imager(notplot=True)
        self.assertTrue('smooth_image_val' in img_vars)

    def test_load_lad_data(self):
        lad_vars = pyspedas.twins.lad(time_clip=True)
        self.assertTrue(data_exists('lad1_data'))
        self.assertTrue(data_exists('lad2_data'))

    def test_load_ephem_data(self):
        ephemeris_vars = pyspedas.twins.ephemeris()
        self.assertTrue(data_exists('FLTGEO'))


if __name__ == '__main__':
    unittest.main()
