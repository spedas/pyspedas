import unittest
from pyspedas import kompsat_load
from pytplot import data_exists


class Kompsat_Tests(unittest.TestCase):
    def test_mag(self):
        var_names = kompsat_load(trange=["2021-01-01 02:00", "2021-01-01 03:00"])
        self.assertTrue(data_exists("sosmag_b_gse"))
        self.assertTrue("sosmag_position" in var_names)

    def test_1m(self):
        var_names = kompsat_load(
            datatype="1m", trange=["2021-01-01 02:00", "2021-01-01 03:00"]
        )
        self.assertTrue(data_exists("sosmag_1m_b_gse"))
        self.assertTrue(data_exists("sosmag_1m_position"))
        self.assertTrue("sosmag_1m_b_gse" in var_names)

    def test_1m_get_support_data(self):
        var_names = kompsat_load(
            datatype="1m", trange=["2021-01-01 02:00", "2021-01-01 03:00"], get_support_data=True
        )
        self.assertTrue(data_exists("sosmag_1m_b_gse"))
        self.assertTrue(data_exists("sosmag_1m_position"))
        self.assertTrue("sosmag_1m_b_gse" in var_names)
        self.assertTrue(data_exists("sosmag_1m_data_flags"))
        self.assertTrue("sosmag_1m_data_flags" in var_names)

    def test_p(self):
        var_names = kompsat_load(
            instrument="p", trange=["2024-04-01 02:00", "2024-04-01 03:00"]
        )
        self.assertTrue(data_exists("kompsat_p_p1"))
        self.assertTrue(data_exists("kompsat_p_p8"))
        self.assertTrue("kompsat_p_p5" in var_names)

    def test_e(self):
        var_names = kompsat_load(
            instrument="e",
            trange=["2024-04-01 02:00", "2024-04-01 03:00"],
            get_support_data=True,
        )
        self.assertTrue(data_exists("kompsat_e_e1"))
        self.assertTrue(data_exists("kompsat_e_e10_qef"))
        self.assertTrue("kompsat_e_e6" in var_names)


if __name__ == "__main__":
    unittest.main()
