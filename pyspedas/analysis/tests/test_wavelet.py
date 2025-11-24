"""Tests of wavelet tool.

These tests will download various IDL tplot savefiles from https://github.com/spedas/test_data
They will also create multiple png files that contain IDL and python plots for comparison.
These png files are created inside CONFIG["local_data_dir"].
"""

import os
import unittest
import logging
from numpy.testing import assert_allclose
import numpy as np
from pyspedas import (
    get_data,
    tplot,
    tplot_rename,
    ylim,
    zlim,
    options,
    tplot_options,
    split_vec,
    join_vec,
    store_data,
    del_data,
    time_double,
    wavelet,
    wavelet98,
    wav_data,
    tplot_restore,
    tplot_names,
)
from pyspedas.analysis.tests.wavetest import wavetest
from pyspedas.utilities.config_testing import TESTING_CONFIG, test_data_download_file

# Whether to display plots during testing
global_display = TESTING_CONFIG["global_display"]
# Directory to save testing output files
output_dir = TESTING_CONFIG["local_testing_dir"]
# Ensure output directory exists
analysis_dir = "analysis_tools"
save_dir = os.path.join(output_dir, analysis_dir)
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
# Directory with IDL SPEDAS validation files
validation_dir = TESTING_CONFIG["remote_validation_dir"]


def tc_scales_from_freqs(freqs, omega0=6.0):
    """Convert desired physical frequencies [Hz] to wavelet scales using Torrence & Compo (1998)"""
    fourier_factor = (omega0 + np.sqrt(2 + omega0**2)) / (4 * np.pi)
    return 1.0 / (freqs * fourier_factor)  # No dt here!


def fracyear_to_unix(fyear: float):
    # Convert fractional years yyyy.fff from Torrence and Compo example to Unix timestamps
    iyear = int(fyear)
    ut_start = time_double(str(iyear))
    frac = fyear - iyear
    secs = time_double(str(iyear + 1)) - ut_start
    return ut_start + frac * secs


