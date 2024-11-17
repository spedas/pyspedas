import os
import unittest
from pytplot import data_exists, del_data
import pyspedas


class Dscovr_LoadTestCases(unittest.TestCase):
    def test_load_mag_data(self):
        del_data()
        mag_vars = pyspedas.projects.dscovr.mag(time_clip=True)
        self.assertTrue(data_exists("dsc_h0_mag_B1RTN"))
        self.assertTrue(data_exists("dsc_h0_mag_B1GSE"))

    def test_load_mag_notplot(self):
        del_data()
        mag_vars = pyspedas.projects.dscovr.mag(notplot=True)
        self.assertTrue("dsc_h0_mag_B1GSE" in mag_vars)

    def test_load_fc_data(self):
        del_data()
        fc_vars = pyspedas.projects.dscovr.fc()
        self.assertTrue(data_exists("dsc_h1_fc_Np"))
        self.assertTrue(data_exists("dsc_h1_fc_THERMAL_TEMP"))

    def test_load_orb_data(self):
        del_data()
        orb_vars = pyspedas.projects.dscovr.orb()
        self.assertTrue(data_exists("dsc_orbit_GSE_POS"))
        self.assertTrue(data_exists("dsc_orbit_GCI_POS"))

    def test_load_att_data(self):
        del_data()
        att_vars = pyspedas.projects.dscovr.att()
        self.assertTrue(data_exists("dsc_att_GCI_Yaw"))
        self.assertTrue(data_exists("dsc_att_GCI_Pitch"))
        self.assertTrue(data_exists("dsc_att_GCI_Roll"))

    def test_load_pre_at_data(self):
        del_data()
        pre_at_vars = pyspedas.projects.dscovr.load(
            instrument="pre_at", trange=["2016-01-15", "2016-01-16"], prefix="prevdata_"
        )
        self.assertTrue(data_exists("prevdata_dsc_at_pre_J2000_Yaw"))
        self.assertTrue(data_exists("prevdata_dsc_at_pre_J2000_Pitch"))

    def test_load_downloadonly(self):
        del_data()
        files = pyspedas.projects.dscovr.mag(
            downloadonly=True, trange=["2018-12-15", "2018-12-16"]
        )
        self.assertTrue(os.path.exists(files[0]))

    def test_load_all(self):
        del_data()
        t_all = pyspedas.projects.dscovr.all()
        self.assertTrue(len(t_all) > 0)

    def test_load_invalid_trange(self):
        del_data()
        t_all = pyspedas.projects.dscovr.all(trange="bad input")
        self.assertTrue(len(t_all) == 0)
        del_data()
        t_all = pyspedas.projects.dscovr.all(trange=["2018-12-15"])
        self.assertTrue(len(t_all) == 0)
        del_data()
        t_all = pyspedas.projects.dscovr.all(trange=["2018-12-15", "2018-12-14"])
        self.assertTrue(len(t_all) == 0)

    def test_load_invalid_instrument(self):
        del_data()
        t_all = pyspedas.projects.dscovr.all(instrument="bad input")
        self.assertTrue(len(t_all) == 0)


if __name__ == "__main__":
    unittest.main()
