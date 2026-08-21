import unittest

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from pyspedas import annotate, del_data, options, store_data, tplot, tplot_options


class GridBackgroundPlotOptionsTestCases(unittest.TestCase):
    def setUp(self):
        del_data("*")
        store_data("panel1", data={"x": [1, 2, 3], "y": [1, 2, 3]})
        store_data("panel2", data={"x": [1, 2, 3], "y": [3, 2, 1]})
        tplot_options("background", None)
        tplot_options("foreground", None)
        tplot_options("grid", False)
        tplot_options("grid_properties", {})
        tplot_options("varlabel_style", None)

    def tearDown(self):
        tplot_options("background", None)
        tplot_options("foreground", None)
        tplot_options("grid", False)
        tplot_options("grid_properties", {})
        tplot_options("varlabel_style", None)
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

    def test_global_foreground_applies_to_plot_text_and_decorations(self):
        tplot_options("background", "#001b33")
        tplot_options("foreground", "white")
        tplot_options("title", "Figure title")
        options("panel1", "title", "Panel title")
        options("panel1", "xtitle", "X title")
        options("panel1", "ytitle", "Y title")
        options("panel1", "legend_names", ["Trace"])
        annotate("panel1", "Annotation", (0.5, 0.5))

        fig, axis = tplot("panel1", display=False, return_plot_objects=True)

        expected_foreground = mcolors.to_rgba("white")
        expected_background = mcolors.to_rgba("#001b33")
        self.assertEqual(
            mcolors.to_rgba(fig._suptitle.get_color()), expected_foreground
        )
        self.assertEqual(mcolors.to_rgba(axis.title.get_color()), expected_foreground)
        self.assertEqual(
            mcolors.to_rgba(axis.xaxis.label.get_color()), expected_foreground
        )
        self.assertEqual(
            mcolors.to_rgba(axis.yaxis.label.get_color()), expected_foreground
        )
        for label in axis.get_xticklabels() + axis.get_yticklabels():
            self.assertEqual(mcolors.to_rgba(label.get_color()), expected_foreground)
        for spine in axis.spines.values():
            self.assertEqual(
                mcolors.to_rgba(spine.get_edgecolor()), expected_foreground
            )
        self.assertEqual(
            mcolors.to_rgba(axis.texts[0].get_color()), expected_foreground
        )
        legend = axis.get_legend()
        self.assertEqual(
            mcolors.to_rgba(legend.get_texts()[0].get_color()), expected_foreground
        )
        self.assertEqual(
            mcolors.to_rgba(legend.get_frame().get_edgecolor())[:3],
            expected_foreground[:3],
        )
        self.assertEqual(
            legend.get_frame().get_facecolor()[:3], expected_background[:3]
        )

    def test_explicit_panel_colors_override_global_foreground(self):
        tplot_options("foreground", "white")
        options("panel1", "xtitle", "X title")
        options("panel1", "ytitle", "Y title")
        options("panel1", "xtitle_color", "red")
        options("panel1", "ytitle_color", "green")
        options("panel1", "xtick_labelcolor", "orange")
        options("panel1", "legend_names", ["Trace"])
        options("panel1", "legend_color", "purple")
        annotate("panel1", "Annotation", (0.5, 0.5), color="black")

        _, axis = tplot("panel1", display=False, return_plot_objects=True)

        self.assertEqual(axis.xaxis.label.get_color(), "red")
        self.assertEqual(axis.yaxis.label.get_color(), "green")
        self.assertTrue(
            all(label.get_color() == "orange" for label in axis.get_xticklabels())
        )
        legend_color = np.asarray(axis.get_legend().get_texts()[0].get_color())
        self.assertTrue(np.all(legend_color == mcolors.to_rgba("purple")))
        self.assertEqual(axis.texts[0].get_color(), "black")

    def test_global_foreground_applies_to_colorbar(self):
        store_data(
            "spectrum",
            data={
                "x": [1, 2, 3],
                "y": [[1, 2], [2, 3], [3, 4]],
                "v": [10, 20],
            },
        )
        options("spectrum", "spec", True)
        tplot_options("background", "#001b33")
        tplot_options("foreground", "white")

        fig, _ = tplot("spectrum", display=False, return_plot_objects=True)

        colorbar_axis = fig.axes[1]
        expected_foreground = mcolors.to_rgba("white")
        expected_background = mcolors.to_rgba("#001b33")
        self.assertEqual(colorbar_axis.get_facecolor(), expected_background)
        for label in colorbar_axis.get_yticklabels():
            self.assertEqual(mcolors.to_rgba(label.get_color()), expected_foreground)
        self.assertEqual(
            mcolors.to_rgba(colorbar_axis.yaxis.label.get_color()),
            expected_foreground,
        )

    def test_global_foreground_applies_to_variable_label_axes(self):
        store_data("labels", data={"x": [1, 2, 3], "y": [10, 20, 30]})
        options("labels", "ytitle", "Position")
        tplot_options("foreground", "white")

        _, axis = tplot(
            "panel1",
            var_label="labels",
            display=False,
            return_plot_objects=True,
        )

        variable_label_axis = axis.child_axes[0]
        expected_foreground = mcolors.to_rgba("white")
        self.assertEqual(
            mcolors.to_rgba(variable_label_axis.xaxis.label.get_color()),
            expected_foreground,
        )
        for label in variable_label_axis.get_xticklabels():
            self.assertEqual(mcolors.to_rgba(label.get_color()), expected_foreground)

    def test_global_foreground_applies_to_variable_label_panel(self):
        store_data("labels", data={"x": [1, 2, 3], "y": [10, 20, 30]})
        options("labels", "ytitle", "Position")
        tplot_options("foreground", "white")
        tplot_options("varlabel_style", "extra_panel")

        _, axes = tplot(
            "panel1",
            var_label=["labels"],
            display=False,
            return_plot_objects=True,
        )

        expected_foreground = mcolors.to_rgba("white")
        variable_label_axis = axes[1]
        for text in variable_label_axis.texts:
            self.assertEqual(mcolors.to_rgba(text.get_color()), expected_foreground)
        for label in variable_label_axis.get_yticklabels():
            self.assertEqual(mcolors.to_rgba(label.get_color()), expected_foreground)

    def test_unset_foreground_uses_matplotlib_defaults(self):
        store_data("labels", data={"x": [1, 2, 3], "y": [10, 20, 30]})
        options("labels", "ytitle", "Position")
        options("panel1", "title", "Panel title")

        _, axis = tplot(
            "panel1",
            var_label="labels",
            display=False,
            return_plot_objects=True,
        )

        self.assertIsNotNone(axis.title.get_color())
        self.assertIsNotNone(axis.child_axes[0].xaxis.label.get_color())

        tplot_options("varlabel_style", "extra_panel")
        _, axes = tplot(
            "panel1",
            var_label=["labels"],
            display=False,
            return_plot_objects=True,
        )
        self.assertTrue(all(text.get_color() is not None for text in axes[1].texts))

    def test_extra_panel_style_without_variable_labels(self):
        tplot_options("varlabel_style", "extra_panel")

        _, axis = tplot("panel1", display=False, return_plot_objects=True)

        self.assertNotIsInstance(axis, np.ndarray)
        self.assertEqual(axis.var_name, "panel1")

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
