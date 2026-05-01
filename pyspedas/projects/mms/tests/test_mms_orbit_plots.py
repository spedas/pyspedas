import unittest
import os
from pyspedas.projects.mms.mms_orbit_plot import mms_orbit_plot


class TestMMSOrbitPlot(unittest.TestCase):
    def test_trange(self):
        # Set trange and save_png options
        trange = ['2015-10-16/00:00:00', '2015-10-16/12:00:00']
        save_png = 'test_trange'

        mms_orbit_plot(trange=trange, save_png=save_png, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_png + '.png'))

    def test_probes(self):
        # Set probes and save_png options
        probes = [1, 2]
        save_png = 'test_probes'

        mms_orbit_plot(probes=probes, save_png=save_png, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_png + '.png'))

    def test_data_rate(self):
        # Set data_rate and save_png options
        data_rate = 'brst'
        save_png = 'test_data_rate'

        mms_orbit_plot(probes=[1, 4], trange=['2019-05-01/02:00', '2019-05-01/02:20'], data_rate=data_rate, save_png=save_png, display=False, earth=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_png + '.png'))

    def test_plane(self):
        # Set plane and save_png options
        plane = 'yz'
        save_png = 'test_plane'

        mms_orbit_plot(plane=plane, save_png=save_png, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_png + '.png'))

    def test_xr(self):
        # Set xr and save_png options
        xr = [-5, 5]
        save_png = 'test_xr'

        mms_orbit_plot(xr=xr, save_png=save_png, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_png + '.png'))

    def test_yr(self):
        # Set yr and save_png options
        yr = [-5, 5]
        save_png = 'test_yr'

        mms_orbit_plot(yr=yr, save_png=save_png, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_png + '.png'))

    def test_coord(self):
        # Set coord and save_png options
        coord = 'gsm'
        save_png = 'test_coord'

        mms_orbit_plot(coord=coord, save_png=save_png, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_png + '.png'))

    def test_xsize(self):
        # Set xsize and save_png options
        xsize = 10
        save_png = 'test_xsize'

        mms_orbit_plot(xsize=xsize, save_png=save_png, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_png + '.png'))

    def test_ysize(self):
        # Set ysize and save_png options
        ysize = 10
        save_png = 'test_ysize'

        mms_orbit_plot(ysize=ysize, save_png=save_png, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_png + '.png'))

    def test_marker(self):
        # Set marker and save_png options
        marker = 'o'
        save_png = 'test_marker'

        mms_orbit_plot(marker=marker, save_png=save_png, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_png + '.png'))

    def test_markevery(self):
        # Set markevery and save_png options
        markevery = 5
        save_png = 'test_markevery'

        mms_orbit_plot(markevery=markevery, save_png=save_png, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_png + '.png'))

    def test_markersize(self):
        # Set markersize and save_png options
        markersize = 10
        save_png = 'test_markersize'

        mms_orbit_plot(markersize=markersize, save_png=save_png, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_png + '.png'))

    def test_earth(self):
        # Set earth and save_png options
        earth = False
        save_png = 'test_earth'

        mms_orbit_plot(earth=earth, save_png=save_png, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_png + '.png'))

    def test_dpi(self):
        # Set dpi and save_png options
        dpi = 100
        save_png = 'test_dpi'

        mms_orbit_plot(dpi=dpi, save_png=save_png, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_png + '.png'))

    def test_save_pdf(self):
        # Set save_png option
        save_pdf = 'test_save_pdf'

        mms_orbit_plot(save_pdf=save_pdf, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_pdf + '.pdf'))

    def test_save_eps(self):
        # Set save_eps option
        save_eps = 'test_save_eps'

        mms_orbit_plot(save_eps=save_eps, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_eps + '.eps'))

    def test_save_jpeg(self):
        # Set save_jpeg option
        save_jpeg = 'test_save_jpeg'

        mms_orbit_plot(save_jpeg=save_jpeg, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_jpeg + '.jpeg'))

    def test_save_svg(self):
        # Set save_svg option
        save_svg = 'test_save_svg'

        mms_orbit_plot(save_svg=save_svg, display=False)

        # Check that the test figure was saved
        self.assertTrue(os.path.exists(save_svg + '.svg'))

    def test_return_plot_objects(self):
        # Set return_plot_objects option
        return_plot_objects = True

        plot_objects = mms_orbit_plot(return_plot_objects=return_plot_objects, display=False)

        # Check that plot_objects is a tuple
        self.assertIsInstance(plot_objects, tuple)


if __name__ == '__main__':
    unittest.main()
