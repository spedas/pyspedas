"""Dependency smoke tests for the shared PyHC environment.

Run only this module, not discovery of the full PySPEDAS test tree::

    MPLBACKEND=Agg python -m unittest -v pyspedas.tests.test_pyhc_integration

See README_pyhc.md for provenance, dependencies, and network requirements.
"""

from pathlib import Path
import tempfile
import socket
import unittest
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numpy.testing import assert_allclose

import pyspedas as ps


class SmokeTestCase(unittest.TestCase):
    """Give every test clean tplot state and temporary plot output."""

    def setUp(self):
        ps.del_data("*")
        self.addCleanup(ps.del_data, "*")
        self.addCleanup(plt.close, "all")
        directory = tempfile.TemporaryDirectory(prefix="pyspedas-pyhc-")
        self.addCleanup(directory.cleanup)
        self.output = Path(directory.name)

    def assert_data(self, name):
        self.assertTrue(ps.data_exists(name), f"No data loaded into {name}")
        data = ps.get_data(name)
        self.assertGreater(data.times.size, 0)
        self.assertTrue(np.isfinite(data.y).any(), f"No finite values in {name}")
        return data

    def assert_plot(self, path):
        self.assertTrue(path.is_file(), f"Plot was not saved: {path}")
        pixels = plt.imread(path)
        self.assertGreater(np.ptp(pixels), 0, "Plot is blank")