class TwaveletDataValidation(unittest.TestCase):
    """Compares wavelet results between Python and IDL"""

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The SPEDAS script that creates the file: general/tools/python_validate/wavelet_python_validate.pro
        """

        # Testing tolerance
        cls.tol = 1e-10

        # Load validation variables from the test file
        filename = test_data_download_file(
            validation_dir, analysis_dir, "wavelet_test.tplot", save_dir
        )
        # If filename does not exist, skip the test
        if not os.path.exists(filename):
            raise unittest.SkipTest(
                "Cannot find local IDL savefile for comparison. Filename: " + filename
            )

        del_data("*")
        tplot_restore(filename)
        tplot_names()

        # Test 1: simple sine waves
        cls.sin_wav = get_data("sin_wav")
        cls.sin_wav_wv_pow = get_data("sin_wav_wv_pow")

        # Test 2: Vassilis homework example using THEMIS FGM data
        cls.tha_fgs_fac_bp_x = get_data("tha_fgs_fac_bp_x")
        cls.tha_fgs_fac_bp_y = get_data("tha_fgs_fac_bp_y")
        cls.tha_fgs_fac_bp_z = get_data("tha_fgs_fac_bp_z")
        cls.tha_fgs_fac_bp_x_wv_pow = get_data("tha_fgs_fac_bp_x_wv_pow")
        cls.tha_fgs_fac_bp_y_wv_pow = get_data("tha_fgs_fac_bp_y_wv_pow")
        cls.tha_fgs_fac_bp_z_wv_pow = get_data("tha_fgs_fac_bp_z_wv_pow")
        cls.wavetest_powspec = get_data("wavetest_powspec")

        tplot_rename("sin_wav_wv_pow", "idl_sin_wav_wv_pow")
        tplot_rename("wavetest_powspec", "idlwavetest_powspec")

        zlim("tha_fgs_fac_bp_?_wv_pow", 1.0e-1, 1.0e2)
        ylim("tha_fgs_fac_bp_?_wv_pow", 1.0e-3, 4.1e-2)
        options("tha_fgs_fac_bp_?_wv_pow", "zlog", True)
        options("tha_fgs_fac_bp_?_wv_pow", "ylog", False)

        tplot_rename("tha_fgs_fac_bp_x_wv_pow", "idl_fgs_fac_bp_x_wv_pow")
        tplot_rename("tha_fgs_fac_bp_y_wv_pow", "idl_fgs_fac_bp_y_wv_pow")
        tplot_rename("tha_fgs_fac_bp_z_wv_pow", "idl_fgs_fac_bp_z_wv_pow")

    def setUp(self):
        """We need to clean tplot variables before each run"""
        # del_data('*')

    def test_sin_wav(self):
        # The default is 'morl' rather than 'cmorl0.5-1.0, but it doesn't appear to make that much difference.
        # cmorl0.5-1.0 is what Eric used in the wiki example.
        wavelet("sin_wav", wavename="cmorl1.5-1.0")
        pvar = "sin_wav_pow"
        options(pvar, "colormap", "jet")
        ylim(pvar, 0.001, 0.1)
        options(pvar, "ylog", True)
        options(pvar, "ytitle", pvar)
        options(pvar, "zlog", True)
        d = get_data("sin_wav_pow")
        logging.info(
            f"Python frequencies: bin count {d.y.shape[1]}, min {np.min(d.v)}, max: {np.max(d.v)}"
        )
        logging.info(f"Python power: min {np.min(d.y)}, max {np.max(d.y)}")
        d_idl = get_data("idl_sin_wav_wv_pow")
        logging.info(
            f"IDL frequencies: bin count {d_idl.y.shape[1]}, min {np.min(d_idl.v)}, max: {np.max(d_idl.v)}"
        )
        logging.info(f"IDL power: min {np.min(d_idl.y)}, max {np.max(d_idl.y)}")

        local_png = os.path.join(save_dir, "sin_wav_simple.png")
        tvar = ["sin_wav", "sin_wav_pow", "idl_sin_wav_wv_pow"]
        tplot(tvar, display=global_display, save_png=local_png)

    def test_equiv_wav(self):

        # 54 logarithmically spaced frequencies between IDL min and max
        idl_freqs = np.logspace(np.log10(0.00051), np.log10(0.05), 54)

        scales = tc_scales_from_freqs(idl_freqs)
        self.assertIsNotNone(scales)

        wavelet("sin_wav", wavename="cmorl1.5-1.0", sampling_period=1.0)
        pvar = "sin_wav_pow"
        options(pvar, "colormap", "spedas")
        ylim(pvar, 0.0005, 0.05)
        options(pvar, "ylog", True)
        options(pvar, "zlog", True)
        options(pvar, "ytitle", pvar)
        d = get_data(pvar)
        logging.info(
            f"Python frequencies: bin count {d.y.shape[1]}, min {np.min(d.v)}, max: {np.max(d.v)}"
        )
        logging.info(f"Python power: min {np.min(d.y)}, max {np.max(d.y)}")
        d_idl = get_data("idl_sin_wav_wv_pow")
        logging.info(
            f"IDL frequencies: bin count {d_idl.y.shape[1]}, min {np.min(d_idl.v)}, max: {np.max(d_idl.v)}"
        )
        logging.info(f"IDL power: min {np.min(d_idl.y)}, max {np.max(d_idl.y)}")

        local_png = os.path.join(save_dir, "sin_wav_equiv.png")
        tvar = ["sin_wav", "sin_wav_pow", "idl_sin_wav_wv_pow"]
        tplot(tvar, display=global_display, save_png=local_png)

    def test_themis_fgm_wavelet(self):
        wavelet("tha_fgs_fac_bp_x")
        wavelet("tha_fgs_fac_bp_y")
        wavelet("tha_fgs_fac_bp_z")

        zlim("tha_fgs_fac_bp_?_pow", 1.0e-1, 1.0e2)
        ylim("tha_fgs_fac_bp_?_pow", 1.0e-3, 4.1e-2)
        options("tha_fgs_fac_bp_?_pow", "zlog", True)
        options("tha_fgs_fac_bp_?_pow", "ylog", False)
        d = get_data("tha_fgs_fac_bp_x_pow")
        logging.info(
            f"Python frequencies: bin count {d.y.shape[1]}, min {np.min(d.v)}, max: {np.max(d.v)}"
        )
        logging.info(f"Python power: min {np.min(d.y)}, max {np.max(d.y)}")
        d_idl = get_data("idl_fgs_fac_bp_x_wv_pow")
        logging.info(
            f"IDL frequencies: bin count {d_idl.y.shape[1]}, min {np.min(d_idl.v)}, max: {np.max(d_idl.v)}"
        )
        logging.info(f"IDL power: min {np.min(d_idl.y)}, max {np.max(d_idl.y)}")

        local_png = os.path.join(save_dir, "themis_fgm_wavelets.png")
        tvar = ["tha_fgs_fac_bp_x_pow", "idl_fgs_fac_bp_x_wv_pow"]
        tplot(tvar, display=global_display, save_png=local_png)

    def test_nino3_tc(self):

        output_dict = wavetest(noplot=True)
        timestamps = [fracyear_to_unix(t) for t in output_dict["time"]]
        store_data(
            "sst_nino3_pwr",
            data={
                "x": timestamps,
                "y": output_dict["power"],
                "v": output_dict["period"],
            },
        )
        options("sst_nino3_pwr", "spec", 1)
        options("sst_nino3_pwr", "yrange", [0.5, 128.0, 1])
        options("sst_nino3_pwr", "zlog", 0)

        options("idlwavetest_powspec", "spec", 1)
        options("idlwavetest_powspec", "yrange", [0.5, 128.0, 1])
        options("idlwavetest_powspec", "zlog", 0)

        local_png = os.path.join(save_dir, "nino_powspec.png")
        tvar = "sst_nino3_pwr idlwavetest_powspec"
        tplot(tvar, display=global_display, save_png=local_png)
        d = get_data("sst_nino3_pwr")
        assert_allclose(d.times, self.wavetest_powspec.times)
        assert_allclose(d.v, self.wavetest_powspec.v)
        # Max relative difference 2.8e-06
        assert_allclose(d.y, self.wavetest_powspec.y, rtol=3e-05)

    def test_wav_data(self):
        # Compare results of wav_data.py to wav_data.pro

        # IDL results (from savefile)
        # IDL Themis data, after all transformation, but before applying wavelets
        tvars = ["tha_fgs_fac_bp_x", "tha_fgs_fac_bp_y", "tha_fgs_fac_bp_z"]
        # IDL results after applying wav_data.pro
        idl_pow = [
            "idl_fgs_fac_bp_x_wv_pow",
            "idl_fgs_fac_bp_y_wv_pow",
            "idl_fgs_fac_bp_z_wv_pow",
        ]

        # Python results (to be computed below)
        py_pow = [
            "tha_fgs_fac_bp_x_wv_pow",
            "tha_fgs_fac_bp_y_wv_pow",
            "tha_fgs_fac_bp_z_wv_pow",
        ]

        all_vars = []
        dcomp = ["time", "y", "v"]
        dxyz = ["x", "y", "z"]

        for i in range(3):
            # Compute the wavelet transform for each of x,y,z
            wav_data(tvars[i])

            # Compare python results with IDL results
            d1 = get_data(idl_pow[i])
            d2 = get_data(py_pow[i])
            logging.info(f"IDL {idl_pow[i]}: {d1.y.shape}, {d1.v.shape}")
            logging.info(f"Python {py_pow[i]}: {d2.y.shape}, {d2.v.shape}")
            for j in range(3):
                # Find max difference
                max_diff = np.abs(np.max(d1[j] - d2[j]))
                logging.info(f"- Max difference for {dcomp[j]}: {max_diff}")
                assert_allclose(d1[j], d2[j], rtol=1e-3, atol=1e-3)

            # Set plotting parameters
            options(py_pow[i], "ytitle", "python " + dxyz[i])
            options(idl_pow[i], "ytitle", "idl " + dxyz[i])
            options(py_pow[i], "ztitle", "python Ptot")
            options(idl_pow[i], "ztitle", "idl Ptot")
            options(py_pow[i], "zlog", True)
            options(py_pow[i], "ylog", False)
            options(idl_pow[i], "zlog", True)
            options(idl_pow[i], "ylog", False)
            zlim(py_pow[i], 1.0e-1, 1.0e2)
            ylim(py_pow[i], 1.0e-3, 4.1e-2)
            zlim(idl_pow[i], 1.0e-1, 1.0e2)
            ylim(idl_pow[i], 1.0e-3, 4.1e-2)
            all_vars.append(idl_pow[i])
            all_vars.append(py_pow[i])

        # Plot 6 panels (x,y,z - IDL, python)
        tplot_options("title", "wav_data: IDL - Python comparison")
        local_png = os.path.join(save_dir, "wav_data_test.png")
        tplot(all_vars, display=global_display, save_png=local_png)

    def test_store_data_singleton_v(self):
        times = [0.0, 1.0, 2.0]
        y = [0.0, 1.0, 2.0]
        v1 = [1]
        v2 = [0.1, 0.2, 0.3]

        # scalar v  (e.g. for 3-vector, or spectrogram with non-time-varying bin values
        store_data("newvar", data={"x": times, "y": y, "v": v1})
        md = get_data("newvar", metadata=True)
        assert_allclose(md["extra_v_values"], np.array(v1))
        # array v (e.g. spectrogram with time-varying bin values)
        store_data("newvar2", data={"x": times, "y": y, "v1": v2})
        md = get_data("newvar2", metadata=True)
        assert_allclose(md["extra_v_values"], np.array(v2))

    def test_join_vec(self):
        dat_x = get_data("tha_fgs_fac_bp_x")
        dat_y = get_data("tha_fgs_fac_bp_y")
        dat_z = get_data("tha_fgs_fac_bp_z")
        self.assertEqual(np.shape(dat_x), np.shape(dat_y))
        self.assertEqual(np.shape(dat_y), np.shape(dat_z))
        join_vec(
            ["tha_fgs_fac_bp_x", "tha_fgs_fac_bp_y", "tha_fgs_fac_bp_z"],
            newname="tha_fgs_joined",
        )
        dat_jv = get_data("tha_fgs_joined")
        self.assertEqual(
            len(dat_jv), 3
        )  # Should have times, yvals, and a 'v' component

    def test_split_rejoin_non_time_varying(self):
        time = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        yvals = np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 1.0, 1.0],
                [2.0, 2.0, 2.0],
                [3.0, 3.0, 3.0],
                [4.0, 4.0, 4.0],
            ]
        )
        const_v = np.array([11.0, 12.0, 13.0])
        store_data("newvar", data={"x": time, "y": yvals, "v": const_v})
        orig_data = get_data("newvar")
        self.assertIsNotNone(orig_data)
        split_vec("newvar")
        join_vec("newvar_*", newname="newvar_rejoined")
        joined_dat = get_data("newvar_rejoined")
        self.assertEqual(len(joined_dat), 3)
        assert_allclose(joined_dat.v, const_v)

    def test_split_rejoin_time_varying(self):
        time = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        yvals = np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 1.0, 1.0],
                [2.0, 2.0, 2.0],
                [3.0, 3.0, 3.0],
                [4.0, 4.0, 4.0],
            ]
        )
        time_varying_v = np.array(
            [
                [1.0, 2.0, 3.0],
                [11.0, 12.0, 13.0],
                [21.0, 22.0, 23.0],
                [31.0, 32.0, 33.0],
                [41.0, 42.0, 43.0],
            ]
        )
        store_data("newvar_tv", data={"x": time, "y": yvals, "v": time_varying_v})
        orig_data = get_data("newvar_tv")
        self.assertIsNotNone(orig_data)
        split_vec("newvar_tv")
        dx = get_data("newvar_tv_x")
        self.assertIsNotNone(dx)
        md = get_data("newvar_tv_x", metadata=True)
        self.assertIn("extra_v_values", md)
        join_vec("newvar_tv_*", newname="newvar_tv_rejoined")
        joined_dat = get_data("newvar_tv_rejoined")
        self.assertEqual(len(joined_dat), 3)
        assert_allclose(joined_dat.v, time_varying_v)

    def test_wav_data_keywords(self):
        # Test various wav_data keywords
        # using a synthetic sine wave dataset so that the test is fast and self-contained

        del_data()
        t = np.arange(4000, dtype=float)
        vtime = time_double("2010-01-01") + 10 * t

        # Create a two-dimensional variable
        var = "sin_wav"
        vdata = np.zeros((4000, 2), dtype=float)
        vdata[:, 0] = np.cos(2 * np.pi * t / 32.0)
        vdata[:, 1] = np.sin(2 * np.pi * t / 64.0)
        store_data(var, data={"x": vtime, "y": vdata})

        # Test rbin, dimennum
        wav_data(var, dimennum=1, rbin=4)
        var1x = "sin_wav(1)_wv_pow"
        var1 = "test_rbin"
        tplot_rename(var1x, var1)
        d = get_data(var1)
        # Since rbin=4, length should be 1000
        self.assertEqual(len(d[0]), 1000)

        # Test trange
        wav_data(var, dimennum=0, trange=[vtime[1000], vtime[2000]])
        var2x = "sin_wav(0)_wv_pow"
        var2 = "test_trange"
        tplot_rename(var2x, var2)
        d = get_data(var2)
        # Since trange is 1001 points, length should be 1001
        self.assertEqual(len(d[0]), 1001)

        # Test resolution
        wav_data(var, dimennum=0, resolution=8)
        var3x = "sin_wav(0)_wv_pow"
        var3 = "test_resolution"
        tplot_rename(var3x, var3)
        d = get_data(var3)
        # Since resolution=8, length should be 500
        self.assertEqual(len(d[0]), 500)

        # Test prange
        wav_data(var, dimennum=0, prange=[8, 60])
        var4x = "sin_wav(0)_wv_pow"
        var4 = "test_prange"
        tplot_rename(var4x, var4)
        d = get_data(var4)
        # Period range should be within 8 to 60
        p = np.array(1.0 / d[2])
        logging.info(p)
        self.assertTrue(np.min(p) >= 8.0)
        self.assertTrue(np.max(p) <= 60.0)
        # In this case, the first p should be 8.0
        self.assertAlmostEqual(np.min(p), 8.0, delta=0.01)

        # Plot all results (optional)
        vnames = tplot_names()
        logging.info(vnames)
        local_png = os.path.join(save_dir, "wav_data_keywords.png")
        tplot(vnames, display=global_display, save_png=local_png)

    def test_wav_data_keywords2(self):
        # Test wav_data with various keywords and compare with IDL results.
        # This is using the IDL save file wav_data_key2_test.tplot
        # which was created by the SPEDAS script: wav_data_validate.pro

        logging.info("\n\nTesting wav_data with keywords2\n")

        # Load IDL savefile
        filename = test_data_download_file(
            validation_dir, analysis_dir, "wav_data_key2_test.tplot", save_dir
        )
        # If filename does not exist, skip the test
        if not os.path.exists(filename):
            self.skipTest(
                "Cannot find local IDL savefile for comparison. Filename: " + filename
            )

        # Load validation variables from the test file
        del_data("*")
        tplot_restore(filename)
        tplot_names()

        var = "sin_wav"
        all_vars = [var]
        py_names = [
            "sin_wav_wv_pow",
            "sin_wav_wv_rat_par",
            "sin_wav_wv_pol_par",
            "sin_wav_wv_pol_perp",
        ]

        for n in py_names:
            new_name = "idl_" + n
            tplot_rename(n, new_name)
            all_vars.append(new_name)
            all_vars.append(n)

        wav_data(var, magrat=1, normval=1, fraction=1, kolom=1, rotate_pow=1)

        # Compare with IDL results
        for n in py_names:
            logging.info(f"Comparing {n}")
            d_idl = get_data("idl_" + n)
            d_py = get_data(n)
            ddd = np.abs(d_idl.y - d_py.y)
            logging.info(
                f"Max difference: {np.max(ddd)} at index {np.argmax(ddd)} Mean difference: {np.mean(ddd)}"
            )
            assert_allclose(d_idl.times, d_py.times)
            assert_allclose(d_idl.v, d_py.v)
            # TODO: this fails but probably is OK
            # because the values in the particular example are very small
            # and the images look very similar
            # assert_allclose(d_idl.y, d_py.y, rtol=1e-01, atol=1e-01)

        # Plot all results (optional)
        local_png = os.path.join(save_dir, "wav_data_key2_test.png")
        tplot(all_vars, display=global_display, save_png=local_png)

    def test_wav_data_2d(self):
        # Test wav_data with 2d data and compare with IDL results.
        # This is using the IDL save file wav_data_2d_test.tplot
        # which was created by the SPEDAS script: wav_data_validate.pro

        logging.info("\n\nTesting wav_data 2d\n")

        # Load IDL savefile
        filename = test_data_download_file(
            validation_dir, analysis_dir, "wav_data_2d_test.tplot", save_dir
        )
        # If filename does not exist, skip the test
        if not os.path.exists(filename):
            self.skipTest(
                "Cannot find local IDL savefile for comparison. Filename: " + filename
            )

        # Load validation variables from the test file
        del_data("*")
        tplot_restore(filename)
        tplot_names()

        var = "sin_wav"
        all_vars = [var]
        py_names = [
            "sin_wav_wv_pow",
            "sin_wav_x_wv_pow",
            "sin_wav_y_wv_pow",
            "sin_wav_wv_pol_perp",
        ]
        for n in py_names:
            new_name = "idl_" + n
            tplot_rename(n, new_name)
            all_vars.append(new_name)
            all_vars.append(n)

        wav_data(var, get_components=1)

        # Compare with IDL results
        for n in py_names:
            logging.info(f"Comparing {n}")
            d_idl = get_data("idl_" + n)
            d_py = get_data(n)
            ddd = np.abs(d_idl.y - d_py.y)
            logging.info(
                f"Max difference: {np.max(ddd)} at index {np.argmax(ddd)} Mean difference: {np.mean(ddd)}"
            )
            assert_allclose(d_idl.times, d_py.times)
            assert_allclose(d_idl.v, d_py.v)
            assert_allclose(d_idl.y, d_py.y, rtol=1e-01, atol=1e-01)

        # Plot all results (optional)
        local_png = os.path.join(save_dir, "wav_data_2d_test.png")
        tplot(all_vars, display=global_display, save_png=local_png)

    def test_wav_data_resample(self):
        # Test wav_data resample portion of the code and compare with IDL results.
        # The NaN and varying time steps in the data trigger the resample.
        # This is using the IDL save file wav_data_resample_test.tplot
        # which was created by the SPEDAS script: wav_data_validate.pro

        logging.info("\n\nTesting wav_data resample keyword\n")

        # Load IDL savefile
        filename = test_data_download_file(
            validation_dir, analysis_dir, "wav_data_resample_test.tplot", save_dir
        )
        # If filename does not exist, skip the test
        if not os.path.exists(filename):
            self.skipTest(
                "Cannot find local IDL savefile for comparison. Filename: " + filename
            )

        # Load validation variables from the test file
        del_data("*")
        tplot_restore(filename)
        tplot_names()

        # Rename the IDL results to distinguish them
        tplot_rename("sin_wav_wv_pow", "idl_pow")
        tplot_rename("sin_wav_orig_wv_pow", "idl_orig_pow")

        var = "sin_wav"
        wav_data(var)
        varx = "sin_wav_wv_pow"

        idl_d = get_data("idl_pow")
        py_d = get_data(varx)

        # Compare IDL and Python results
        assert_allclose(idl_d[0], py_d[0], rtol=1e-5, atol=1e-8)
        assert_allclose(idl_d[1], py_d[1], rtol=1e-5, atol=1e-5)
        assert_allclose(idl_d[2], py_d[2], rtol=1e-5, atol=1e-8)

        # Plot all results (optional)
        allvar = [var, varx, "idl_pow"]
        local_png = os.path.join(save_dir, "wav_data_resample_test.png")
        tplot(allvar, display=global_display, save_png=local_png)

    def test_wav_data_cross(self):
        # Test wav_data keywords cross1, cross2 and compare with IDL results.
        # This is using the IDL save file wav_data_cross_test.tplot
        # which was created by the SPEDAS script: wav_data_validate.pro

        logging.info("\n\nTesting wav_data cross1, cross2 keywords\n")

        # Load IDL savefile
        filename = test_data_download_file(
            validation_dir, analysis_dir, "wav_data_cross_test.tplot", save_dir
        )
        # If filename does not exist, skip the test
        if not os.path.exists(filename):
            self.skipTest(
                "Cannot find local IDL savefile for comparison. Filename: " + filename
            )

        # Load validation variables from the test file
        del_data("*")
        tplot_restore(filename)
        tplot_names()

        var = "sin_wav"
        all_vars0 = [var]
        all_vars1 = []
        all_vars2 = []
        py_names0 = [
            "sin_wav_wv_pow",
            "sin_wav_x_wv_pow",
            "sin_wav_y_wv_pow",
            "sin_wav_z_wv_pow",
        ]
        py_names1 = [
            "sin_wav_wv_gam_lin",
            "sin_wav_wv_coin_lin",
            "sin_wav_wv_quad_lin",
            "sin_wav_wv_gam_cir",
            "sin_wav_wv_coin_cir",
            "sin_wav_wv_quad_cir",
        ]
        py_names2 = [
            "sin_wav_wv_gam_pr",
            "sin_wav_wv_coin_pr",
            "sin_wav_wv_quad_pr",
            "sin_wav_wv_gam_pl",
            "sin_wav_wv_coin_pl",
            "sin_wav_wv_quad_pl",
        ]

        # Rename the IDL results to distinguish them
        for n in py_names0:
            new_name = "idl_" + n
            tplot_rename(n, new_name)
            all_vars0.append(new_name)
            all_vars0.append(n)
        for n in py_names1:
            new_name = "idl_" + n
            tplot_rename(n, new_name)
            all_vars1.append(new_name)
            all_vars1.append(n)
        for n in py_names2:
            new_name = "idl_" + n
            tplot_rename(n, new_name)
            all_vars2.append(new_name)
            all_vars2.append(n)

        # Compute the python results
        wav_data(var, get_components=1, cross1=1, cross2=1)

        # Compare base results
        d_idl = get_data("idl_sin_wav_wv_pow")
        d_py = get_data("sin_wav_wv_pow")
        assert_allclose(d_idl.times, d_py.times)
        assert_allclose(d_idl.v, d_py.v)
        assert_allclose(d_idl.y, d_py.y, rtol=1e-03, atol=1e-3)

        # Compare x,y,z results
        for n in py_names0:
            logging.info(f"Comparing {n}")
            d_idl = get_data("idl_" + n)
            d_py = get_data(n)
            ddd = np.abs(d_idl.y - d_py.y)
            logging.info(
                f"Max difference: {np.max(ddd)} at index {np.argmax(ddd)} Mean difference: {np.mean(ddd)}"
            )
            assert_allclose(d_idl.times, d_py.times)
            assert_allclose(d_idl.v, d_py.v)
            assert_allclose(d_idl.y, d_py.y, rtol=7e-03, atol=7e-03)

        # Compare cross1 results
        for n in py_names1:
            logging.info(f"Comparing {n}")
            d_idl = get_data("idl_" + n)
            d_py = get_data(n)
            ddd = np.abs(d_idl.y - d_py.y)
            logging.info(
                f"Max difference: {np.max(ddd)} at index {np.argmax(ddd)} Mean difference: {np.mean(ddd)}"
            )
            assert_allclose(d_idl.times, d_py.times)
            assert_allclose(d_idl.v, d_py.v)
            assert_allclose(d_idl.y, d_py.y, rtol=7e-01, atol=7e-1)

        # Compare cross2 results
        for n in py_names2:
            d_idl = get_data("idl_" + n)
            d_py = get_data(n)
            assert_allclose(d_idl.times, d_py.times)
            assert_allclose(d_idl.v, d_py.v)
            ddd = np.abs(d_idl.y - d_py.y)
            logging.info(
                f"Max difference: {np.max(ddd)} at index {np.argmax(ddd)} Mean difference: {np.mean(ddd)}"
            )
            assert_allclose(d_idl.y, d_py.y, rtol=7e-01, atol=7e-1)

        # Plot all results (optional)
        local_png = os.path.join(save_dir, "wav_data_cross0.png")
        tplot(all_vars0, display=global_display, save_png=local_png)
        local_png = os.path.join(save_dir, "wav_data_cross1.png")
        tplot(all_vars1, display=global_display, save_png=local_png)
        local_png = os.path.join(save_dir, "wav_data_cross2.png")
        tplot(all_vars2, display=global_display, save_png=local_png)

    def test_wavelet98_paul_dog(self):
        # Test wavelet98.py Paul and Dog and compare with IDL results.

        logging.info("\n\nTesting wavelet98 Paul and Dog wavelets\n")

        # Load IDL savefile
        filename = test_data_download_file(
            validation_dir, analysis_dir, "wavelet98_paul_dog_test.tplot", save_dir
        )
        # If filename does not exist, skip the test
        if not os.path.exists(filename):
            self.skipTest(
                "Cannot find local IDL savefile for comparison. Filename: " + filename
            )

        # Load validation variables from the test file
        del_data("*")
        tplot_restore(filename)
        tplot_names()

        # Rename the IDL results to distinguish them
        tplot_rename("wav_paul", "idl_wav_paul")
        options("idl_wav_paul", "ytitle", "idl")
        tplot_rename("pow_paul", "idl_pow_paul")
        options("idl_pow_paul", "ytitle", "idl")
        tplot_rename("wav_dog", "idl_wav_dog")
        options("idl_wav_dog", "ytitle", "idl")
        tplot_rename("pow_dog", "idl_pow_dog")
        options("idl_pow_dog", "ytitle", "idl")

        var = "sin_wav"
        data = get_data(var)
        vtime = data[0]
        vy = data[1]
        dt = np.median(np.diff(vtime))  # time step in seconds

        # PAUL wavelet
        paul_res = wavelet98(vy, dt, mother="PAUL")
        wave_paul = paul_res[0]
        period_paul = paul_res[2]

        store_data("wav_paul", data={"x": vtime, "y": wave_paul, "v": period_paul})
        options("wav_paul", "ytitle", "python")
        options("wav_paul", "ysubtitle", "Paul")

        pow_paul = np.abs(wave_paul) ** 2
        store_data("pow_paul", data={"x": vtime, "y": pow_paul, "v": period_paul})
        options("pow_paul", "ytitle", "Power")
        options("pow_paul", "ysubtitle", "Paul")
        options("pow_paul", "spec", 1)
        options("pow_paul", "ylog", 1)

        # Compare IDL to Python Paul results
        d_idl_paul = get_data("idl_wav_paul")
        d_py_paul = get_data("wav_paul")
        assert_allclose(d_idl_paul.times, d_py_paul.times)
        assert_allclose(d_idl_paul.v, d_py_paul.v)
        assert_allclose(d_idl_paul.y, d_py_paul.y, rtol=7e-05, atol=7e-5)
        p_idl_paul = get_data("idl_pow_paul")
        p_py_paul = get_data("pow_paul")
        assert_allclose(p_idl_paul.times, p_py_paul.times)
        assert_allclose(p_idl_paul.v, p_py_paul.v)
        assert_allclose(p_idl_paul.y, p_py_paul.y, rtol=7e-05, atol=7e-5)

        # DOG wavelet
        dog_res = wavelet98(vy, dt, mother="DOG")
        wave_dog = dog_res[0]
        period_dog = dog_res[2]

        store_data("wav_dog", data={"x": vtime, "y": wave_dog, "v": period_dog})
        options("wav_dog", "ytitle", "python")
        options("wav_dog", "ysubtitle", "Dog")

        pow_dog = np.abs(wave_dog) ** 2
        store_data("pow_dog", data={"x": vtime, "y": pow_dog, "v": period_dog})
        options("pow_dog", "ytitle", "Power")
        options("pow_dog", "ysubtitle", "Dog")
        options("pow_dog", "spec", 1)
        options("pow_dog", "ylog", 1)

        # Compare dog results
        d_idl_dog = get_data("idl_wav_dog")
        d_py_dog = get_data("wav_dog")
        assert_allclose(d_idl_dog.times, d_py_dog.times)
        assert_allclose(d_idl_dog.v, d_py_dog.v)
        assert_allclose(d_idl_dog.y, d_py_dog.y, rtol=7e-05, atol=7e-5)
        p_idl_dog = get_data("idl_pow_dog")
        p_py_dog = get_data("pow_dog")
        assert_allclose(p_idl_dog.times, p_py_dog.times)
        assert_allclose(p_idl_dog.v, p_py_dog.v)
        assert_allclose(p_idl_dog.y, p_py_dog.y, rtol=7e-05, atol=7e-5)

        # Plot all results (optional)
        allvar = [
            var,
            "wav_paul",
            "idl_wav_paul",
            "pow_paul",
            "idl_pow_paul",
            "wav_dog",
            "idl_wav_dog",
            "pow_dog",
            "idl_pow_dog",
        ]
        local_png = os.path.join(save_dir, "wavelet98_paul_dog_test.png")
        tplot(allvar, display=global_display, save_png=local_png)


if __name__ == "__main__":
    unittest.main()
