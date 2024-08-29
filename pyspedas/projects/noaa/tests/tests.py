import unittest
import pyspedas
from pytplot import data_exists, del_data, get_data
import numpy as np


class LoadTestCases(unittest.TestCase):
    def test_load_kp_data_2024(self):
        # final
        del_data('*')
        kp_vars = pyspedas.noaa.noaa_load_kp(trange=['2024-01-01', '2024-01-02'])
        self.assertTrue('Kp' in kp_vars)
        self.assertTrue('ap' in kp_vars)
        self.assertTrue('Sol_Rot_Num' in kp_vars)
        self.assertTrue('Sol_Rot_Day' in kp_vars)
        self.assertTrue('Kp_Sum' in kp_vars)
        self.assertTrue('ap_Mean' in kp_vars)
        self.assertTrue('Cp' in kp_vars)
        self.assertTrue('C9' in kp_vars)
        self.assertTrue(data_exists('Kp'))
        self.assertTrue(data_exists('ap'))
        self.assertTrue(data_exists('Sol_Rot_Num'))
        self.assertTrue(data_exists('Sol_Rot_Day'))
        self.assertTrue(data_exists('Kp_Sum'))
        self.assertTrue(data_exists('ap_Mean'))
        self.assertTrue(data_exists('Cp'))
        self.assertTrue(data_exists('C9'))

    def test_load_kp_data_2014(self):
        # final
        del_data('*')
        kp_vars = pyspedas.noaa.noaa_load_kp(trange=['2014-01-01', '2014-01-02'])
        self.assertTrue('Kp' in kp_vars)
        self.assertTrue('ap' in kp_vars)
        self.assertTrue('Sol_Rot_Num' in kp_vars)
        self.assertTrue('Sol_Rot_Day' in kp_vars)
        self.assertTrue('Kp_Sum' in kp_vars)
        self.assertTrue('ap_Mean' in kp_vars)
        self.assertTrue('Cp' in kp_vars)
        self.assertTrue('C9' in kp_vars)
        self.assertTrue('Sunspot_Number' in kp_vars)
        self.assertTrue('F10.7' in kp_vars)
        self.assertTrue('Flux_Qualifier' in kp_vars)
        self.assertTrue(data_exists('Kp'))
        self.assertTrue(data_exists('ap'))
        self.assertTrue(data_exists('Sol_Rot_Num'))
        self.assertTrue(data_exists('Sol_Rot_Day'))
        self.assertTrue(data_exists('Kp_Sum'))
        self.assertTrue(data_exists('ap_Mean'))
        self.assertTrue(data_exists('Cp'))
        self.assertTrue(data_exists('C9'))
        self.assertTrue(data_exists('Sunspot_Number'))
        self.assertTrue(data_exists('F10.7'))
        self.assertTrue(data_exists('Flux_Qualifier'))

    def test_load_kp_data_2014_gfz(self):
        # final
        del_data('*')
        kp_vars = pyspedas.noaa.noaa_load_kp(trange=['2014-01-01', '2014-01-02'], gfz=True)
        self.assertTrue('Kp' in kp_vars)
        self.assertTrue('ap' in kp_vars)
        self.assertTrue('Sol_Rot_Num' in kp_vars)
        self.assertTrue('Sol_Rot_Day' in kp_vars)
        self.assertTrue('Kp_Sum' in kp_vars)
        self.assertTrue('ap_Mean' in kp_vars)
        self.assertTrue('Cp' in kp_vars)
        self.assertTrue('C9' in kp_vars)
        self.assertTrue(data_exists('Kp'))
        self.assertTrue(data_exists('ap'))
        self.assertTrue(data_exists('Sol_Rot_Num'))
        self.assertTrue(data_exists('Sol_Rot_Day'))
        self.assertTrue(data_exists('Kp_Sum'))
        self.assertTrue(data_exists('ap_Mean'))
        self.assertTrue(data_exists('Cp'))
        self.assertTrue(data_exists('C9'))


if __name__ == "__main__":
    unittest.main()
