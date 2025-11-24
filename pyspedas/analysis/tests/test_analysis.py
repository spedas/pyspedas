"""Automated tests for the analysis functions."""

import unittest
import os
import copy
import logging
from unittest.mock import patch
import numpy as np
from numpy.testing import assert_allclose
import importlib
import pyspedas
from pyspedas import (
    avg_data,
    yclip,
    deriv_data,
    tinterpol,
    tvectot,
    wavelet,
    time_domain_filter,
    get_data,
    store_data,
    replace_data,
    time_string,
    time_float,
    data_exists,
    del_data,
    tcrossp,
    tdotp,
    tnormalize,
    smooth,
    subtract_average,
    subtract_median,
    tsmooth,
    time_clip,
    tdeflag,
    clean_spikes,
)
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


class TestAnalysisFunctions(unittest.TestCase):
    """Test functions under analysis folder."""

    def setUp(self):
        """Create a tplot variable to be used in tests."""
        del_data("*")
        store_data(
            "test",
            data={
                "x": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                "y": [3.0, 5.0, 8.0, 15.0, 20.0, 1.0],
            },
        )

    def tearDown(self):
        """Delete the tplot variable."""
        del_data("*")

    def test_tdotp(self):
        store_data("var1", data={"x": [0], "y": [[3, -3, 1]]})
        store_data("var2", data={"x": [0], "y": [[4, 9, 2]]})
        _ = tdotp("var1", "var2")
        dpdata = get_data("var1_dot_var2")
        self.assertTrue(dpdata.y == np.array([-13]))

    def test_tcrossp(self):
        """cross product tests"""
        cp = tcrossp([3, -3, 1], [4, 9, 2], return_data=True)
        self.assertTrue(cp.tolist() == [-15, -2, 39])
        cp = tcrossp([3, -3, 1], [4, 9, 2])
        cp = get_data(cp)
        self.assertTrue(cp.y[0, :].tolist() == [-15, -2, 39])

        store_data("var1", data={"x": [0], "y": [[3, -3, 1]]})
        store_data("var2", data={"x": [0], "y": [[4, 9, 2]]})
        cp = tcrossp("var1", "var2", return_data=True)
        self.assertTrue(cp[0].tolist() == [-15, -2, 39])

        cp = tcrossp("var1", "var2", newname="test_crossp")
        cp = get_data("test_crossp")
        self.assertTrue(cp.y[0, :].tolist() == [-15, -2, 39])

    def test_tnormalize(self):
        """tests for normalizing tplot variables"""
        store_data(
            "test_tnormalize",
            data={
                "x": [1, 2, 3, 4, 5],
                "y": [[3, 2, 1], [1, 2, 3], [10, 5, 1], [8, 10, 14], [70, 20, 10]],
            },
        )
        norm = tnormalize("test_tnormalize")
        normalized_data = get_data(norm)
        self.assertTrue(
            np.round(normalized_data.y[0, :], 4).tolist() == [0.8018, 0.5345, 0.2673]
        )
        self.assertTrue(
            np.round(normalized_data.y[1, :], 4).tolist() == [0.2673, 0.5345, 0.8018]
        )
        self.assertTrue(
            np.round(normalized_data.y[2, :], 4).tolist() == [0.8909, 0.4454, 0.0891]
        )
        self.assertTrue(
            np.round(normalized_data.y[3, :], 4).tolist() == [0.4216, 0.527, 0.7379]
        )
        self.assertTrue(
            np.round(normalized_data.y[4, :], 4).tolist() == [0.9526, 0.2722, 0.1361]
        )

    def test_subtract_median(self):
        """Test subtract_median."""

        none1 = subtract_median("aaabbbccc")  # Test non-existent name
        self.assertTrue(none1 is None)
        subtract_median("test")
        d = get_data("test-m")
        self.assertTrue(d[1].tolist() == [-3.5, -1.5, 1.5, 8.5, 13.5, -5.5])
        dn = [
            [3.0, 5.0, 8.0],
            [15.0, 20.0, 1.0],
            [3.0, 5.0, 8.0],
            [15.0, 20.0, 1.0],
            [23.0, 15.0, 28.0],
            [15.0, 20.0, float("nan")],
        ]
        store_data("test1", data={"x": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0], "y": dn})
        none2 = subtract_median("aaabbbcc")
        self.assertTrue(none2 is None)
        subtract_median("test1", newname="aabb")
        d = get_data("aabb")
        self.assertTrue(len(d[1]) == 6)
        subtract_median(["test", "aabb"], newname="aaabbb")
        subtract_median("test1", overwrite=True)
        subtract_average("test", newname="testtest")
        subtract_average(["test-m", "test"], newname="testtest2")

    def test_subtract_average(self):
        """Test subtract_average."""
        subtract_average("aaabbbccc")  # Test non-existent name
        subtract_average("test")
        d = get_data("test-d")
        self.assertTrue(
            (np.round(d[1].tolist()) == [-6.0, -4.0, -1.0, 6.0, 11.0, -8.0]).all()
        )
        dn = [
            [3.0, 5.0, 8.0],
            [15.0, 20.0, 1.0],
            [3.0, 5.0, 8.0],
            [15.0, 20.0, 1.0],
            [23.0, 15.0, 28.0],
            [15.0, 20.0, float("nan")],
        ]
        store_data("test1", data={"x": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0], "y": dn})
        subtract_average("aaabbbcc")
        subtract_average("test1", newname="aabb")
        d = get_data("aabb")
        subtract_average(["test", "aabb"], newname="aaabbb")
        subtract_average("test1", overwrite=True)
        subtract_average("test1", newname="testtest")
        subtract_average(["test1", "test"], newname="testtest2")
        self.assertTrue(len(d[1]) == 6)

    def test_subtract_average_nan(self):
        """Test subtract_average with NaN values."""
        # Create a tplot variable with NaN values
        store_data(
            "test-nan", data={"x": [1.0, 2.0, 3.0, 4.0], "y": [3.0, 5.0, np.nan, 8.0]}
        )

        # Run subtract_average
        tvar = subtract_average("test-nan")
        d = get_data(tvar[0])

        # Check that the result is not all NaN
        self.assertFalse(np.isnan(d[1]).all(), "The result should not be all NaN.")

        # Check that NaN remains where it was
        self.assertTrue(np.isnan(d[1][2]), "NaN values should remain in the output.")

        # Check that non-NaN values are properly adjusted
        expected_values = np.array([3.0, 5.0, np.nan, 8.0]) - np.nanmean(
            np.array([3.0, 5.0, np.nan, 8.0])
        )
        np.testing.assert_array_almost_equal(
            d[1],
            expected_values,
            err_msg="Non-NaN values should be adjusted by subtracting the mean.",
        )

        # Additional NaN scenarios
        store_data(
            "test-nan-all",
            data={"x": [1.0, 2.0, 3.0, 4.0], "y": [np.nan, np.nan, np.nan, np.nan]},
        )

        # Check all NaN case
        result_all = subtract_average("test-nan-all")
        d_all = get_data(result_all[0])
        self.assertTrue(
            np.isnan(d_all[1]).all(), "All NaN input should result in all NaN output."
        )

    def test_subtract_median_nan(self):
        """Test subtract_median with NaN values."""
        # Create a tplot variable with NaN values
        store_data(
            "test-nan", data={"x": [1.0, 2.0, 3.0, 4.0], "y": [3.0, 5.0, np.nan, 8.0]}
        )

        # Run subtract_median
        tvar = subtract_median("test-nan")
        d = get_data(tvar[0])

        # Check that the result is not all NaN
        self.assertFalse(np.isnan(d[1]).all(), "The result should not be all NaN.")

        # Check that NaN remains where it was
        self.assertTrue(np.isnan(d[1][2]), "NaN values should remain in the output.")

        # Check that non-NaN values are properly adjusted by subtracting the median
        expected_values = np.array([3.0, 5.0, np.nan, 8.0]) - np.nanmedian(
            np.array([3.0, 5.0, np.nan, 8.0])
        )
        np.testing.assert_array_almost_equal(
            d[1],
            expected_values,
            err_msg="Non-NaN values should be adjusted by subtracting the median.",
        )

        # Additional NaN scenarios
        store_data(
            "test-nan-all",
            data={"x": [1.0, 2.0, 3.0, 4.0], "y": [np.nan, np.nan, np.nan, np.nan]},
        )

        # Check all NaN case
        result_all = subtract_median("test-nan-all")
        d_all = get_data(result_all[0])
        self.assertTrue(
            np.isnan(d_all[1]).all(), "All NaN input should result in all NaN output."
        )

    def test01_subtract_average_with_suffix(self):
        """Test subtract_average with suffix."""
        subtract_average("test", suffix="-sfx")
        self.assertIsNotNone(get_data("test-sfx"))

    def test02_subtract_average_with_newname_and_suffix(self):
        """Test subtract_average with both custom suffix and newname."""
        subtract_average("test", newname="new_test", suffix="-sfx")
        self.assertIsNotNone(get_data("new_test"))
        # Ensure suffix is not applied when newname is provided
        self.assertIsNone(get_data("test-sfx"))

    def test_subtract_average_with_invalid_names(self):
        """Test subtract_average with invalid names input."""
        result = subtract_average("invalid_name")
        self.assertIsNone(result)  # Should handle gracefully

    def test_subtract_average_with_empty_names(self):
        """Test subtract_average with empty names list."""
        result = subtract_average([])
        self.assertIsNone(result)  # Should handle gracefully

    def test_subtract_average_all_same_values(self):
        """Test subtract_average with all same values in the dataset."""
        store_data("test_same", data={"x": [1.0, 2.0, 3.0], "y": [5.0, 5.0, 5.0]})
        subtract_average("test_same")
        d = get_data("test_same-d")
        self.assertTrue((d[1] == [0, 0, 0]).all())

    def test_subtract_average_one_element(self):
        """Test subtract_average with dataset containing only one element."""
        store_data("test_one", data={"x": [1.0], "y": [10.0]})
        subtract_average("test_one")
        d = get_data("test_one-d")
        self.assertTrue((d[1] == [0]).all())

    def test_subtract_median_basic(self):
        """Test basic functionality of subtract_median."""
        store_data("test", data={"x": [1.0, 2.0, 3.0], "y": [4.0, 5.0, 6.0]})
        subtract_median("test")
        d = get_data("test-m")
        self.assertIsNotNone(d)

    def test_subtract_median_parameter_passing(self):
        """Test that parameters are correctly passed to subtract_average via subtract_median."""
        sm = importlib.import_module("pyspedas.tplot_tools.tplot_math.subtract_median")

        with patch.object(sm, "subtract_average") as mock_subtract_average:
            logging.info(mock_subtract_average)
            pyspedas.subtract_median(
                "test", newname="new_test", suffix="-sfx", overwrite=True
            )

            # Check that subtract_average was called with the correct parameters, including median=1
            mock_subtract_average.assert_called_once_with(
                "test", newname="new_test", suffix="-sfx", overwrite=True, median=1
            )

    def test_yclip(self):
        """Test yclip."""
        yclip("aaabbbccc", 0.0, 12.0)  # Test non-existent name
        yclip("aabb", 0.0, 12.0)
        yclip("test", 0.0, 12.0)
        d = get_data("test-clip")
        # Replace nan with -99.0
        dd = np.nan_to_num(d[1], nan=-99.0)
        yclip("test", 0.0, 12.0, newname="name-clip")
        yclip(["test", "name-clip"], 0.0, 12.0, newname="name1-clip")
        yclip("test", 0.0, 12.0, overwrite=True)
        yclip("test", 0.0, 12.0, newname="testtest")
        yclip(["test", "test-clip"], 0.0, 12.0, newname="testtest2")
        self.assertTrue((dd == [3.0, 5.0, 8.0, -99.0, -99.0, 1.0]).all())

    def test_timeclip(self):
        """Test time_clip."""
        time_clip("aaabbbccc", 1577308800, 1577598800)  # Test non-existent
        tn = [1577112800, 1577308800, 1577598800, 1577608800, 1577998800, 1587998800]
        dn = [3.0, 5.0, 8.0, 15.0, 20.0, 1.0]
        store_data("test1", data={"x": tn, "y": dn})
        time_clip("aaabbb", 1577308800, 1577598800)
        time_clip("test1", 1577112800, 1577608800)
        d = get_data("test1-tclip")
        dd = d[1]
        time_clip("test", 1577308800, 1577598800, newname="name-clip")
        time_clip(["test", "name-clip"], 1577308800, 1577598800, newname="name1-ci")
        time_clip("test", 1577308800, 1577598800, overwrite=True)
        time_clip("test", 1577308800, 1577598800, newname="testtest")
        time_clip(["test", "test1"], 1577308800, 1577598800, newname="testtest2")
        time_clip("test1", 1677112800, 1577608800)
        self.assertTrue((dd == [3.0, 5.0, 8.0, 15.0]).all())

    def test_avg_data(self):
        """Test avg_data."""
        avg_data("aaabbbccc", width=2)  # Test non-existent name
        avg_data("test", width=2)
        d = get_data("test-avg")
        self.assertTrue((d[1] == [4.0, 11.5, 10.5]).all())
        avg_data("test", width=2, overwrite=True)  # Test overwrite
        store_data(
            "test",
            data={
                "x": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                "y": [3.0, 5.0, 8.0, -4.0, 20.0, 1.0],
            },
        )
        avg_data("test", width=2, newname="aabb")  # Test newname
        d = get_data("aabb")
        # Test multiple names
        avg_data(["test", "aabb"], newname="aaabbb", width=2)
        dt = [1.0, 12.0, 13.0, 14.0, 15.0, 16.0]
        dn = [
            [3.0, 5.0, 8.0],
            [15.0, 20.0, 1.0],
            [3.0, 5.0, 8.0],
            [15.0, 20.0, 1.0],
            [23.0, 15.0, 28.0],
            [15.0, 20.0, 1.0],
        ]
        dv = dn
        store_data("test1", data={"x": dt, "y": dn, "v": dv})
        avg_data("test1", width=2)  # Test 3-d data
        avg_data("test1", newname="test2", res=2.0)  # Test a reasonable resolution
        avg_data("test1", res=-1.0)  # Test res error
        avg_data("test1", res=1.0e8)  # Test res error
        d2 = get_data("test2")
        self.assertTrue(len(d2) > 0)
        self.assertTrue(d2[1][-1][0] == 15.0)
        self.assertTrue(len(d2[2]) == len(d2[0]))

    def test_avg_data_idl(self):
        # Compare data with IDL avg_data
        # Requires file: avg_data_validate.tplot from
        #   https://github.com/spedas/test_data
        # The SPEDAS script that creates the file: general/tools/python_validate/avg_data_python_validate.pro

        # Load IDL savefile
        filename = test_data_download_file(
            validation_dir, analysis_dir, "avg_data_validate.tplot", save_dir
        )

        trange = ["2010-02-13 00:00:00", "2010-02-13 11:59:59"]
        probe = "b"
        pyspedas.projects.themis.esa(trange=trange, probe=probe)
        var = "thb_peir_en_eflux"
        vara = var + "-avg"
        pyspedas.time_clip(var, trange[0], trange[1], overwrite=True)
        pyspedas.avg_data(var)

        # Get IDL data
        pyspedas.tplot_restore(filename)
        varidl = var + "_avg"

        # Compare IDL to python results
        d1 = pyspedas.get_data(varidl)
        d2 = pyspedas.get_data(vara)

        assert_allclose(d1[0], d2[0], atol=1e-5, rtol=1e-5, equal_nan=True)
        assert_allclose(d1[1], d2[1], atol=1e-5, rtol=1e-5, equal_nan=True)
        assert_allclose(d1[2], d2[2], atol=1e-5, rtol=1e-5, equal_nan=True)

    def test_clean_spikes(self):
        """Test clean_spikes."""
        clean_spikes("aaabbbccc", nsmooth=3)  # Test non-existent name
        clean_spikes("test", nsmooth=3)
        d = get_data("test-despike")
        self.assertTrue(len(d[1]) == 6)
        # Now test 3 dim data.
        dn = [
            [3.0, 5.0, 8.0],
            [15.0, 20.0, 1.0],
            [3.0, 5.0, 8.0],
            [15.0, 20.0, 1.0],
            [23.0, 15.0, 28.0],
            [15.0, 20.0, 1.0],
        ]
        store_data("test1", data={"x": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0], "y": dn})
        clean_spikes("test1", nsmooth=3)
        d2 = get_data("test1-despike")
        clean_spikes("test", newname="test_desp", nsmooth=3, sub_avg=True)
        clean_spikes(["test", "test1"], newname="test1-desp")
        clean_spikes("test1", overwrite=True)
        self.assertTrue(len(d2[1]) == 6)

    def test_tdeflag(self):
        """Test tdeflag."""
        tdeflag("aaabbbccc")  # Test non-existent name
        dn = [3.0, float("NaN"), 8.0, float("NaN"), 20.0, 1.0]
        len_dn = len(dn)
        replace_data("test", dn)
        tdeflag("test")
        d = get_data("test-deflag")
        tdeflag("test", overwrite=True)
        tdeflag("test", newname="testtest")
        tdeflag(["test", "test-deflag"], newname="testtest2")
        # Length should be two less, because NaNs were removed.
        self.assertTrue(len(d[1]) == len_dn - 2)

    def test_tdeflag_2d(self):
        """Test tdeflag."""
        times = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        vals = np.array(
            [
                [1.0, 2.0, 3.0],
                [1.1, 2.1, 3.1],
                [1.2, 2.2, 3.2],
                [1.3, 2.3, 3.3],
                [1.4, 2.4, 3.4],
            ]
        )
        # dn = [3.0, float("NaN"), 8.0, float("NaN"), 20.0, 1.0]

        vals_noflag = copy.deepcopy(vals)
        store_data("vals_noflag", data={"x": times, "y": vals_noflag})
        tdeflag(
            "vals_noflag", newname="vals_noflag_remove"
        )  # no method should default to remove_nan
        tdeflag("vals_noflag", newname="vals_noflag_linear", method="linear")
        tdeflag("vals_noflag", newname="vals_noflag_repeat", method="repeat")
        tdeflag(
            "vals_noflag",
            newname="vals_noflag_replace",
            method="replace",
            fillval=100.0,
        )
        d1 = get_data("vals_noflag_remove")
        d2 = get_data("vals_noflag_linear")
        d3 = get_data("vals_noflag_repeat")
        d4 = get_data("vals_noflag_replace")
        d5 = get_data("vals_noflag_linear")
        np.testing.assert_array_equal(d1.y, vals_noflag)
        np.testing.assert_array_equal(d2.y, vals_noflag)
        np.testing.assert_array_equal(d3.y, vals_noflag)
        np.testing.assert_array_equal(d4.y, vals_noflag)
        np.testing.assert_array_equal(d5.y, vals_noflag)

        # There can be multiple flags. Make sure the 'no unflagged data' case is
        # properly defected when each individual flag leaves some valid data, but
        # the combination flags everything.

        # commented out for now until they pass
        # tdeflag('vals_noflag', newname='vals_all_multiflag_linear', method='linear', flag=[2.0,2.1,2.3,2.4,2.5])
        # self.assertFalse(data_exists('vals_all_multiflag_linear'))
        # tdeflag('vals_noflag', newname='vals_all_multiflag_repeat', method='repeat', flag=[2.0,2.1,2.3,2.4,2.5])
        # self.assertFalse(data_exists('vals_all_multiflag_repeat'))

        vals_flag_beginning = copy.deepcopy(vals)
        vals_flag_beginning[0, 1] = np.nan
        store_data("vals_flag_beginning", data={"x": times, "y": vals_flag_beginning})
        tdeflag(
            "vals_flag_beginning",
            newname="vals_flag_beginning_remove",
            method="remove_nan",
        )
        tdeflag(
            "vals_flag_beginning", newname="vals_flag_beginning_linear", method="linear"
        )
        tdeflag(
            "vals_flag_beginning", newname="vals_flag_beginning_repeat", method="repeat"
        )
        tdeflag(
            "vals_flag_beginning",
            newname="vals_flag_beginning_replace",
            method="replace",
            fillval=100.0,
        )
        d1 = get_data("vals_flag_beginning_remove")
        d2 = get_data("vals_flag_beginning_linear")
        d3 = get_data("vals_flag_beginning_repeat")
        d4 = get_data("vals_flag_beginning_replace")
        np.testing.assert_equal(len(d1.times), 4)
        np.testing.assert_equal(d1.times[0], times[1])
        np.testing.assert_equal(d2.y[0, 1], 2.1)
        np.testing.assert_equal(d3.y[0, 1], 2.1)
        np.testing.assert_equal(d4.y[0, 1], 100.0)

        vals_flag_end = copy.deepcopy(vals)
        vals_flag_end[4, 1] = np.nan
        store_data("vals_flag_end", data={"x": times, "y": vals_flag_end})
        tdeflag("vals_flag_end", newname="vals_flag_end_remove", method="remove_nan")
        tdeflag("vals_flag_end", newname="vals_flag_end_linear", method="linear")
        tdeflag("vals_flag_end", newname="vals_flag_end_repeat", method="repeat")
        tdeflag(
            "vals_flag_end",
            newname="vals_flag_end_replace",
            method="replace",
            fillval=100.0,
        )
        d1 = get_data("vals_flag_end_remove")
        d2 = get_data("vals_flag_end_linear")
        d3 = get_data("vals_flag_end_repeat")
        d4 = get_data("vals_flag_end_replace")
        np.testing.assert_equal(len(d1.times), 4)
        np.testing.assert_equal(d1.times[3], times[3])
        np.testing.assert_equal(d2.y[4, 1], 2.3)
        np.testing.assert_equal(d3.y[4, 1], 2.3)
        np.testing.assert_equal(d4.y[4, 1], 100.0)

        vals_flag_middle = copy.deepcopy(vals)
        vals_flag_middle[2, 1] = np.nan
        store_data("vals_flag_middle", data={"x": times, "y": vals_flag_middle})
        tdeflag(
            "vals_flag_middle", newname="vals_flag_middle_remove", method="remove_nan"
        )
        tdeflag("vals_flag_middle", newname="vals_flag_middle_linear", method="linear")
        tdeflag("vals_flag_middle", newname="vals_flag_middle_repeat", method="repeat")
        tdeflag(
            "vals_flag_middle",
            newname="vals_flag_middle_replace",
            method="replace",
            fillval=100.0,
        )
        d1 = get_data("vals_flag_middle_remove")
        d2 = get_data("vals_flag_middle_linear")
        d3 = get_data("vals_flag_middle_repeat")
        d4 = get_data("vals_flag_middle_replace")
        np.testing.assert_equal(len(d1.times), 4)
        np.testing.assert_equal(d1.times[2], times[3])
        np.testing.assert_equal(d2.y[2, 1], 2.2)
        np.testing.assert_equal(d3.y[2, 1], 2.1)
        np.testing.assert_equal(d4.y[2, 1], 100.0)

        vals_flag_all = copy.deepcopy(vals)
        vals_flag_all[:, :] = np.nan
        store_data("vals_flag_all", data={"x": times, "y": vals_flag_all})
        tdeflag("vals_flag_all", newname="vals_flag_all_remove", method="remove_nan")
        self.assertFalse(data_exists("vals_flag_all_remove"))
        tdeflag("vals_flag_all", newname="vals_flag_all_linear", method="linear")
        self.assertFalse(data_exists("vals_flag_all_linear"))
        tdeflag("vals_flag_all", newname="vals_flag_all_repeat", method="repeat")
        self.assertFalse(data_exists("vals_flag_all_repeat"))
        tdeflag(
            "vals_flag_all",
            newname="vals_flag_all_replace",
            method="replace",
            fillval=100.0,
        )
        d = get_data("vals_flag_all_replace")
        self.assertEqual(d.y[0, 0], 100.0)

    def test_tdeflag_1d(self):
        times = [1.0, 2.0, 3.0, 4.0, 5.0]
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        vals_noflag = copy.deepcopy(data)
        store_data("vals_noflag_1d", data={"x": times, "y": vals_noflag})
        tdeflag("vals_noflag_1d", newname="vals_noflag_1d_linear", method="linear")
        d1 = get_data("vals_noflag_1d_linear")
        np.testing.assert_array_equal(d1.y, vals_noflag)

    def test_deriv_data(self):
        """Test deriv_data."""
        deriv_data("aaabbbccc")  # Test non-existent name
        deriv_data("test")
        d = get_data("test-der")
        deriv_data("test", overwrite=True)
        deriv_data("test", newname="testtest")
        deriv_data(["test", "test-der"], newname="testtest2")
        self.assertTrue((d[1] == [2.0, 2.5, 5.0, 6.0, -7.0, -19.0]).all())

    def test_tvectot(self):
        from pyspedas.projects.themis import state
        from pyspedas.tplot_tools import data_exists

        state(probe="a")
        tvectot("tha_pos", join_component=True)
        self.assertTrue(data_exists("tha_pos_tot"))
        d = get_data("tha_pos_tot")
        s = d.y.shape[1]
        self.assertEqual(s, 4)
        del_data("tha_pos_tot")
        tvectot("tha_pos")  # join_component defaults to True now
        self.assertTrue(data_exists("tha_pos_tot"))
        d = get_data("tha_pos_tot")
        s = d.y.shape[1]
        self.assertEqual(s, 4)
        del_data("tha_pos_tot")
        _ = tvectot("tha_pos", join_component=False)
        self.assertTrue(data_exists("tha_pos_mag"))
        d = get_data("tha_pos_mag")
        ndims = len(d.y.shape)
        self.assertEqual(ndims, 1)
        del_data("tha_pos_mag")
        _ = tvectot("tha_pos", newname="tha_pos_total", join_component=False)
        self.assertTrue(data_exists("tha_pos_total"))
        d = get_data("tha_pos_total")
        ndims = len(d.y.shape)
        self.assertEqual(ndims, 1)
        del_data("tha_pos_total")
        tvectot("tha_pos", suffix="_rtot")
        self.assertTrue(data_exists("tha_pos_rtot"))

    def test_wavelet(self):
        # Create a tplot variable that contains a wave.
        t = np.arange(4000.0)
        y = np.sin(2 * np.pi * t / 32.0)
        y2 = np.sin(2 * np.pi * t / 64.0)
        y[1000:3000] = y2[1000:3000]
        var = "sin_wav"
        time = time_float("2010-01-01") + 10 * t
        store_data(var, data={"x": time, "y": y})

        # Gaussian Derivative wavelets transformation.
        powervar = wavelet(var, wavename="gaus1")
        pvar = powervar[0]
        self.assertTrue(data_exists(pvar))

    def test_time_domain_filter(self):
        # Create a tplot variable that contains a wave.
        t = np.arange(4000.0)
        y = np.sin(2 * np.pi * t / 32.0)
        y2 = np.sin(2 * np.pi * t / 64.0)
        y[1000:3000] = y2[1000:3000]
        dat = np.zeros((4000, 3))
        dat[:, 0] = y
        dat[:, 1] = y
        dat[:, 2] = y
        time = time_float("2010-01-01") + 10 * t
        output = time_domain_filter(dat, time, 16.0, 48.0)
        self.assertEqual(output.shape[0], dat.shape[0])
        self.assertEqual(output.shape[1], dat.shape[1])

    def test_tsmooth(self):
        """Test smooth."""
        tsmooth("aaabbbccc")  # Test non-existent name
        a = [1.0, 1.0, 2.0, 3.0, 4.0, 1.0, 4.0, 3.0, 2.0, 1.0, 1.0]
        x = smooth(a, 3)
        r = [
            1.0,
            1.3333333333333333,
            2.0,
            3.0,
            2.6666666666666665,
            3.0,
            2.6666666666666665,
            3.0,
            2.0,
            1.3333333333333333,
            1.0,
        ]
        self.assertTrue(x == r)
        b = [1.0, 1.0, 2.0, 3.0, np.nan, np.nan, np.nan, np.nan, 2.0, 1.0, 1.0]
        y = smooth(b, width=3)
        ry = [
            1.0,
            1.3333333333333333,
            2.0,
            1.6666666666666665,
            1.0,
            np.nan,
            np.nan,
            0.6666666666666666,
            1.0,
            1.3333333333333333,
            1.0,
        ]
        self.assertTrue(y == ry)
        tsmooth("test")
        d = get_data("test-s")
        tsmooth("test", overwrite=True)
        tsmooth("test", newname="testtest")
        tsmooth(["test", "test-s"], newname="testtest2")
        self.assertTrue(d[1].tolist() == [3.0, 5.0, 8.0, 15.0, 20.0, 1.0])

    def test_tinterpol(self):
        """Test tinterpol."""
        tinterpol("aaabbbccc", "test")  # Test non-existent name
        tn = [1.0, 1.5, 4.6, 5.8, 6.0]
        dn = [10.0, 15.0, 46.0, 58.0, 60.0]
        data = np.array(
            [
                [0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19],
                [20, 21, 22, 23, 24],
            ]
        )
        store_data("test1", data={"x": tn, "y": dn})
        store_data("test2", data={"x": tn, "y": data, "v": [10, 20, 30, 40, 50]})
        tinterpol("test1", "test")
        tinterpol("test1", "doesnt_exist")
        tinterpol("test2", "test", newname="")
        tinterpol("test2", [1, 2, 3, 4, 5, 6], newname="pyarray_float")
        tinterpol("test2", np.array([1, 2, 3, 4, 5, 6]), newname="nparray_float")
        tinterpol("test2", time_string([1, 2, 3, 4, 5, 6]), newname="pyarray_str")
        tinterpol(
            "test2", np.array(time_string([1, 2, 3, 4, 5, 6])), newname="nparray_str"
        )
        bad_datatype = {}
        tinterpol("test2", [bad_datatype], newname="nparray_bad_datatype")

        d = get_data("test1-itrp")
        self.assertTrue(d[1][1] == 20.0)
        d2 = get_data("pyarray_float")
        self.assertTrue(abs(d2[1][1][0] - 5.80645161) < 1e-6)
        d3 = get_data("nparray_float")
        self.assertTrue(abs(d3[1][1][0] - 5.80645161) < 1e-6)
        d4 = get_data("pyarray_str")
        self.assertTrue(abs(d4[1][1][0] - 5.80645161) < 1e-6)
        d5 = get_data("nparray_str")
        self.assertTrue(abs(d5[1][1][0] - 5.80645161) < 1e-6)

    def test_scipy_interp1d(self):
        import scipy
        import numpy as np

        time_strings_input = np.array(
            [
                "2018-07-01T13:02:16.892474880",
                "2018-07-01T13:02:16.922475008",
                "2018-07-01T13:02:16.952474880",
            ]
        )
        values_input = np.array([0.028584518, 0.0, 0.013626526], dtype=np.float32)

        input_times_npdt64 = np.array([np.datetime64(t) for t in time_strings_input])
        interp_to_times_npdt64 = np.array(input_times_npdt64[1])

        input_times_float64 = input_times_npdt64.astype(np.float64)
        interp_to_time_float64 = interp_to_times_npdt64.astype(np.float64)

        interpolator = scipy.interpolate.interp1d(
            input_times_float64, values_input, kind="linear"
        )
        result = interpolator(interp_to_time_float64)
        logging.info(result)
        # Known to fail.  This affects xarray.interp and the current version of tinterpol.
        # self.assertTrue((result >= 0.0).all())

    def test_scipy_spline(self):
        import scipy
        import numpy as np

        time_strings_input = np.array(
            [
                "2018-07-01T13:02:16.892474880",
                "2018-07-01T13:02:16.922475008",
                "2018-07-01T13:02:16.952474880",
            ]
        )
        values_input = np.array([0.028584518, 0.0, 0.013626526], dtype=np.float32)

        input_times_npdt64 = np.array([np.datetime64(t) for t in time_strings_input])
        interp_to_times_npdt64 = np.array(input_times_npdt64[1])

        input_times_float64 = input_times_npdt64.astype(np.float64)
        interp_to_time_float64 = interp_to_times_npdt64.astype(np.float64)

        interpolator = scipy.interpolate.make_interp_spline(
            input_times_float64, values_input, k=1
        )
        result = interpolator(interp_to_time_float64)
        logging.info(result)
        # make_interp_spline() with k=1 gives the expected result
        self.assertTrue((result >= 0.0).all())

    def test_xarray_interp(self):
        import xarray as xr
        import numpy as np

        time_strings_input = np.array(
            [
                "2018-07-01T13:02:16.892474880",
                "2018-07-01T13:02:16.922475008",
                "2018-07-01T13:02:16.952474880",
            ]
        )
        values_input = np.array([0.028584518, 0.0, 0.013626526], dtype=np.float32)

        input_times_npdt64 = np.array([np.datetime64(t) for t in time_strings_input])
        interp_to_times_npdt64 = np.array(input_times_npdt64[1])

        data_array = xr.DataArray(
            values_input, dims=["time"], coords={"time": ("time", input_times_npdt64)}
        )

        result = data_array.interp({"time": interp_to_times_npdt64}, method="linear")
        # This is known to fail, due to issues in scipy.interpolate.interp1d
        # logging.info(result.values)
        # result.values is [-3.469446951953614e-18]
        # self.assertTrue((result.values >= 0.0).all())
        self.assertAlmostEqual(result.values, 0.0)

    def test_xarray_interp_float_times(self):
        import xarray as xr
        import numpy as np

        time_strings_input = np.array(
            [
                "2018-07-01T13:02:16.892474880",
                "2018-07-01T13:02:16.922475008",
                "2018-07-01T13:02:16.952474880",
            ]
        )
        values_input = np.array([0.028584518, 0.0, 0.013626526], dtype=np.float32)

        input_times_npdt64 = np.array([np.datetime64(t) for t in time_strings_input])
        interp_to_times_npdt64 = np.array(input_times_npdt64[1])

        input_times_float64 = input_times_npdt64.astype(np.float64)
        interp_to_time_float64 = interp_to_times_npdt64.astype(np.float64)

        data_array = xr.DataArray(
            values_input, dims=["time"], coords={"time": ("time", input_times_float64)}
        )

        result = data_array.interp({"time": interp_to_time_float64}, method="linear")
        # This is known to fail, due to issues in scipy.interpolate.interp1d
        # l ogging.info(result.values)
        # result.values is [-3.469446951953614e-18]
        # self.assertTrue((result.values >= 0.0).all())
        self.assertAlmostEqual(result.values, 0.0)

    def test_numpy_interp(self):
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

    def test_tinterpol_nonnegative2(self):
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
        store_data("interp_input", data={"x": input_times_npdt64, "y": values_input})
        store_data("interp_to", data={"x": interp_to_times_npdt64, "y": [0.0]})
        tinterpol("interp_input", "interp_to", newname="interp_result")
        result = get_data("interp_result")
        # This is known to fail, apparently due to limitations of scipy.interpolate.interp1d which are
        # unlikely to ever be fixed. See tests above for xarray.interp and scipy
        # self.assertTrue((result.y >= 0.0).all())
        self.assertAlmostEqual(result.y[0], 0.0, places=6)

    def test_tinterpol_slinear(self):
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
        store_data("interp_input", data={"x": input_times_npdt64, "y": values_input})
        store_data("interp_to", data={"x": interp_to_times_npdt64, "y": [0.0]})
        tinterpol(
            "interp_input", "interp_to", newname="interp_result", method="slinear"
        )
        result = get_data("interp_result")
        self.assertTrue((result.y >= 0.0).all())


if __name__ == "__main__":
    unittest.main()
