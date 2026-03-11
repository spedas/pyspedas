import unittest
from pyspedas import kompsat_load
from pyspedas.tplot_tools import data_exists
from pyspedas.projects.kompsat.esa_hapi_data import check_esa_hapi_connection


class Kompsat_Tests(unittest.TestCase):
    def test_server_connection(self):
        # Test connection to ESA HAPI server
        self.assertTrue(check_esa_hapi_connection())

    def test_mag(self):
        # Test SOSMAG recalibrated L2 data
        var_names = kompsat_load(trange=["2026-01-01 02:00", "2026-01-01 03:00"])
        self.assertTrue(data_exists("sosmag_b_gse"))
        self.assertTrue("sosmag_position" in var_names)

    def test_1m_get_support_data(self):
        # Test SOSMAG 1-minute data
        var_names = kompsat_load(trange=["2026-01-01 02:00", "2026-01-01 03:00"], datatype="1m")
        self.assertTrue(data_exists("sosmag_1m_b_gse"))
        self.assertTrue(data_exists("sosmag_1m_position"))
        self.assertTrue("sosmag_1m_b_gse" in var_names)
        self.assertTrue(data_exists("sosmag_1m_data_flags"))
        self.assertTrue("sosmag_1m_data_flags" in var_names)

    def test_p(self):
        # Test KSEM proton data
        var_names = kompsat_load(trange=["2026-01-01 02:00", "2026-01-01 03:00"], datatype="p")
        self.assertTrue(data_exists("kompsat_p_p1"))
        self.assertTrue(data_exists("kompsat_p_p8"))
        self.assertTrue("kompsat_p_p5" in var_names)

    def test_e(self):
        # Test KSEM electron data
        var_names = kompsat_load(trange=["2026-01-01 02:00", "2026-01-01 03:00"], datatype="e")
        self.assertTrue(data_exists("kompsat_e_e1"))
        self.assertTrue(data_exists("kompsat_e_e10_qef"))
        self.assertTrue("kompsat_e_e6" in var_names)


if __name__ == "__main__":
    unittest.main()
