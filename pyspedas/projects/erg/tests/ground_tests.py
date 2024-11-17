
import os
import unittest
from pytplot import data_exists, del_data, tplot_names

import pyspedas

class LoadTestCases(unittest.TestCase):
    def test_camera_omti_asi_data(self):
        del_data()
        omti_vars = pyspedas.projects.erg.camera_omti_asi(site='ath', trange=['2020-01-20', '2020-01-21'])
        self.assertTrue(data_exists('omti_asi_ath_5577_image_raw'))
        self.assertTrue('omti_asi_ath_5577_image_raw' in omti_vars)

    def test_load_isee_fluxgate_data(self):
        del_data()
        fg_vars = pyspedas.projects.erg.gmag_isee_fluxgate(trange=['2020-08-01/00:00:00','2020-08-01/02:00:00'], site='lcl')
        self.assertTrue(data_exists('isee_fluxgate_mag_lcl_64hz_hdz'))
        self.assertTrue('isee_fluxgate_mag_lcl_64hz_hdz' in fg_vars)

    def test_load_stel_fluxgate_data(self):
        del_data()
        fg_vars = pyspedas.projects.erg.gmag_stel_fluxgate(trange=['2020-08-01/00:00:00','2020-08-01/02:00:00'], site='lcl')
        self.assertTrue(data_exists('isee_fluxgate_mag_lcl_64hz_hdz'))
        self.assertTrue('isee_fluxgate_mag_lcl_64hz_hdz' in fg_vars)

    def test_load_isee_induction_data(self):
        del_data()
        ind_vars = pyspedas.projects.erg.gmag_isee_induction(trange=['2020-08-01/00:00:00', '2020-08-01/02:00:00'], site='msr')
        self.assertTrue(data_exists('isee_induction_db_dt_msr'))
        self.assertTrue('isee_induction_db_dt_msr' in ind_vars)

    def test_load_isee_induction_frequency_dependent_data(self):
        del_data()
        ind_vars = pyspedas.projects.erg.gmag_isee_induction(trange=['2020-08-01/00:00:00', '2020-08-01/02:00:00'], site='msr', frequency_dependent=True)
        self.assertTrue(type(ind_vars) == dict)
        self.assertTrue('msr' in ind_vars)

    def test_load_stel_induction_data(self):
        del_data()
        ind_vars = pyspedas.projects.erg.gmag_stel_induction(trange=['2020-08-01/00:00:00', '2020-08-01/02:00:00'], site='msr')
        self.assertTrue(data_exists('isee_induction_db_dt_msr'))
        self.assertTrue('isee_induction_db_dt_msr' in ind_vars)

    def test_load_magdas_1sec_data(self):
        del_data()
        magdas_vars = pyspedas.projects.erg.gmag_magdas_1sec(trange=["2010-01-01/00:00:00", "2010-01-01:02:00:00"], site='ama')
        self.assertTrue(data_exists('magdas_mag_ama_1sec_hdz'))
        self.assertTrue('magdas_mag_ama_1sec_hdz' in magdas_vars)

    def test_load_mm210_data(self):
        del_data()
        mm210_vars = pyspedas.projects.erg.gmag_mm210(trange=["2005-01-01", "2005-01-02"], site='adl', datatype='1min')
        self.assertTrue(data_exists('mm210_mag_adl_1min_hdz'))
        self.assertTrue('mm210_mag_adl_1min_hdz' in mm210_vars)

    def test_load_sd_fit_data(self):
        del_data()
        sd_vars = pyspedas.projects.erg.sd_fit(trange=['2018-10-14/00:00:00', '2018-10-14/02:00:00'], site='ade')
        self.assertTrue(data_exists('sd_ade_azim_no_5'))
        self.assertTrue('sd_ade_azim_no_5' in sd_vars)

    def test_load_isee_brio_data(self):
        del_data()
        brio_vars = pyspedas.projects.erg.isee_brio(trange=['2020-08-01', '2020-08-02'], site='ath')
        self.assertTrue(data_exists('isee_brio30_ath_64hz_cna'))
        self.assertTrue('isee_brio30_ath_64hz_cna' in brio_vars)

    def test_load_isee_vlf_data(self):
        del_data()
        vlf_vars = pyspedas.projects.erg.isee_vlf(trange=['2017-03-30/12:00:00', '2017-03-30/15:00:00'], site='ath')
        self.assertTrue(data_exists('isee_vlf_ath_ch1'))
        self.assertTrue('isee_vlf_ath_ch1' in vlf_vars)

    def test_load_isee_vlf_cal_gain_data(self):
        del_data()
        vlf_vars = pyspedas.projects.erg.isee_vlf(trange=['2017-03-30/12:00:00', '2017-03-30/15:00:00'], site='ath',  cal_gain=True)
        self.assertTrue(data_exists('isee_vlf_ath_ch1'))
        self.assertTrue('isee_vlf_ath_ch1' in vlf_vars)


if __name__ == '__main__':
    unittest.main()