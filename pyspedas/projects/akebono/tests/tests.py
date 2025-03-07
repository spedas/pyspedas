import os
import unittest
from pytplot import data_exists
import pyspedas
import time

sleep_time = 5

class LoadTestCases(unittest.TestCase):
    def test_load_pws_data(self):
        out_vars = pyspedas.projects.akebono.pws(time_clip=True)
        self.assertTrue(data_exists('akb_pws_RX1'))
        self.assertTrue(data_exists('akb_pws_RX2'))
        time.sleep(sleep_time)


    def test_load_pws_data_prefix_none(self):
        out_vars = pyspedas.projects.akebono.pws(prefix=None)
        self.assertTrue(data_exists('akb_pws_RX1'))
        self.assertTrue(data_exists('akb_pws_RX2'))
        time.sleep(sleep_time)

    def test_load_pws_data_suffix_none(self):
        out_vars = pyspedas.projects.akebono.pws(suffix=None)
        self.assertTrue(data_exists('akb_pws_RX1'))
        self.assertTrue(data_exists('akb_pws_RX2'))
        time.sleep(sleep_time)

    def test_load_pws_data_prefix_suffix(self):
        out_vars = pyspedas.projects.akebono.pws(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_akb_pws_RX1_suf'))
        self.assertTrue(data_exists('pre_akb_pws_RX2_suf'))
        time.sleep(sleep_time)

    def test_load_rdm_data(self):
        out_vars = pyspedas.projects.akebono.rdm()
        self.assertTrue(data_exists('akb_L'))
        self.assertTrue(data_exists('akb_MLT'))
        self.assertTrue(data_exists('akb_rdm_FEIO'))
        time.sleep(sleep_time)

    def test_load_rdm_data_prefix_none(self):
        out_vars = pyspedas.projects.akebono.rdm(prefix=None)
        self.assertTrue(data_exists('akb_L'))
        self.assertTrue(data_exists('akb_MLT'))
        self.assertTrue(data_exists('akb_rdm_FEIO'))
        time.sleep(sleep_time)

    def test_load_rdm_data_suffix_none(self):
        out_vars = pyspedas.projects.akebono.rdm(suffix=None)
        self.assertTrue(data_exists('akb_L'))
        self.assertTrue(data_exists('akb_MLT'))
        self.assertTrue(data_exists('akb_rdm_FEIO'))
        time.sleep(sleep_time)

    def test_load_rdm_data_prefix_suffix(self):
        out_vars = pyspedas.projects.akebono.rdm(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_akb_L_suf'))
        self.assertTrue(data_exists('pre_akb_MLT_suf'))
        self.assertTrue(data_exists('pre_akb_rdm_FEIO_suf'))
        time.sleep(sleep_time)

    def test_load_orb_data(self):
        out_vars = pyspedas.projects.akebono.orb()
        self.assertTrue(data_exists('akb_orb_geo'))
        self.assertTrue(data_exists('akb_orb_gdlat'))
        self.assertTrue(data_exists('akb_orb_gdlon'))
        time.sleep(sleep_time)

    def test_load_orb_prefix_none(self):
        out_vars = pyspedas.projects.akebono.orb(prefix=None)
        self.assertTrue(data_exists('akb_orb_geo'))
        self.assertTrue(data_exists('akb_orb_gdlat'))
        self.assertTrue(data_exists('akb_orb_gdlon'))
        time.sleep(sleep_time)

    def test_load_orb_suffix_none(self):
        out_vars = pyspedas.projects.akebono.orb(suffix=None)
        self.assertTrue(data_exists('akb_orb_geo'))
        self.assertTrue(data_exists('akb_orb_gdlat'))
        self.assertTrue(data_exists('akb_orb_gdlon'))
        time.sleep(sleep_time)

    def test_load_orb_prefix_suffix(self):
        out_vars = pyspedas.projects.akebono.orb(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_akb_orb_geo_suf'))
        self.assertTrue(data_exists('pre_akb_orb_gdlat_suf'))
        self.assertTrue(data_exists('pre_akb_orb_gdlon_suf'))
        time.sleep(sleep_time)

    def test_load_notplot(self):
        out_vars = pyspedas.projects.akebono.pws(notplot=True)
        self.assertTrue('akb_pws_RX1' in out_vars)
        time.sleep(sleep_time)

    def test_downloadonly(self):
        files = pyspedas.projects.akebono.pws(downloadonly=True, trange=['2012-10-01', '2012-10-02'])
        self.assertTrue(os.path.exists(files[0]))
        time.sleep(sleep_time)


if __name__ == '__main__':
    unittest.main()

    