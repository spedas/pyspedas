import os
import unittest
from pytplot import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_none_data(self):
        induction_vars = pyspedas.projects.mica.induction()
        self.assertTrue(induction_vars == None)

    def test_load_notplot(self):
        induction_vars = pyspedas.projects.mica.induction(site='nal', notplot=True)
        self.assertTrue('spectra_x_1Hz_NAL' in induction_vars)

    def test_load_NAL_data(self):
        induction_vars = pyspedas.projects.mica.induction(site='nal', time_clip=True)
        self.assertTrue(data_exists('spectra_x_1Hz_NAL'))

    def test_downloadonly(self):
        files = pyspedas.projects.mica.induction(site='nal', downloadonly=True, trange=['2014-2-15', '2014-2-16'])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()
