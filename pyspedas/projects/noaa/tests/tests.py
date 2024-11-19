import unittest
import pyspedas
from pytplot import data_exists, del_data, get_data
import numpy as np


class LoadTestCases(unittest.TestCase):
    def test_load_kp_data_2024(self):
        # Load data from noaa
        del_data('*')
        kp_vars = pyspedas.projects.noaa.noaa_load_kp(trange=['2024-01-01', '2024-01-02'])
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
        # Load data from noaa
        del_data('*')
        kp_vars = pyspedas.projects.noaa.noaa_load_kp(trange=['2014-01-01', '2014-01-02'], prefix='noaa_', suffix='_test')
        self.assertTrue('noaa_Kp_test' in kp_vars)
        self.assertTrue('noaa_ap_test' in kp_vars)
        self.assertTrue('noaa_Sol_Rot_Num_test' in kp_vars)
        self.assertTrue('noaa_Sol_Rot_Day_test' in kp_vars)
        self.assertTrue('noaa_Kp_Sum_test' in kp_vars)
        self.assertTrue('noaa_ap_Mean_test' in kp_vars)
        self.assertTrue('noaa_Cp_test' in kp_vars)
        self.assertTrue('noaa_C9_test' in kp_vars)
        self.assertTrue('noaa_Sunspot_Number_test' in kp_vars)
        self.assertTrue('noaa_F10.7_test' in kp_vars)
        self.assertTrue('noaa_Flux_Qualifier_test' in kp_vars)
        self.assertTrue(data_exists('noaa_Kp_test'))
        self.assertTrue(data_exists('noaa_ap_test'))
        self.assertTrue(data_exists('noaa_Sol_Rot_Num_test'))
        self.assertTrue(data_exists('noaa_Sol_Rot_Day_test'))
        self.assertTrue(data_exists('noaa_Kp_Sum_test'))
        self.assertTrue(data_exists('noaa_ap_Mean_test'))
        self.assertTrue(data_exists('noaa_Cp_test'))
        self.assertTrue(data_exists('noaa_C9_test'))
        self.assertTrue(data_exists('noaa_Sunspot_Number_test'))
        self.assertTrue(data_exists('noaa_F10.7_test'))
        self.assertTrue(data_exists('noaa_Flux_Qualifier_test'))

    def test_load_kp_data_2014_gfz(self):
        # final
        del_data('*')
        kp_vars = pyspedas.projects.noaa.noaa_load_kp(trange=['2014-01-01', '2014-01-02'], gfz=True)
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

    def test_load_kp_data_2014_gfz_ftp(self):
        # final
        del_data('*')
        kp_vars = pyspedas.projects.noaa.noaa_load_kp(trange=['2014-01-01', '2014-01-02'], gfz=True,gfz_ftp=True)
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
