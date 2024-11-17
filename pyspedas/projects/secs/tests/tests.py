import unittest
from unittest.mock import patch
import pyspedas
from pyspedas.projects.secs.makeplots import make_plots
from pytplot import del_data
from pyspedas.projects.secs.config import CONFIG


class SECSTestCases(unittest.TestCase):
    @patch("matplotlib.pyplot.show")
    def test_load_secs(self, mock_show):
        del_data()
        trange = ["2017-03-27", "2017-03-28"]
        d = pyspedas.projects.secs.data(
            trange=trange,
            resolution=10,
            dtype="SECS",
            no_download=False,
            downloadonly=True,
            out_type="df",
            spdf=True,
            force_download=True,
        )
        # Returns a Pandas dataframe, not tplot variables
        self.assertTrue(len(d) > 0)
        make_plots(
            dtype="SECS",
            dtime="2017-03-27/06:00:00",
            vplot_sized=True,
            contour_den=201,
            s_loc=False,
            quiver_scale=30,
        )

    @patch("matplotlib.pyplot.show")
    def test_load_eics(self, mock_show):
        del_data()
        trange = ["2017-03-27", "2017-03-28"]
        d = pyspedas.projects.secs.data(
            trange=trange,
            resolution=10,
            dtype="EICS",
            no_download=False,
            downloadonly=False,
            out_type="df",
            spdf=True,
            force_download=True,
        )
        # Returns a Pandas dataframe, not tplot variables
        self.assertTrue(len(d) > 0)
        make_plots(
            dtype="EICS",
            dtime="2017-03-27/06:00:00",
            vplot_sized=True,
            contour_den=201,
            s_loc=False,
            quiver_scale=30,
        )

    def test_load_secs_dc(self):
        trange = ["2017-03-27", "2017-03-28"]
        del_data()
        d = pyspedas.projects.secs.data(
            trange=trange,
            resolution=10,
            dtype="SECS",
            no_download=False,
            downloadonly=False,
            out_type="dc",
        )
        # Returns a Pandas dataframe, not tplot variables
        self.assertTrue(len(d) > 0)

    def test_load_eics_dc(self):
        del_data()
        trange = ["2017-03-27", "2017-03-28"]
        d = pyspedas.projects.secs.data(
            trange=trange,
            resolution=10,
            dtype="EICS",
            no_download=False,
            downloadonly=False,
            out_type="dc",
        )
        # Returns a Pandas dataframe, not tplot variables
        self.assertTrue(len(d) > 0)

    def test_load_secs_np(self):
        del_data()
        trange = ["2017-03-27", "2017-03-28"]
        d = pyspedas.projects.secs.data(
            trange=trange,
            resolution=10,
            dtype="SECS",
            no_download=False,
            downloadonly=False,
            out_type="np",
        )
        # Returns a Pandas dataframe, not tplot variables
        self.assertTrue(len(d) > 0)

    def test_load_eics_np(self):
        del_data()
        trange = ["2017-03-27", "2017-03-28"]
        d = pyspedas.projects.secs.data(
            trange=trange,
            resolution=10,
            dtype="EICS",
            no_download=False,
            downloadonly=False,
            out_type="np",
        )
        # Returns a Pandas dataframe, not tplot variables
        self.assertTrue(len(d) > 0)

    def test_load_gz(self):
        # A few dates in 2007 have .gz files (instead of .zip files)
        # This only happens for the UCLA data, not the SPDF data
        del_data()
        dtype = "EICS"  # 'EICS or SECS'
        trange = ["2007-02-09/02:15:35", "2007-02-09/02:15:35"]
        d = pyspedas.projects.secs.data(
            trange=trange,
            dtype=dtype,
            downloadonly=True,
        )
        self.assertTrue(len(d) > 0)

    def test_none_cases(self):
        # No data type provided
        del_data()
        trange = ["2017-03-27", "2017-03-28"]
        d = pyspedas.projects.secs.data(
            trange=trange,
            dtype=None,
        )
        self.assertTrue(d is None)

        # Wrong data type provided
        del_data()
        trange = ["2017-03-27", "2017-03-28"]
        d = pyspedas.projects.secs.data(
            trange=trange,
            dtype="aaa",
        )
        self.assertTrue(d is None)

        # Invalid time range provided
        del_data()
        trange = ["2018-03-27", "2017-03-28"]
        d = pyspedas.projects.secs.data(
            trange=trange,
            dtype="dc",
        )
        self.assertTrue(d is None)

        # Invalid out type provided
        trange = ["2017-03-27", "2017-03-28"]
        d = pyspedas.projects.secs.data(
            trange=trange,
            dtype="dc",
            out_type="aaa",
        )
        self.assertTrue(d is None)


if __name__ == "__main__":
    unittest.main()
