import unittest

from pyspedas.projects.galileo.load import get_info, load
from pyspedas.tplot_tools import data_exists, del_data


class LoadTestCases(unittest.TestCase):
    def test_load_magnitude_data(self):
        del_data()
        trange = ["1996-06-30 00:00:00", "1996-06-30 01:00:00"]
        datatype = "magnitude"
        vars = load(trange=trange, datatype=datatype)
        self.assertTrue("galileo_b_mag" in vars)
        self.assertTrue(data_exists("galileo_b_mag"))

    def test_load_jovicentric_data(self):
        del_data()
        trange = ["1997-06-30 00:00:00", "1997-06-30 01:00:00"]
        datatype = "jovicentric"
        vars = load(trange=trange, datatype=datatype)
        self.assertTrue("galileo_longitude" in vars)
        self.assertTrue(data_exists("galileo_l"))

    def test_load_fce_data(self):
        del_data()
        trange = ["1997-06-30 00:00:00", "1997-06-30 01:00:00"]
        datatype = "fce"
        vars = load(trange=trange, datatype=datatype)
        print(vars)
        self.assertTrue("galileo_fce" in vars)
        self.assertTrue(data_exists("galileo_fce"))

    def test_get_info(self):
        info = get_info(datatype="fce")
        self.assertTrue(isinstance(info, str))
        self.assertTrue(len(info) > 0)

    def test_load_invalid_datatype(self):
        del_data()
        trange = ["1997-02-02 12:00:00", "1997-02-02 14:00:00"]
        datatype = "invalid_datatype"
        with self.assertRaises(ValueError):
            load(trange=trange, datatype=datatype)

    def test_load_invalid_trange(self):
        del_data()
        trange = ["1997-02-02 14:00:00", "1997-02-02 12:00:00"]  # Invalid trange (start > end)
        datatype = "magnitude"
        with self.assertRaises(ValueError):
            load(trange=trange, datatype=datatype)

        trange = ["1997-02-02 12:00:00"]  # Invalid trange (only one time)
        with self.assertRaises(ValueError):
            load(trange=trange, datatype=datatype)

        trange = "1997-02-02 12:00:00"  # Invalid trange (not a list)
        with self.assertRaises(TypeError):
            load(trange=trange, datatype=datatype)

        trange = ["1997-02-01 12:00:00", "1997-02-04 12:00:00"]  # Invalid trange (more than 2 days)
        with self.assertRaises(ValueError):
            load(trange=trange, datatype=datatype)


if __name__ == "__main__":
    unittest.main()
