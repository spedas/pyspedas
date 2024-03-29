import os
import unittest
from pytplot import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_rep_data(self):
        rep_vars = pyspedas.csswe.reptile(time_clip=True)
        self.assertTrue(data_exists('E1flux'))

    def test_load_notplot(self):
        rep_vars = pyspedas.csswe.reptile(notplot=True)
        self.assertTrue('E1flux' in rep_vars)

    def test_downloadonly(self):
        files = pyspedas.csswe.reptile(downloadonly=True, trange=['2014-2-15', '2014-2-16'])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()
