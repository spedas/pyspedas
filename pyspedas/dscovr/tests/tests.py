
import os
import unittest
from pyspedas.utilities.data_exists import data_exists

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_load_mag_data(self):
        mag_vars = pyspedas.dscovr.mag(time_clip=True)
        self.assertTrue(data_exists('B1RTN'))
        self.assertTrue(data_exists('B1GSE'))

    def test_load_fc_data(self):
        fc_vars = pyspedas.dscovr.fc()
        self.assertTrue(data_exists('Np'))
        self.assertTrue(data_exists('THERMAL_TEMP'))

    def test_load_orb_data(self):
        orb_vars = pyspedas.dscovr.orb()
        self.assertTrue(data_exists('GSE_POS'))
        self.assertTrue(data_exists('GCI_POS'))

    def test_load_att_data(self):
        att_vars = pyspedas.dscovr.att()
        self.assertTrue(data_exists('GCI_Yaw'))
        self.assertTrue(data_exists('GCI_Pitch'))
        self.assertTrue(data_exists('GCI_Roll'))

    def test_load_downloadonly(self):
        files = pyspedas.dscovr.mag(downloadonly=True, trange=['2018-12-15', '2018-12-16'])
        self.assertTrue(os.path.exists(files[0]))

    def test_load_all(self):
        t_all = pyspedas.dscovr.all()
        self.assertTrue(len(t_all) > 0)
        
        
if __name__ == '__main__':
    unittest.main()