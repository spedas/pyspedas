import unittest
from unittest.mock import patch
import pyspedas
from pyspedas.secs.makeplots import make_plots

from pyspedas.secs.config import CONFIG
CONFIG['plots_dir'] = 'dir/'


class SECSTestCases(unittest.TestCase):
    @patch("matplotlib.pyplot.show")
    def test_load_secs(self, mock_show):
        trange = ['2017-03-27', '2017-03-28']
        d = pyspedas.secs.data(trange=trange,
                               resolution=10,
                               dtype='SECS',
                               no_download=False,
                               downloadonly=False,
                               out_type='df')

        make_plots(dtype='SECS',
                   dtime='2017-03-27/06:00:00',
                   vplot_sized=True,
                   contour_den=201,
                   s_loc=False,
                   quiver_scale=30)

    @patch("matplotlib.pyplot.show")
    def test_load_eics(self, mock_show):
        trange = ['2017-03-27', '2017-03-28']
        d = pyspedas.secs.data(trange=trange,
                               resolution=10,
                               dtype='EICS',
                               no_download=False,
                               downloadonly=False,
                               out_type='df')

        make_plots(dtype='EICS',
                   dtime='2017-03-27/06:00:00',
                   vplot_sized=True,
                   contour_den=201,
                   s_loc=False,
                   quiver_scale=30)

    def test_load_secs_dc(self):
        trange = ['2017-03-27', '2017-03-28']
        d = pyspedas.secs.data(trange=trange,
                               resolution=10,
                               dtype='SECS',
                               no_download=False,
                               downloadonly=False,
                               out_type='dc')

    # def test_load_eics_dc(self):
    #     trange = ['2017-03-27', '2017-03-28']
    #     d = pyspedas.secs.data(trange=trange,
    #                            resolution=10,
    #                            dtype='EICS',
    #                            no_download=False,
    #                            downloadonly=False,
    #                            out_type='dc')

    def test_load_secs_np(self):
        trange = ['2017-03-27', '2017-03-28']
        d = pyspedas.secs.data(trange=trange,
                               resolution=10,
                               dtype='SECS',
                               no_download=False,
                               downloadonly=False,
                               out_type='np')

    # def test_load_eics_np(self):
    #     trange = ['2017-03-27', '2017-03-28']
    #     d = pyspedas.secs.data(trange=trange,
    #                            resolution=10,
    #                            dtype='EICS',
    #                            no_download=False,
    #                            downloadonly=False,
    #                            out_type='np')

if __name__ == '__main__':
    unittest.main()
