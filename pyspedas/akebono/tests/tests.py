import os
import unittest
from pytplot import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_pws_data(self):
        out_vars = pyspedas.akebono.pws(time_clip=True)
        self.assertTrue(data_exists('akb_pws_RX1'))
        self.assertTrue(data_exists('akb_pws_RX2'))

    def test_load_pws_data_prefix_none(self):
        out_vars = pyspedas.akebono.pws(prefix=None)
        self.assertTrue(data_exists('akb_pws_RX1'))
        self.assertTrue(data_exists('akb_pws_RX2'))

    def test_load_pws_data_suffix_none(self):
        out_vars = pyspedas.akebono.pws(suffix=None)
        self.assertTrue(data_exists('akb_pws_RX1'))
        self.assertTrue(data_exists('akb_pws_RX2'))

    def test_load_pws_data_prefix_suffix(self):
        out_vars = pyspedas.akebono.pws(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_akb_pws_RX1_suf'))
        self.assertTrue(data_exists('pre_akb_pws_RX2_suf'))

    def test_load_rdm_data(self):
        out_vars = pyspedas.akebono.rdm()
        self.assertTrue(data_exists('akb_L'))
        self.assertTrue(data_exists('akb_MLT'))
        self.assertTrue(data_exists('akb_rdm_FEIO'))

    def test_load_rdm_data_prefix_none(self):
        out_vars = pyspedas.akebono.rdm(prefix=None)
        self.assertTrue(data_exists('akb_L'))
        self.assertTrue(data_exists('akb_MLT'))
        self.assertTrue(data_exists('akb_rdm_FEIO'))

    def test_load_rdm_data_suffix_none(self):
        out_vars = pyspedas.akebono.rdm(suffix=None)
        self.assertTrue(data_exists('akb_L'))
        self.assertTrue(data_exists('akb_MLT'))
        self.assertTrue(data_exists('akb_rdm_FEIO'))

    def test_load_rdm_data_prefix_suffix(self):
        out_vars = pyspedas.akebono.rdm(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_akb_L_suf'))
        self.assertTrue(data_exists('pre_akb_MLT_suf'))
        self.assertTrue(data_exists('pre_akb_rdm_FEIO_suf'))

    def test_load_orb_data(self):
        out_vars = pyspedas.akebono.orb()
        self.assertTrue(data_exists('akb_orb_geo'))
        self.assertTrue(data_exists('akb_orb_gdlat'))
        self.assertTrue(data_exists('akb_orb_gdlon'))

    def test_load_orb_prefix_none(self):
        out_vars = pyspedas.akebono.orb(prefix=None)
        self.assertTrue(data_exists('akb_orb_geo'))
        self.assertTrue(data_exists('akb_orb_gdlat'))
        self.assertTrue(data_exists('akb_orb_gdlon'))

    def test_load_orb_suffix_none(self):
        out_vars = pyspedas.akebono.orb(suffix=None)
        self.assertTrue(data_exists('akb_orb_geo'))
        self.assertTrue(data_exists('akb_orb_gdlat'))
        self.assertTrue(data_exists('akb_orb_gdlon'))

    def test_load_orb_prefix_suffix(self):
        out_vars = pyspedas.akebono.orb(prefix='pre_', suffix='_suf')
        self.assertTrue(data_exists('pre_akb_orb_geo_suf'))
        self.assertTrue(data_exists('pre_akb_orb_gdlat_suf'))
        self.assertTrue(data_exists('pre_akb_orb_gdlon_suf'))

    def test_load_notplot(self):
        out_vars = pyspedas.akebono.pws(notplot=True)
        self.assertTrue('akb_pws_RX1' in out_vars)

    def test_downloadonly(self):
        files = pyspedas.akebono.pws(downloadonly=True, trange=['2012-10-01', '2012-10-02'])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()

    