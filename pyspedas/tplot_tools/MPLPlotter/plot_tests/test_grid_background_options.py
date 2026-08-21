import unittest

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

from pyspedas import del_data, options, store_data, tplot, tplot_options


class GridBackgroundPlotOptionsTestCases(unittest.TestCase):
    def setUp(self):
        del_data("*")
        store_data("panel1", data={"x": [1, 2, 3], "y": [1, 2, 3]})
        store_data("panel2", data={"x": [1, 2, 3], "y": [3, 2, 1]})
        tplot_options("background", None)
        tplot_options("grid", False)
        tplot_options("grid_properties", {})

    def tearDown(self):
        tplot_options("background", None)
        tplot_options("grid", False)
        tplot_options("grid_properties", {})
        del_data("*")
        plt.close("all")

    def test_global_background_applies_to_figure_and_panels(self):
        tplot_options("background", "#123456")

        fig, axes = tplot(["panel1", "panel2"], display=False, return_plot_objects=True)

        expected = mcolors.to_rgba("#123456")
        self.assertEqual(fig.get_facecolor(), expected)
        for axis in axes:
            self.assertEqual(axis.get_facecolor(), expected)

    def test_global_grid_and_per_panel_override(self):
        tplot_options("grid", True)
        tplot_options(
            "grid_properties",
            {"color": "red", "alpha": 0.4, "linewidth": 2.0, "linestyle": "--"},
        )
        options("panel2", "grid", False)

        _, axes = tplot(["panel1", "panel2"], display=False, return_plot_objects=True)

        panel1_gridline = axes[0].get_ygridlines()[0]
        self.assertTrue(panel1_gridline.get_visible())
        self.assertEqual(panel1_gridline.get_color(), "red")
        self.assertEqual(panel1_gridline.get_alpha(), 0.4)
        self.assertEqual(panel1_gridline.get_linewidth(), 2.0)
        self.assertEqual(panel1_gridline.get_linestyle(), "--")
        self.assertFalse(any(line.get_visible() for line in axes[1].get_ygridlines()))

    def test_panel_grid_properties_override_global_properties(self):
        tplot_options("grid", True)
        tplot_options("grid_properties", {"color": "red", "linewidth": 1.0})
        options("panel1", "grid_properties", {"color": "blue"})

        _, axes = tplot(["panel1", "panel2"], display=False, return_plot_objects=True)

        panel1_gridline = axes[0].get_ygridlines()[0]
        panel2_gridline = axes[1].get_ygridlines()[0]
        self.assertEqual(panel1_gridline.get_color(), "blue")
        self.assertEqual(panel1_gridline.get_linewidth(), 1.0)
        self.assertEqual(panel2_gridline.get_color(), "red")

    def test_grid_properties_rejects_visible(self):
        tplot_options("grid_properties", {"visible": True})
        options("panel1", "grid_properties", {"visible": True})

        _, axes = tplot("panel1", display=False, return_plot_objects=True)

        self.assertFalse(any(line.get_visible() for line in axes.get_ygridlines()))


if __name__ == "__main__":
    unittest.main()
