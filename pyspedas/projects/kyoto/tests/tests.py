import unittest
import pyspedas
from pytplot import data_exists, del_data, get_data, tplot_names
import numpy as np



class LoadTestCases(unittest.TestCase):
    def test_load_dst_data(self):
        # final
        del_data('*')
        dst_vars = pyspedas.projects.kyoto.dst(trange=["2015-10-15", "2015-10-16"])
        self.assertTrue(data_exists("kyoto_dst"))
        # provisional
        del_data('*')
        dst_vars = pyspedas.projects.kyoto.dst(trange=["2019-10-15", "2019-10-16"])
        self.assertTrue(data_exists("kyoto_dst"))
        # real time
        del_data('*')
        dst_vars = pyspedas.projects.kyoto.dst(trange=["2022-07-15", "2022-07-16"])
        self.assertTrue(data_exists("kyoto_dst"))

    def test_load_ae_data(self):
        # final
        del_data('*')
        ae_vars = pyspedas.projects.kyoto.load_ae(trange=["2015-10-15", "2015-10-16"], datatypes=["ae", "al", "ao", "au", "ax"])
        self.assertTrue(data_exists("kyoto_ae"))
        self.assertTrue(data_exists("kyoto_al"))
        self.assertTrue(data_exists("kyoto_ao"))
        self.assertTrue(data_exists("kyoto_au"))
        self.assertTrue(data_exists("kyoto_ax"))
        # provisional
        del_data('*')
        ae_vars = pyspedas.projects.kyoto.load_ae(trange=["2019-10-15", "2019-10-16"], datatypes=["ae", "al", "ao", "au", "ax"])
        self.assertTrue(data_exists("kyoto_ae"))
        self.assertTrue(data_exists("kyoto_al"))
        self.assertTrue(data_exists("kyoto_ao"))
        self.assertTrue(data_exists("kyoto_au"))
        self.assertTrue(data_exists("kyoto_ax"))


    def test_load_dst_3digit(self):
        # Test a time interval with 3-digit Dst values, which can run together in the data file
        del_data('*')
        dst_vars = pyspedas.projects.kyoto.dst(trange=["2015-03-16", "2015-03-19"])
        self.assertTrue(data_exists("kyoto_dst"))
        kd = get_data("kyoto_dst")
        dst_min=np.min(kd.y)
        self.assertTrue(dst_min < -100.0)

    def test_load_geomagnetic_indices(self):
        del_data('*')
        geom_ind_vars = pyspedas.projects.kyoto.load_geomagnetic_indices(trange=["2015-03-16", "2015-03-19"])
        self.assertTrue(data_exists("kyoto_ae"))
        self.assertTrue(data_exists("thg_idx_al"))
        self.assertTrue(data_exists("noaa_Kp"))
        self.assertTrue(data_exists("gfz_Kp"))
        self.assertTrue(data_exists("omni_Pressure"))
        self.assertTrue("kyoto_ae" in geom_ind_vars)
        self.assertTrue("thg_idx_al" in geom_ind_vars)
        self.assertTrue("noaa_Kp" in geom_ind_vars)
        self.assertTrue("gfz_Kp" in geom_ind_vars)
        self.assertTrue("omni_Pressure" in geom_ind_vars)

    def test_load_geomagnetic_indices_omni_load_all(self):
        del_data('*')
        geom_ind_vars = pyspedas.projects.kyoto.load_geomagnetic_indices(missions=["omni"], omni_load_all=True,trange=["2015-03-16", "2015-03-19"])
        self.assertTrue(data_exists("omni_BY_GSE"))
        self.assertTrue("omni_BY_GSE" in geom_ind_vars)

    def test_load_geomagnetic_indices_datatype(self):
        del_data('*')
        geom_ind_vars = pyspedas.projects.kyoto.load_geomagnetic_indices(trange=["2015-03-16", "2015-03-19"], datatypes=['dst'])
        self.assertTrue(data_exists("kyoto_dst"))
        self.assertTrue("kyoto_dst" in geom_ind_vars)

    def test_errors(self):
        pyspedas.projects.kyoto.dst(trange=None)
        pyspedas.projects.kyoto.dst(trange=["1015-10-15", "1015-10-16"])
        pyspedas.projects.kyoto.load_ae(trange=None)
        pyspedas.projects.kyoto.load_ae(trange=["1015-10-15", "1015-10-16"])


if __name__ == "__main__":
    unittest.main()
