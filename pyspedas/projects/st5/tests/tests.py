import os
import unittest
from pytplot import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_mag_data(self):
        out_vars = pyspedas.projects.st5.mag(time_clip=True)
        self.assertTrue(data_exists('B_SM'))

    def test_load_notplot(self):
        out_vars = pyspedas.projects.st5.mag(notplot=True)
        self.assertTrue('B_SM' in out_vars)

    def test_downloadonly(self):
        files = pyspedas.projects.st5.mag(downloadonly=True, trange=['2006-06-01', '2006-06-02'])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()

    