class LocalTests(SmokeTestCase):
    """No mission downloads or external validation fixtures."""

    def test_csv_sector_masks(self):
        """From test_mms_feeps.test_sector_masks; CSVs ship with PySPEDAS."""
        from pyspedas.projects.mms.feeps_tools.mms_read_feeps_sector_masks_csv import mms_read_feeps_sector_masks_csv

        masks = mms_read_feeps_sector_masks_csv(["2015-08-01", "2015-08-02"])
        self.assertEqual(masks["mms1imaskt2"], [11, 12])
        self.assertEqual(masks["mms1imaskt3"], [22, 23, 24, 25, 26, 27, 28, 31, 32])

    def test_wavelet_and_spectrogram(self):
        """From test_analysis.test_wavelet, with a saved line/spectrogram plot."""
        t = np.arange(4000.0)
        y = np.sin(2 * np.pi * t / 32.0)
        y2 = np.sin(2 * np.pi * t / 64.0)
        y[1000:3000] = y2[1000:3000]
        ps.store_data("sin_wav", data={"x": ps.time_double("2010-01-01") + 10 * t, "y": y})
        names = ps.wavelet("sin_wav", wavename="gaus1")
        self.assertTrue(names)
        power = self.assert_data(names[0])
        self.assertEqual(power.y.shape[0], t.size)
        self.assertGreater(power.y.shape[1], 1)
        self.assertTrue(np.isfinite(power.y).all())
        self.assertTrue((power.y >= 0).all())
        path = self.output / "wavelet.png"
        ps.tplot(["sin_wav", names[0]], display=False, save_png=str(path))
        self.assert_plot(path)

    def test_line_plot(self):
        """From test_utilities_plot.test_markers_and_symbols (one render)."""
        ps.store_data("data", data={"x": [1, 2, 3, 4, 5, 6], "y": [1, 1, 1, 1, 1, 1]})
        ps.options("data", "marker", "X")
        path = self.output / "line.png"
        ps.tplot("data", display=False, save_png=str(path))
        self.assert_plot(path)

    def test_basemap(self):
        """From MPLPlotter/plot_tests/test_tplot_map.test_basic_map."""
        from pyspedas.tplot_tools.MPLPlotter.tplot_map import tplot_map

        tmap = tplot_map(
            projection="merc", resolution="c", llcrnrlon=-170, llcrnrlat=35,
            urcrnrlon=-45, urcrnrlat=75,
        )
        tmap.add_map_boundary()
        tmap.add_fillcontinents()
        tmap.add_coastlines(linewidth=0.25)
        x, y = tmap(-100, 50)
        self.assertTrue(np.isfinite([x, y]).all())
        assert_allclose(tmap(x, y, inverse=True), [-100, 50])
        path = self.output / "map.png"
        plt.savefig(path, dpi=100)
        self.assert_plot(path)

    def test_t89(self):
        """From test_geopack.test_tt89 and gen_circle; six synthetic positions."""
        from pyspedas.geopack import tt89

        angle = np.deg2rad(np.arange(0.0, 360.0, 60.0))
        positions = 5 * 6371.2 * np.column_stack((np.sin(angle), np.zeros(6), np.cos(angle)))
        times = ps.time_double("2024-01-01/06:31:00") + np.arange(6)
        ps.store_data("circle", data={"x": times, "y": positions})
        ps.set_coords("circle", "GSM")
        ps.set_units("circle", "km")
        tt89("circle", iopt=3)
        field = self.assert_data("circle_bt89")
        assert_allclose(field.times, times)
        self.assertEqual(field.y.shape, (6, 3))
        self.assertTrue(np.isfinite(field.y).all())
        self.assertGreater(np.max(np.abs(field.y)), 0)
        # Exercise PySPEDAS' Astropy quantity conversion as well as Geopack.
        quantity = ps.get_data("circle_bt89", units=True).y
        assert_allclose(quantity.to_value("T"), field.y * 1e-9)

    def test_wave_polarization(self):
        """From test_twavpol.test_multiple_twavpol_call; replace IDL fixture with a wave."""
        t = np.arange(512.0)
        phase = 2 * np.pi * t / 16
        vector = np.column_stack((np.cos(phase), np.sin(phase), 0.1 * np.sin(2 * phase)))
        ps.store_data("wave", data={"x": ps.time_double("2010-01-01") + t, "y": vector})
        # wavpol changes warning filters internally; restore them after each call.
        with warnings.catch_warnings():
            self.assertEqual(ps.twavpol("wave", nopfft=64, steplength=32, bin_freq=3), 1)
        before = self.assert_data("wave_powspec").y.copy()
        for suffix in ("degpol", "waveangle", "elliptict", "helict", "pspec3"):
            self.assert_data("wave_" + suffix)
        with warnings.catch_warnings():
            self.assertEqual(ps.twavpol("wave", nopfft=64, steplength=32, bin_freq=3), 1)
        after = self.assert_data("wave_powspec")
        assert_allclose(before, after.y)
        peak = after.v[np.nanargmax(np.nanmean(after.y, axis=0))]
        self.assertAlmostEqual(peak, 1 / 16, delta=1 / 64)

    def test_numpy_interp(self):
        """Copied from test_analysis.test_numpy_interp."""
        time_strings_input = np.array(
            [
                "2018-07-01T13:02:16.892474880",
                "2018-07-01T13:02:16.922475008",
                "2018-07-01T13:02:16.952474880",
            ]
        )
        values_input = np.array([0.028584518, 0.0, 0.013626526], dtype=np.float32)

        time_strings_interp_to = np.array(["2018-07-01T13:02:16.922475008"])
        input_times_npdt64 = np.array([np.datetime64(t) for t in time_strings_input])
        interp_to_times_npdt64 = np.array(
            [np.datetime64(t) for t in time_strings_interp_to]
        )
        input_times_float64 = input_times_npdt64.astype(np.float64)
        interp_to_time_float64 = interp_to_times_npdt64.astype(np.float64)
        result = np.interp(interp_to_time_float64, input_times_float64, values_input)
        # This works, unlike scipy and xarray!
        self.assertTrue((result >= 0.0).all())
        assert_allclose(result, [0.0], atol=1e-12)

    def test_tinterpol_slinear(self):
        """Copied from test_analysis.test_tinterpol_slinear (xarray/SciPy)."""
        # This test uses the 'slinear' interpolation method (order 1 spline) which
        # seems not to be susceptible to the issue that method='linear' has with interpolating
        # to points exactly matching the input times.
        time_strings_input = np.array(
            [
                "2018-07-01T13:02:16.892474880",
                "2018-07-01T13:02:16.922475008",
                "2018-07-01T13:02:16.952474880",
            ]
        )
        values_input = np.array([0.028584518, 0.0, 0.013626526], dtype=np.float32)
        time_strings_interp_to = np.array(["2018-07-01T13:02:16.922475008"])
        input_times_npdt64 = np.array([np.datetime64(t) for t in time_strings_input])
        interp_to_times_npdt64 = np.array(
            [np.datetime64(t) for t in time_strings_interp_to]
        )
        ps.store_data("interp_input", data={"x": input_times_npdt64, "y": values_input})
        ps.store_data("interp_to", data={"x": interp_to_times_npdt64, "y": [0.0]})
        ps.tinterpol(
            "interp_input", "interp_to", newname="interp_result", method="slinear"
        )
        result = ps.get_data("interp_result")
        self.assertTrue((result.y >= 0.0).all())
        assert_allclose(result.y, [0.0], atol=1e-12)


    def test_interpolate_nan_gaps(self):
        """From test_interp_nan.test_time_limit_uses_elapsed_seconds."""
        times = np.array([0., 1., 2., 3., 10., 11., 20.])
        values = np.array([0., np.nan, np.nan, 3., 10., np.nan, 20.])
        ps.store_data("gaps", data={"x": times, "y": values})
        # Xarray's max_gap path also exercises bottleneck's forward filling.
        ps.interp_nan("gaps", "filled", max_gap_time=3)
        assert_allclose(ps.get_data("filled").y, [0, 1, 2, 3, 10, np.nan, 20], equal_nan=True)


