import os
import unittest
from pytplot import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_downloadonly(self):
        files = pyspedas.projects.twins.imager(downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))

    def test_load_img_data(self):
        img_vars = pyspedas.projects.twins.imager()
        self.assertTrue(data_exists('smooth_image_val'))
        img_vars = pyspedas.projects.twins.imager(notplot=True)
        self.assertTrue('smooth_image_val' in img_vars)

    def test_load_lad_data(self):
        lad_vars = pyspedas.projects.twins.lad(time_clip=True)
        self.assertTrue(data_exists('lad1_data'))
        self.assertTrue(data_exists('lad2_data'))

    def test_load_lad_data_prefix_none(self):
        lad_vars = pyspedas.projects.twins.lad(prefix=None)
        self.assertTrue(data_exists('lad1_data'))
        self.assertTrue(data_exists('lad2_data'))

    def test_load_lad_data_suffix_none(self):
        lad_vars = pyspedas.projects.twins.lad(suffix=None)
        self.assertTrue(data_exists('lad1_data'))
        self.assertTrue(data_exists('lad2_data'))

    def test_load_lad_data_prefix_suffix(self):
        lad_vars = pyspedas.projects.twins.lad(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_lad1_data_suf'))
        self.assertTrue(data_exists('pre_lad2_data_suf'))

    def test_load_ephem_data(self):
        ephemeris_vars = pyspedas.projects.twins.ephemeris()
        self.assertTrue(data_exists('FLTGEO'))


if __name__ == '__main__':
    unittest.main()
