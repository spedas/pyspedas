"""Automated tests for tplot math and utility functions."""

import unittest
import math
import numpy as np
from numpy.testing import assert_array_equal
from pyspedas import (
    clean_spikes,
    smooth,
    tsmooth,
    tdotp,
    tcrossp,
    tnormalize,
    subtract_median,
    subtract_average,
    get_data,
    store_data,
    del_data,
    crop,
    add_across,
    add,
    subtract,
    multiply,
    divide,
    derive,
    tres,
    tpwrspc,
    pwr_spec,
    spec_mult,
    data_exists,
    time_float,
)


class BaseTestCase(unittest.TestCase):
    """Data to be used in tests."""

    def setUp(self):
        """Create a tplot variable to be used in tests."""
        store_data(
            "test",
            data={
                "x": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                "y": [3.0, 5.0, 8.0, 15.0, 20.0, 1.0],
            },
        )


class AnalysisTestCases(BaseTestCase):
    """Test functions under tplot_math, and some other utilities."""

    def test_tdotp(self):
        store_data("var1", data={"x": [0], "y": [[3, -3, 1]]})
        store_data("var2", data={"x": [0], "y": [[4, 9, 2]]})
        dp = tdotp("var1", "var2")
        dpdata = get_data("var1_dot_var2")
        self.assertTrue(dpdata.y == np.array([-13]))
        dp = tdotp("var1_doesnt_exist", "var2")
        self.assertIsNone(dp)
        dp = tdotp("var1", "var2_doesnt_exist")
        self.assertIsNone(dp)

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
        self.assertTrue(np.round(normalized_data.y[0, :], 4).tolist() == [0.8018, 0.5345, 0.2673])
        self.assertTrue(np.round(normalized_data.y[1, :], 4).tolist() == [0.2673, 0.5345, 0.8018])
        self.assertTrue(np.round(normalized_data.y[2, :], 4).tolist() == [0.8909, 0.4454, 0.0891])
        self.assertTrue(np.round(normalized_data.y[3, :], 4).tolist() == [0.4216, 0.527, 0.7379])
        self.assertTrue(np.round(normalized_data.y[4, :], 4).tolist() == [0.9526, 0.2722, 0.1361])

    def test_subtract_median(self):
        """Test subtract_median."""
        subtract_median("aaabbbccc")  # Test non-existent name
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
        subtract_median("aaabbbcc")
        subtract_median("test1", newname="aabb")
        d = get_data("aabb")
        self.assertTrue(len(d[1]) == 6)
        subtract_median(["test", "aabb"], newname="aaabbb")
        subtract_median("test1", overwrite=1)
        subtract_average("test", newname="testtest")
        subtract_average(["test-m", "test"], newname="testtest2")

    def test_subtract_average(self):
        """Test subtract_average."""
        subtract_average("aaabbbccc")  # Test non-existent name
        subtract_average("test")
        d = get_data("test-d")
        self.assertTrue((np.round(d[1].tolist()) == [-6.0, -4.0, -1.0, 6.0, 11.0, -8.0]).all())
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
        self.assertTrue(len(d[1]) == 6)
        subtract_average(["test", "aabb"], newname="aaabbb")
        subtract_average("test1", overwrite=1)
        subtract_average("test1", newname="testtest")
        subtract_average(["test1", "test"], newname="testtest2")

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
        clean_spikes("test1", overwrite=1)
        self.assertTrue(len(d2[1]) == 6)

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
        tsmooth("test", overwrite=1)
        tsmooth("test", newname="testtest")
        tsmooth(["test", "test-s"], newname="testtest2")
        self.assertTrue(d[1].tolist() == [3.0, 5.0, 8.0, 15.0, 20.0, 1.0])

    def test_tplot_arithmetic(self):
        del_data("*")
        times = [0.0, 1.0, 2.0, 3.0, 4.0]
        dat1 = [1.0, 2.0, 3.0, 4.0, 5.0]
        dat2 = [10.0, 20.0, 30.0, 40.0, 50.0]
        store_data("v1", data={"x": times, "y": dat1})
        store_data("v2", data={"x": times, "y": dat2})
        add("v1", "v2", newname="sum")
        subtract("v2", "v1", newname="diff")
        multiply("v1", "v2", newname="prod")
        divide("v2", "v1", newname="quot")
        derive("v2", newname="ddx")
        sum_t, sum_d = get_data("sum")
        diff_t, diff_d = get_data("diff")
        prod_t, prod_d = get_data("prod")
        quot_t, quot_d = get_data("quot")
        ddx_t, ddx_d = get_data("ddx")
        assert_array_equal(diff_d, np.array([9.0, 18.0, 27.0, 36.0, 45.0]))
        assert_array_equal(sum_d, np.array([11.0, 22.0, 33.0, 44.0, 55.0]))
        assert_array_equal(quot_d, np.array([10.0, 10.0, 10.0, 10.0, 10.0]))
        assert_array_equal(prod_d, np.array([10.0, 40.0, 90.0, 160.0, 250.0]))
        assert_array_equal(ddx_d, np.array([10.0, 10.0, 10.0, 10.0, 10.0]))
        dt = tres("v1")
        self.assertEqual(dt, 1.0)

    def test_tplot_spectools(self):
        del_data("*")
        # tpwrspc, pwrspc
        store_data("a", data={"x": range(100), "y": np.random.random(100)})
        tpwrspc("a")
        spec = get_data("a_pwrspc")
        self.assertEqual(len(spec.y), 1)
        self.assertTrue(data_exists("a_pwrspc"))
        # pwr_spec
        time = [time_float("2020-01-01") + i for i in range(10000)]
        quantity = [math.sin(i) for i in range(10000)]
        store_data("dp", data={"x": time, "y": quantity})
        pwr_spec("dp", newname="dp_pwrspec")
        # pyspedas.tplot("dp_pwrspec")
        self.assertTrue(data_exists("dp_pwrspec"))
        # spec_mult
        store_data(
            "h",
            data={
                "x": [0, 4, 8, 12, 16, 19, 21],
                "y": [
                    [8, 1, 1],
                    [100, 2, 3],
                    [4, 2, 47],
                    [4, 39, 5],
                    [5, 5, 99],
                    [6, 6, 25],
                    [7, -2, -5],
                ],
                "v": [
                    [1, 1, 50],
                    [2, 2, 3],
                    [100, 4, 47],
                    [4, 90, 5],
                    [5, 5, 99],
                    [6, 6, 25],
                    [7, 7, -5],
                ],
            },
        )
        spec_mult("h")
        hdat = get_data("h_specmult")
        assert_array_equal(
            hdat.y,
            np.array(
                [
                    [8, 1, 50],
                    [200, 4, 9],
                    [400, 8, 2209],
                    [16, 3510, 25],
                    [25, 25, 9801],
                    [36, 36, 625],
                    [49, -14, 25],
                ]
            ),
        )

    def test_add_across(self):
        del_data("*")
        # Add across every column in the data
        store_data(
            "d",
            data={
                "x": [2, 5, 8, 11, 14, 17, 21],
                "y": [
                    [1, 1, 50],
                    [2, 2, 3],
                    [100, 4, 47],
                    [4, 90, 5],
                    [5, 5, 99],
                    [6, 6, 25],
                    [7, 7, -5],
                ],
            },
        )
        add_across("d", newname="d_aa")
        daa = get_data("d_aa")
        assert_array_equal(daa.y, np.array([[52], [7], [151], [99], [109], [37], [9]]))

        # Add across specific columns in the data
        store_data(
            "b",
            data={
                "x": [2, 5, 8, 11, 14, 17, 20],
                "y": [
                    [1, 1, 1, 1, 1, 1],
                    [2, 2, 5, 4, 1, 1],
                    [100, 100, 3, 50, 1, 1],
                    [4, 4, 8, 58, 1, 1],
                    [5, 5, 9, 21, 1, 1],
                    [6, 6, 2, 2, 1, 1],
                    [7, 7, 1, 6, 1, 1],
                ],
            },
        )
        add_across("b", column_range=[[1, 2], [3, 4]], newname="b_aap")
        dbaap = get_data("b_aap")
        assert_array_equal(
            dbaap.y,
            np.array([[2, 2], [7, 5], [103, 51], [12, 59], [14, 22], [8, 3], [8, 7]]),
        )

    def test_crop(self):
        del_data("*")
        store_data("a", data={"x": [0, 4, 8, 12, 16], "y": [1, 2, 3, 4, 5]})
        store_data(
            "b",
            data={
                "x": [2, 5, 8, 11, 14, 17, 20],
                "y": [
                    [1, 1, 1, 1, 1, 1],
                    [2, 2, 5, 4, 1, 1],
                    [100, 100, 3, 50, 1, 1],
                    [4, 4, 8, 58, 1, 1],
                    [5, 5, 9, 21, 1, 1],
                    [6, 6, 2, 2, 1, 1],
                    [7, 7, 1, 6, 1, 1],
                ],
            },
        )
        crop("a", "b", replace=False)
        acrop_data = get_data("a_cropped")
        bcrop_data = get_data("b_cropped")
        assert_array_equal(acrop_data.times, np.array([4.0, 8.0, 12.0, 16.0]))
        assert_array_equal(acrop_data.y, np.array([2, 3, 4, 5]))
        assert_array_equal(bcrop_data.times, np.array([2.0, 5.0, 8.0, 11.0, 14.0]))
        assert_array_equal(
            bcrop_data.y,
            np.array(
                [
                    [1, 1, 1, 1, 1, 1],
                    [2, 2, 5, 4, 1, 1],
                    [100, 100, 3, 50, 1, 1],
                    [4, 4, 8, 58, 1, 1],
                    [5, 5, 9, 21, 1, 1],
                ]
            ),
        )
        # with replacement
        crop("a", "b", replace=True)
        acrop_data = get_data("a")
        bcrop_data = get_data("b")
        assert_array_equal(acrop_data.times, np.array([4.0, 8.0, 12.0, 16.0]))
        assert_array_equal(acrop_data.y, np.array([2, 3, 4, 5]))
        assert_array_equal(bcrop_data.times, np.array([2.0, 5.0, 8.0, 11.0, 14.0]))
        assert_array_equal(
            bcrop_data.y,
            np.array(
                [
                    [1, 1, 1, 1, 1, 1],
                    [2, 2, 5, 4, 1, 1],
                    [100, 100, 3, 50, 1, 1],
                    [4, 4, 8, 58, 1, 1],
                    [5, 5, 9, 21, 1, 1],
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()
