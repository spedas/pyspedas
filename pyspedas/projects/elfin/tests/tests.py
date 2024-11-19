import os
import unittest
import pyspedas
from pytplot import data_exists, del_data


class LoadTestCases(unittest.TestCase):

    def test_load_fgm_data(self):
        out_vars = pyspedas.projects.elfin.fgm(time_clip=True)
        self.assertTrue(data_exists('ela_fgs'))
        self.assertTrue('ela_fgs' in out_vars)

    def test_load_epd_data(self):
        out_vars = pyspedas.projects.elfin.epd(trange=['2020-11-01', '2020-11-02'])
        self.assertTrue(data_exists('ela_pef_nflux'))
        self.assertTrue('ela_pef_nflux' in out_vars)

    def test_load_mrma_data(self):
        out_vars = pyspedas.projects.elfin.mrma()
        self.assertTrue(data_exists('ela_mrma'))
        self.assertTrue('ela_mrma' in out_vars)

    def test_load_mrmi_data(self):
        out_vars = pyspedas.projects.elfin.mrmi()
        self.assertTrue(data_exists('ela_mrmi'))
        self.assertTrue('ela_mrmi' in out_vars)

    def test_load_state_data(self):
        out_vars = pyspedas.projects.elfin.state()
        self.assertTrue(data_exists('ela_pos_gei'))
        self.assertTrue(data_exists('ela_vel_gei'))
        self.assertTrue('ela_pos_gei' in out_vars)
        self.assertTrue('ela_vel_gei' in out_vars)

    def test_load_eng_data(self):
        out_vars = pyspedas.projects.elfin.eng()
        self.assertTrue(data_exists('ela_fc_idpu_temp'))
        self.assertTrue('ela_fc_idpu_temp' in out_vars)

    def test_load_notplot(self):
        del_data('*')
        out_vars = pyspedas.projects.elfin.epd(notplot=True)
        self.assertTrue('ela_pef' in out_vars)
        self.assertFalse(data_exists('ela_pef'))


    def test_downloadonly(self):
        files = pyspedas.projects.elfin.epd(downloadonly=True, trange=['2020-11-01', '2020-11-02'])
        self.assertTrue(os.path.exists(files[0]))

    def test_load_fgm_data(self):
        out_vars = pyspedas.projects.elfin.fgm()
        self.assertTrue(data_exists('ela_fgs'))
        self.assertTrue('ela_fgs' in out_vars)

    def test_load_mrma_data(self):
        out_vars = pyspedas.projects.elfin.mrma()
        self.assertTrue(data_exists('ela_mrma'))
        self.assertTrue('ela_mrma' in out_vars)

    def test_load_mrmi_data(self):
        out_vars = pyspedas.projects.elfin.mrmi()
        self.assertTrue(data_exists('ela_mrmi'))
        self.assertTrue('ela_mrmi' in out_vars)

if __name__ == '__main__':
    unittest.main()

    