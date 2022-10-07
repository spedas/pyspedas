import os
import unittest
from pyspedas.utilities.data_exists import data_exists
from pytplot import get_data
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_notplot(self):
        sem_vars = pyspedas.poes.sem(notplot=True)
        self.assertTrue('ted_ele_tel0_low_eflux' in sem_vars)

    def test_load_sem_data(self):
        sem_vars = pyspedas.poes.sem(time_clip=True)
        self.assertTrue(data_exists('ted_ele_tel0_low_eflux'))

    def test_load_probe_regression(self):
        sem_vars = pyspedas.poes.sem(probe='metop1', time_clip=True)
        self.assertTrue(data_exists('ted_ele_tel0_low_eflux'))
        m = get_data('ted_ele_tel0_low_eflux', metadata=True)
        self.assertTrue(m['CDF']['GATT']['Source_name'] == 'MetOp1')
        sem_vars = pyspedas.poes.sem(probe='metop2', time_clip=True)
        m = get_data('ted_ele_tel0_low_eflux', metadata=True)
        self.assertTrue(m['CDF']['GATT']['Source_name'] == 'MetOp2')

    def test_downloadonly(self):
        files = pyspedas.poes.sem(downloadonly=True, probe='noaa19')
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()
