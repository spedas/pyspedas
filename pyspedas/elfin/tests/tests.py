import os
import unittest
from pyspedas.utilities.data_exists import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_fgm_data(self):
        out_vars = pyspedas.elfin.fgm(time_clip=True)
        self.assertTrue(data_exists('ela_fgs'))

    def test_load_epd_data(self):
        out_vars = pyspedas.elfin.epd()
        self.assertTrue(data_exists('ela_pef'))

    def test_load_mrma_data(self):
        out_vars = pyspedas.elfin.mrma()
        self.assertTrue(data_exists('ela_mrma'))

    def test_load_mrmi_data(self):
        out_vars = pyspedas.elfin.mrmi()
        self.assertTrue(data_exists('ela_mrmi'))

    def test_load_state_data(self):
        out_vars = pyspedas.elfin.state()
        self.assertTrue(data_exists('ela_pos_gei'))
        self.assertTrue(data_exists('ela_vel_gei'))

    def test_load_eng_data(self):
        out_vars = pyspedas.elfin.eng()
        self.assertTrue(data_exists('ela_fc_idpu_temp'))

    def test_load_notplot(self):
        out_vars = pyspedas.elfin.epd(notplot=True)
        self.assertTrue('ela_pef' in out_vars)

    def test_downloadonly(self):
        files = pyspedas.elfin.epd(downloadonly=True, trange=['2020-11-01', '2020-11-02'])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()

    