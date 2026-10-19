"""Unit tests for filled time-series plots and the ``y2`` option alias."""

import unittest

from matplotlib.collections import PolyCollection
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from pyspedas import del_data, options, store_data, time_string, tplot


class FillBetweenTestCases(unittest.TestCase):
    def setUp(self):
        del_data("*")
        self.times = 1700000000 + np.arange(5) * 60
        self.values = np.column_stack(
            [10 + np.arange(5), 20 + np.arange(5), 30 + np.arange(5)]
        )
        self.baselines = [0, -2, 50]
        store_data("fill_test", data={"x": self.times, "y": self.values})

    def tearDown(self):
        del_data("*")
        plt.close("all")

    def _plot(self, name="fill_test"):
        fig, axis = tplot(
            name,
            trange=time_string([self.times[0], self.times[-1]]),
            display=False,
            return_plot_objects=True,
        )
        fig.canvas.draw()
        return axis

    def _assert_fills(self, axis, baselines, values=None):
        if values is None:
            values = self.values
        self.assertEqual(len(axis.lines), 0)
        self.assertEqual(len(axis.collections), len(baselines))
        for trace, (collection, baseline) in enumerate(
            zip(axis.collections, baselines)
        ):
            with self.subTest(trace=trace, baseline=baseline):
                self.assertIsInstance(collection, PolyCollection)
                paths = collection.get_paths()
                self.assertEqual(len(paths), 1)
                # Ignore polygon vertex ordering; check both the trace and
                # baseline boundary, including fills above the trace.
                expected_y = np.unique(np.append(values[:, trace], baseline))
                np.testing.assert_allclose(
                    np.unique(paths[0].vertices[:, 1]), expected_y
                )

    def _assert_lines(self, axis):
        self.assertEqual(len(axis.collections), 0)
        self.assertEqual(len(axis.lines), 3)
        for trace, line in enumerate(axis.lines):
            np.testing.assert_allclose(line.get_ydata(), self.values[:, trace])

    def test_default_is_unfilled_lines(self):
        self._assert_lines(self._plot())

    def test_fill_defaults_to_zero_baseline(self):
        options("fill_test", "fill_between", True)

        self._assert_fills(self._plot(), [0, 0, 0])

    def test_fill_uses_a_different_baseline_for_each_trace(self):
        options("fill_test", "fill_between", True)
        options("fill_test", "y_fill_line", self.baselines)

        self._assert_fills(self._plot(), self.baselines)

    def test_y2_alias_sets_the_fill_baselines(self):
        options(
            "fill_test",
            opt_dict={"fill_between": True, "y2": self.baselines},
        )

        self._assert_fills(self._plot(), self.baselines)

    def test_scalar_baseline_applies_to_all_traces(self):
        options("fill_test", "fill_between", True)
        for baseline in (0, -5, 50):
            with self.subTest(baseline=baseline):
                options("fill_test", "y_fill_line", baseline)

                self._assert_fills(self._plot(), [baseline] * 3)

    def test_fill_can_be_disabled_without_clearing_the_baseline(self):
        options(
            "fill_test",
            opt_dict={"fill_between": True, "y_fill_line": self.baselines},
        )
        self._assert_fills(self._plot(), self.baselines)

        options("fill_test", "fill_between", False)

        self._assert_lines(self._plot())

    def test_baseline_alone_does_not_enable_fills(self):
        options("fill_test", "y_fill_line", self.baselines)

        self._assert_lines(self._plot())

    def test_fill_ignores_marker_options_with_default_baseline(self):
        options(
            "fill_test",
            opt_dict={
                "fill_between": True,
                "marker": "o",
                "marker_size": 5,
                "markevery": 2,
            },
        )

        self._assert_fills(self._plot(), [0, 0, 0])

    def test_fill_ignores_marker_size_with_explicit_baselines(self):
        options(
            "fill_test",
            opt_dict={
                "fill_between": True,
                "y2": self.baselines,
                "marker_size": 5,
            },
        )

        self._assert_fills(self._plot(), self.baselines)

    def test_fill_ignores_marker_interval_with_explicit_baselines(self):
        options(
            "fill_test",
            opt_dict={
                "fill_between": True,
                "y2": self.baselines,
                "markevery": 2,
            },
        )

        self._assert_fills(self._plot(), self.baselines)

    def test_fill_takes_precedence_over_scatter_options(self):
        options(
            "fill_test",
            opt_dict={
                "fill_between": True,
                "y2": self.baselines,
                "symbols": True,
                "marker_size": 5,
            },
        )

        self._assert_fills(self._plot(), self.baselines)

    def test_single_trace_can_be_filled(self):
        store_data(
            "fill_single", data={"x": self.times, "y": self.values[:, 0]}
        )
        options("fill_single", opt_dict={"fill_between": True, "y2": -2})

        self._assert_fills(
            self._plot("fill_single"), [-2], values=self.values[:, :1]
        )

    def test_pseudovariable_distributes_baselines_across_components(self):
        store_data(
            "fill_pair", data={"x": self.times, "y": self.values[:, :2]}
        )
        store_data(
            "fill_single", data={"x": self.times, "y": self.values[:, 2]}
        )
        store_data("fill_combined", data=["fill_pair", "fill_single"])
        options(
            "fill_combined",
            opt_dict={"fill_between": True, "y2": self.baselines},
        )

        self._assert_fills(self._plot("fill_combined"), self.baselines)

    def test_fill_preserves_colors_alpha_and_legend_labels(self):
        colors = ["blue", "green", "red"]
        labels = ["First", "Second", "Third"]
        options(
            "fill_test",
            opt_dict={
                "fill_between": True,
                "y_fill_line": self.baselines,
                "color": colors,
                "alpha": 0.3,
                "legend_names": labels,
            },
        )

        axis = self._plot()

        self._assert_fills(axis, self.baselines)
        for collection, color, label in zip(axis.collections, colors, labels):
            np.testing.assert_allclose(
                collection.get_facecolor()[0], mcolors.to_rgba(color, alpha=0.3)
            )
            self.assertEqual(collection.get_label(), label)
        self.assertEqual(
            [text.get_text() for text in axis.get_legend().get_texts()], labels
        )


if __name__ == "__main__":
    unittest.main()
