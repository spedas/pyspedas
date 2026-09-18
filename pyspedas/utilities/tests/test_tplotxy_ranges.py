"""Range controls for projected vector plots, using local synthetic data."""

import unittest

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from pyspedas import del_data, set_units, store_data, tplotxy, tplotxy3


class PlotRangeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        store_data(
            "tplotxy_range_test",
            data={"x": np.arange(3), "y": np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])},
        )
        set_units("tplotxy_range_test", "re")

    @classmethod
    def tearDownClass(cls):
        del_data("tplotxy_range_test")

    def tearDown(self):
        plt.close("all")

    def test_single_panel_ranges_follow_projected_axes(self):
        for plane in ("xy", "xz", "yz"):
            with self.subTest(plane=plane):
                tplotxy(
                    "tplotxy_range_test", plane=plane, hrange=(-10, 10),
                    vrange=(-20, 20), reverse_x=True, reverse_y=True,
                    show_centerbody=False, display=False,
                )
                axis = plt.gcf().axes[0]
                np.testing.assert_allclose(axis.get_xlim(), (10, -10))
                np.testing.assert_allclose(axis.get_ylim(), (20, -20))
                plt.close("all")

    def test_three_panel_ranges_follow_spatial_coordinates(self):
        fig = tplotxy3(
            "tplotxy_range_test", xrange=(-10, 10), yrange=(-20, 20),
            zrange=(-30, 30), reverse_x=True, show_centerbody=False,
            display=False,
        )
        for axis in (fig.xy_plane, fig.xz_plane):
            np.testing.assert_allclose(axis.get_xlim(), (10, -10))
        np.testing.assert_allclose(fig.xy_plane.get_ylim(), (20, -20))
        np.testing.assert_allclose(fig.yz_plane.get_xlim(), (-20, 20))
        for axis in (fig.xz_plane, fig.yz_plane):
            np.testing.assert_allclose(axis.get_ylim(), (-30, 30))

    def test_unspecified_ranges_keep_default_behavior(self):
        fig = tplotxy3(
            "tplotxy_range_test", xrange=(-10, 10),
            show_centerbody=False, display=False,
        )
        np.testing.assert_allclose(fig.xy_plane.get_xlim(), (-10, 10))
        np.testing.assert_allclose(fig.xz_plane.get_xlim(), (-10, 10))
        np.testing.assert_allclose(fig.xz_plane.get_ylim(), fig.yz_plane.get_ylim())

    def test_single_panel_methods_preserve_axis_direction(self):
        for reverse in (False, True):
            with self.subTest(reverse=reverse):
                fig = tplotxy(
                    "tplotxy_range_test", plane="yz", reverse_x=reverse,
                    reverse_y=reverse, show_centerbody=False, display=False,
                )
                fig.set_hrange((-11, 12))
                fig.set_vrange((-21, 22))
                expected_x = (12, -11) if reverse else (-11, 12)
                expected_y = (22, -21) if reverse else (-21, 22)
                np.testing.assert_allclose(fig.xy_axis.get_xlim(), expected_x)
                np.testing.assert_allclose(fig.xy_axis.get_ylim(), expected_y)
                plt.close(fig)

    def test_three_panel_methods_preserve_axis_direction(self):
        for reverse in (False, True):
            with self.subTest(reverse=reverse):
                fig = tplotxy3(
                    "tplotxy_range_test", reverse_x=reverse,
                    show_centerbody=False, display=False,
                )
                fig.set_xrange((-11, 12))
                fig.set_yrange((-21, 22))
                fig.set_zrange((-31, 32))
                expected_x = (12, -11) if reverse else (-11, 12)
                expected_xy_y = (22, -21) if reverse else (-21, 22)
                for axis in (fig.xy_plane, fig.xz_plane):
                    np.testing.assert_allclose(axis.get_xlim(), expected_x)
                np.testing.assert_allclose(fig.xy_plane.get_ylim(), expected_xy_y)
                np.testing.assert_allclose(fig.yz_plane.get_xlim(), (-21, 22))
                for axis in (fig.xz_plane, fig.yz_plane):
                    np.testing.assert_allclose(axis.get_ylim(), (-31, 32))
                plt.close(fig)


if __name__ == "__main__":
    unittest.main()
