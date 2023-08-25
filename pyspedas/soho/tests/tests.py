import os
import unittest
from pytplot import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_celias_data(self):
        out_vars = pyspedas.soho.celias(time_clip=True)
        self.assertTrue(data_exists('V_p'))
        self.assertTrue(data_exists('N_p'))

    def test_load_cosp_data(self):
        out_vars = pyspedas.soho.costep(time_clip=True)
        self.assertTrue(data_exists('P_int'))
        self.assertTrue(data_exists('He_int'))

    def test_load_erne_data(self):
        out_vars = pyspedas.soho.erne(time_clip=True)
        self.assertTrue(data_exists('PH'))

    def test_load_orbit_data(self):
        out_vars = pyspedas.soho.orbit(time_clip=True)
        self.assertTrue(data_exists('GSE_POS'))
        self.assertTrue(data_exists('GSE_VEL'))

    def test_load_notplot(self):
        out_vars = pyspedas.soho.erne(notplot=True)
        self.assertTrue('PH' in out_vars)

    def test_downloadonly(self):
        files = pyspedas.soho.erne(downloadonly=True, trange=['2006-06-01', '2006-06-02'])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()

    