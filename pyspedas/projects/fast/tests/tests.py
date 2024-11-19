import os
import unittest
from pytplot import data_exists, del_data
import pyspedas


class Fast_Tests(unittest.TestCase):
    def test_downloadonly(self):
        files = pyspedas.projects.fast.acf(
            trange=["1999-09-22", "1999-09-23"],
            time_clip=True,
            level="k0",
            downloadonly=True,
        )
        self.assertTrue(os.path.exists(files[0]))

    def test_load_dcf_data(self):
        dcf_vars = pyspedas.projects.fast.dcf(trange=["1999-09-22", "1999-09-23"], level="k0")
        self.assertTrue(data_exists("fast_dcf_BX"))
        self.assertTrue(data_exists("fast_dcf_BY"))
        self.assertTrue(data_exists("fast_dcf_BZ"))
        self.assertTrue("fast_dcf_BZ" in dcf_vars)

    def test_load_dcf_data_l2(self):
        dcf_vars = pyspedas.projects.fast.dcf(trange=["1998-09-22", "1998-09-23"], level="l2")
        self.assertTrue(data_exists("fast_dcf_DeltaB_GEI"))
        self.assertTrue("fast_dcf_DeltaB_GEI" in dcf_vars)

    def test_load_acf_data(self):
        dcf_vars = pyspedas.projects.fast.acf(
            trange=["1999-09-22", "1999-09-23"], time_clip=True, level="k0"
        )
        self.assertTrue(data_exists("fast_acf_HF_PWR"))
        self.assertTrue(data_exists("fast_acf_HF_E_SPEC"))
        self.assertTrue("fast_acf_HF_E_SPEC" in dcf_vars)

    def test_load_esa_data(self):
        esa_vars = pyspedas.projects.fast.esa(
            notplot=True, trange=["1998-09-05/02:00", "1998-09-05/02:30"]
        )
        self.assertTrue("fast_esa_eflux" in esa_vars)

    def test_load_teams_data(self):
        teams_vars = pyspedas.projects.fast.teams(
            trange=["1998-09-05", "1998-09-06"], level="k0"
        )
        self.assertTrue(data_exists("fast_teams_H+"))
        self.assertTrue(data_exists("fast_teams_O+"))
        self.assertTrue(data_exists("fast_teams_He+"))
        self.assertTrue("fast_teams_fa_spin_dec" in teams_vars)

    def test_load_teams_data_l2(self):
        teams_vars = pyspedas.projects.fast.teams(
            trange=["2004-06-01", "2004-06-02"], level="l2"
        )
        self.assertTrue(data_exists("fast_teams_proton_distribution"))
        self.assertTrue("fast_teams_helium_distribution" in teams_vars)

    def test_load_invalid_trange(self):
        del_data()
        t_all = pyspedas.projects.fast.load(trange="bad input")
        self.assertTrue(len(t_all) == 0)
        del_data()
        t_all = pyspedas.projects.fast.load(trange=["2018-12-15"])
        self.assertTrue(len(t_all) == 0)
        del_data()
        t_all = pyspedas.projects.fast.load(trange=["2018-12-15", "2018-12-14"])
        self.assertTrue(len(t_all) == 0)

    def test_load_invalid_instrument(self):
        t_all = pyspedas.projects.fast.load(instrument="bad input")
        self.assertTrue(len(t_all) == 0)


if __name__ == "__main__":
    unittest.main()
