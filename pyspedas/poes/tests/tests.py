
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_sem_data(self):
        sem_vars = pyspedas.poes.sem()
        self.assertTrue(data_exists('ted_ele_tel0_low_eflux'))

if __name__ == '__main__':
    unittest.main()