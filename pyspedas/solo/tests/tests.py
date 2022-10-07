import os
import unittest
from pyspedas.utilities.data_exists import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_mag_data(self):
        mag_vars = pyspedas.solo.mag(time_clip=True)
        self.assertTrue(data_exists('B_RTN'))
        mag_vars = pyspedas.solo.mag(datatype='rtn-normal-1-minute')
        self.assertTrue(data_exists('B_RTN'))
        mag_vars = pyspedas.solo.mag(notplot=True, datatype='rtn-burst')
        self.assertTrue('B_RTN' in mag_vars)

    def test_load_mag_ll02_data(self):
        mag_vars = pyspedas.solo.mag(level='ll02', trange=['2020-08-04', '2020-08-05'])
        self.assertTrue(data_exists('B_RTN'))
        self.assertTrue(data_exists('B_SRF'))

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
        swa_vars = pyspedas.solo.swa(level='l2', datatype='eas1-nm3d-def')
        self.assertTrue(data_exists('SWA_EAS1_Data'))
        swa_vars = pyspedas.solo.swa(notplot=True)
        self.assertTrue('eflux' in swa_vars)

    def test_load_swa_l1_data(self):
        swa_vars = pyspedas.solo.swa(level='l1', datatype='eas-padc')
        self.assertTrue(data_exists('SWA_EAS_BM_Data'))
        self.assertTrue(data_exists('SWA_EAS_MagDataUsed'))
        swa_vars = pyspedas.solo.swa(level='l1', datatype='his-pha', trange=['2020-06-03', '2020-06-04'])
        self.assertTrue(data_exists('HIS_PHA_EOQ_STEP'))

    def test_downloadonly(self):
        files = pyspedas.solo.mag(downloadonly=True)
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()
