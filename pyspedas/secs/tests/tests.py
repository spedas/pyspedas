import unittest
from unittest.mock import patch
import pyspedas
from pyspedas.secs.makeplots import make_plots

from pyspedas.secs.config import CONFIG
CONFIG['plots_dir'] = 'dir/'

from pytplot import data_exists, tplot_names, del_data

class SECSTestCases(unittest.TestCase):
    @patch("matplotlib.pyplot.show")
    def test_load_secs(self, mock_show):
        del_data()
        trange = ['2017-03-27', '2017-03-28']
        d = pyspedas.secs.data(trange=trange,
                               resolution=10,
                               dtype='SECS',
                               no_download=False,
                               downloadonly=False,
                               out_type='df')
        # Returns a Pandas dataframe, not tplot variables
        self.assertTrue(len(d) > 0)
        make_plots(dtype='SECS',
                   dtime='2017-03-27/06:00:00',
                   vplot_sized=True,
                   contour_den=201,
                   s_loc=False,
                   quiver_scale=30)

    @patch("matplotlib.pyplot.show")
    def test_load_eics(self, mock_show):
        del_data()
        trange = ['2017-03-27', '2017-03-28']
        d = pyspedas.secs.data(trange=trange,
                               resolution=10,
                               dtype='EICS',
                               no_download=False,
                               downloadonly=False,
                               out_type='df')
        # Returns a Pandas dataframe, not tplot variables
        self.assertTrue(len(d) > 0)
        make_plots(dtype='EICS',
                   dtime='2017-03-27/06:00:00',
                   vplot_sized=True,
                   contour_den=201,
                   s_loc=False,
                   quiver_scale=30)

    def test_load_secs_dc(self):
        trange = ['2017-03-27', '2017-03-28']
        del_data()
        d = pyspedas.secs.data(trange=trange,
                               resolution=10,
                               dtype='SECS',
                               no_download=False,
                               downloadonly=False,
                               out_type='dc')
        # Returns a Pandas dataframe, not tplot variables
        self.assertTrue(len(d) > 0)

    def test_load_eics_dc(self):
        del_data()
        trange = ['2017-03-27', '2017-03-28']
        d = pyspedas.secs.data(trange=trange,
                               resolution=10,
                               dtype='EICS',
                               no_download=False,
                               downloadonly=False,
                               out_type='dc')
        # Returns a Pandas dataframe, not tplot variables
        self.assertTrue(len(d) > 0)

    def test_load_secs_np(self):
        del_data()
        trange = ['2017-03-27', '2017-03-28']
        d = pyspedas.secs.data(trange=trange,
                               resolution=10,
                               dtype='SECS',
                               no_download=False,
                               downloadonly=False,
                               out_type='np')
        # Returns a Pandas dataframe, not tplot variables
        self.assertTrue(len(d) > 0)

    def test_load_eics_np(self):
        del_data()
        trange = ['2017-03-27', '2017-03-28']
        d = pyspedas.secs.data(trange=trange,
                               resolution=10,
                               dtype='EICS',
                               no_download=False,
                               downloadonly=False,
                               out_type='np')
        # Returns a Pandas dataframe, not tplot variables
        self.assertTrue(len(d) > 0)

if __name__ == '__main__':
    unittest.main()