class NetworkTests(SmokeTestCase):
    """Small public loads; failures remain failures, including server errors."""

    def setUp(self):
        super().setUp()
        # Bound urllib-based clients (HAPI); restore the process default afterward.
        self.addCleanup(socket.setdefaulttimeout, socket.getdefaulttimeout())
        socket.setdefaulttimeout(30)

    def test_cdf_ace(self):
        """From test_ace.test_load_mfi_data; one hour from one daily CDF."""
        trange = ["2018-11-05/00:00:00", "2018-11-05/01:00:00"]
        loaded = ps.projects.ace.mfi(trange=trange, time_clip=True, varnames=["Magnitude"])
        self.assertIn("Magnitude", loaded)
        data = self.assert_data("Magnitude")
        self.assertGreaterEqual(data.times[0], ps.time_double(trange[0]))
        self.assertLessEqual(data.times[-1], ps.time_double(trange[1]))

    def test_hapi_calgary(self):
        """From test_hapi.test_calgary_specbins; five minutes instead of a day."""
        trange = ["2026-01-25T00:00:00", "2026-01-25T00:05:00"]
        loaded = ps.hapi(
            trange=trange,
            server="https://api.phys.ucalgary.ca/hapi", dataset="SWAN_HSR_K0@GILL",
            # The power's HAPI bins refer to this separate frequency parameter.
            parameters=["raw_power", "band_central_frequency"],
        )
        self.assertIn("raw_power", loaded)
        data = self.assert_data("raw_power")
        self.assertEqual(data.y.ndim, 2)
        self.assertGreater(data.y.shape[1], 1)
        self.assertEqual(data.v.shape[-1], data.y.shape[1])
        self.assertTrue(np.isfinite(data.v).all())
        self.assertGreaterEqual(data.times[0], ps.time_double(trange[0]))
        self.assertLessEqual(data.times[-1], ps.time_double(trange[1]))
        path = self.output / "hapi_calgary.png"
        ps.tplot("raw_power", display=False, save_png=str(path))
        self.assert_plot(path)

    def test_cdaweb_netcdf(self):
        """From test_cdagui.test_load_icon_netcdf; NetCDF via NASA, not NCEI."""
        from pyspedas.cdagui_tools.config import CONFIG

        from cdasws import CdasWs

        client = ps.CDAWeb()
        # CDAWeb currently constructs cdasws without a timeout. Use its public
        # constructor to keep this small integration request bounded.
        client.cdas.close()
        client.cdas = CdasWs(endpoint=CONFIG["cdas_endpoint"], timeout=30)
        self.addCleanup(client.cdas.close)
        urls = client.get_filenames(
            ["ICON_L2-2_MIGHTI_VECTOR-WIND-GREEN"],
            "2021-01-15T14:05:52", "2021-01-15T15:08:57",
        )
        self.assertTrue(urls, "CDAWeb returned no ICON files")
        count, _, names = client.cda_download(urls, CONFIG["local_data_dir"])
        self.assertGreater(count, 0)
        self.assertIn("ICON_L22_Fringe_Amplitude", names)
        self.assert_data("ICON_L22_Fringe_Amplitude")

    def test_mth5_fdsn(self):
        """From test_load_fdsn.test02_load_fdsn_basic; one station, five minutes."""
        from pyspedas.mth5.load_fdsn import load_fdsn

        trange = ["2015-06-22T01:45:00", "2015-06-22T01:50:00"]
        name = load_fdsn(network="4P", station="REU49", trange=trange, nodownload=True)
        self.assertEqual(name, "fdsn_4P_REU49")
        data = self.assert_data(name)
        self.assertEqual(data.y.shape[1], 3)
        self.assertGreaterEqual(data.times[0], ps.time_double(trange[0]))
        self.assertLessEqual(data.times[-1], ps.time_double(trange[1]))


if __name__ == "__main__":
    unittest.main()
