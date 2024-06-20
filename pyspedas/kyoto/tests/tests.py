import unittest
import pyspedas
from pytplot import data_exists, del_data, get_data
import numpy as np



class LoadTestCases(unittest.TestCase):
    def test_load_dst_data(self):
        # final
        del_data('*')
        dst_vars = pyspedas.kyoto.dst(trange=["2015-10-15", "2015-10-16"])
        self.assertTrue(data_exists("kyoto_dst"))
        # provisional
        del_data('*')
        dst_vars = pyspedas.kyoto.dst(trange=["2019-10-15", "2019-10-16"])
        self.assertTrue(data_exists("kyoto_dst"))
        # real time
        del_data('*')
        dst_vars = pyspedas.kyoto.dst(trange=["2022-07-15", "2022-07-16"])
        self.assertTrue(data_exists("kyoto_dst"))

    def test_load_ae_data(self):
        # final
        del_data('*')
        ae_vars = pyspedas.kyoto.load_ae(trange=["2015-10-15", "2015-10-16"], datatypes=["ae", "al", "ao", "au", "ax"])
        self.assertTrue(data_exists("kyoto_ae"))
        self.assertTrue(data_exists("kyoto_al"))
        self.assertTrue(data_exists("kyoto_ao"))
        self.assertTrue(data_exists("kyoto_au"))
        self.assertTrue(data_exists("kyoto_ax"))
        # provisional
        del_data('*')
        ae_vars = pyspedas.kyoto.load_ae(trange=["2019-10-15", "2019-10-16"], datatypes=["ae", "al", "ao", "au", "ax"])
        self.assertTrue(data_exists("kyoto_ae"))
        self.assertTrue(data_exists("kyoto_al"))
        self.assertTrue(data_exists("kyoto_ao"))
        self.assertTrue(data_exists("kyoto_au"))
        self.assertTrue(data_exists("kyoto_ax"))


    def test_load_dst_3digit(self):
        # Test a time interval with 3-digit Dst values, which can run together in the data file
        del_data('*')
        dst_vars = pyspedas.kyoto.dst(trange=["2015-03-16", "2015-03-19"])
        self.assertTrue(data_exists("kyoto_dst"))
        kd = get_data("kyoto_dst")
        dst_min=np.min(kd.y)
        self.assertTrue(dst_min < -100.0)


    def test_errors(self):
        pyspedas.kyoto.dst(trange=None)
        pyspedas.kyoto.dst(trange=["1015-10-15", "1015-10-16"])
        pyspedas.kyoto.load_ae(trange=None)
        pyspedas.kyoto.load_ae(trange=["1015-10-15", "1015-10-16"])


if __name__ == "__main__":
    unittest.main()
