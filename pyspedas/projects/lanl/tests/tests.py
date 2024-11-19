import os
import unittest
from pytplot import data_exists
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_mpa_data(self):
        out_vars = pyspedas.projects.lanl.mpa(time_clip=True)
        self.assertTrue(data_exists("dens_lop"))
        self.assertTrue(data_exists("vel_lop"))
        self.assertTrue(data_exists("temp_lop"))

    def test_load_spa_data(self):
        out_vars = pyspedas.projects.lanl.spa(time_clip=True)
        self.assertTrue(data_exists("spa_p_temp"))
        self.assertTrue(data_exists("spa_e_temp"))
        self.assertTrue(data_exists("spa_a_flux"))
        self.assertTrue(data_exists("spa_e_flx"))
        self.assertTrue(data_exists("spa_p_flx"))

    def test_load_notplot(self):
        out_vars = pyspedas.projects.lanl.spa(notplot=True)
        self.assertTrue("spa_p_temp" in out_vars)

    def test_downloadonly(self):
        files = pyspedas.projects.lanl.spa(
            downloadonly=True, trange=["2004-10-31", "2004-11-01"]
        )
        self.assertTrue(os.path.exists(files[0]))


if __name__ == "__main__":
    unittest.main()
