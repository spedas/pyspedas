import os
import unittest

from pyspedas import data_exists, del_data, tplot
from pyspedas.projects.juno.config import CONFIG
from pyspedas.projects.juno.load import get_info, load

global_display = False
outputdir = os.path.join(CONFIG["local_data_dir"], "idltestfiles")


class LoadTestCases(unittest.TestCase):
    def test_load_jovicentric_data(self):
        del_data()
        trange = ["2020-02-02 12:00:00", "2020-02-02 14:00:00"]
        datatype = "jovicentric"
        vars = load(trange=trange, datatype=datatype)
        self.assertTrue("jovicentric_mlat" in vars)
        self.assertTrue(data_exists("jovicentric_mlt"))

        # Test tplot display and save_png functionality
        # If outputdir does not exist, create it
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)
        local_png = os.path.join(outputdir, "juno_jovicentric_2020-02-02.png")
        tplot(
            vars,
            display=global_display,
            save_png=local_png,
        )

    def test_load_params_data(self):
        del_data()
        trange = ["2020-02-02 12:00:00", "2020-02-02 14:00:00"]
        datatype = "jovicentric"
        params = "JLAT CLAT JULT"
        vars = load(trange=trange, datatype=datatype, params=params)
        print(vars)
        self.assertTrue("jovicentric_clat" in vars)
        self.assertTrue(data_exists("jovicentric_clat"))

    def test_get_info(self):
        info = get_info(datatype="mag")
        self.assertTrue(isinstance(info, str))
        self.assertTrue(len(info) > 0)

    def test_load_invalid_datatype(self):
        del_data()
        trange = ["2020-02-02 12:00:00", "2020-02-02 14:00:00"]
        datatype = "invalid_datatype"
        with self.assertRaises(ValueError):
            load(trange=trange, datatype=datatype)

    def test_load_invalid_trange(self):
        del_data()
        trange = ["2020-02-02 14:00:00", "2020-02-02 12:00:00"]  # Invalid trange (start > end)
        datatype = "magnitude"
        with self.assertRaises(ValueError):
            load(trange=trange, datatype=datatype)

        trange = ["2020-02-02 12:00:00"]  # Invalid trange (only one time)
        with self.assertRaises(ValueError):
            load(trange=trange, datatype=datatype)

        trange = "2020-02-02 12:00:00"  # Invalid trange (not a list)
        with self.assertRaises(TypeError):
            load(trange=trange, datatype=datatype)

        trange = ["2020-02-01 12:00:00", "2020-02-04 12:00:00"]  # Invalid trange (more than 2 days)
        with self.assertRaises(ValueError):
            load(trange=trange, datatype=datatype)


if __name__ == "__main__":
    unittest.main()
