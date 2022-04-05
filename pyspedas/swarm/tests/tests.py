import unittest
from pyspedas.utilities.data_exists import data_exists
import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_mag_data(self):
        vfm_vars = pyspedas.swarm.mag(probe='c', trange=['2017-03-27/06:00', '2017-03-27/08:00'], datatype='hr')
        self.assertTrue(data_exists('swarmc_B_VFM'))

if __name__ == '__main__':
    unittest.main()