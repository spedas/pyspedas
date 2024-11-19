import os
import unittest
from pytplot import data_exists, del_data
import pyspedas


class LoadTestCases(unittest.TestCase):
    def test_load_mag_data(self):
        del_data()
        out_vars = pyspedas.projects.de2.mag(time_clip=True)
        self.assertTrue(data_exists("bx"))
        self.assertTrue(data_exists("by"))
        self.assertTrue(data_exists("bz"))

    def test_load_nacs_data(self):

        del_data()
        out_vars = pyspedas.projects.de2.nacs(force_download=True)
        self.assertTrue(data_exists("O_density"))
        self.assertTrue(data_exists("N_density"))

    def test_load_rpa_data(self):
        del_data()
        out_vars = pyspedas.projects.de2.rpa(prefix="de2_")
        self.assertTrue(data_exists("de2_ionDensity"))
        self.assertTrue(data_exists("de2_ionTemperature"))

    def test_load_fpi_data(self):
        del_data()
        out_vars = pyspedas.projects.de2.fpi(suffix="_de2", varnames=["TnF"])
        self.assertTrue(data_exists("TnF_de2"))

    # issue with the CDFs here, 2Nov2022
    def test_load_idm_data(self):
        del_data()
        out_vars = pyspedas.projects.de2.idm()
        self.assertTrue(data_exists("ionVelocityY"))
        self.assertTrue(data_exists("ionVelocityZ"))

    def test_load_wats_data(self):
        del_data()
        out_vars = pyspedas.projects.de2.wats()
        self.assertTrue(data_exists("density"))
        self.assertTrue(data_exists("Tn"))

    def test_load_vefi_data(self):
        del_data()
        out_vars = pyspedas.projects.de2.vefi(trange=["1981-12-06", "1981-12-07"])
        self.assertTrue(data_exists("spectA"))
        self.assertTrue(data_exists("spectB"))
        self.assertTrue(data_exists("spectC"))

    def test_load_lang_data(self):
        del_data()
        out_vars = pyspedas.projects.de2.lang(time_clip=True)
        self.assertTrue(data_exists("plasmaDensity"))
        self.assertTrue(data_exists("electronTemp"))

    def test_load_notplot(self):
        del_data()
        out_vars = pyspedas.projects.de2.mag(notplot=True)
        self.assertTrue("bz" in out_vars)

    def test_downloadonly(self):
        del_data()
        files = pyspedas.projects.de2.mag(downloadonly=True, trange=["1983-2-16", "1983-2-17"])
        self.assertTrue(os.path.exists(files[0]))


if __name__ == "__main__":
    unittest.main()
