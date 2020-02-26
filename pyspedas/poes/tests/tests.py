
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_sem_data(self):
        sem_vars = pyspedas.poes.sem(time_clip=True)
        self.assertTrue(data_exists('ted_ele_tel0_low_eflux'))

    def test_downloadonly(self):
        files = pyspedas.poes.sem(downloadonly=True, probe='noaa19')
        self.assertTrue(os.path.exists(files[0]))

if __name__ == '__main__':
    unittest.main()