import unittest
import matplotlib.pyplot as plt
import numpy as np

from pyspedas import del_data, store_data, tplot, tplot_options


class TestMarginOptions(unittest.TestCase):
    def setUp(self):
        del_data("*")
        store_data("var1", data={"x": [1, 2, 3], "y": [10, 20, 30]})
        store_data("var2", data={"x": [1, 2, 3], "y": [5, 15, 25]})
        tplot_options("xmargin", None)
        tplot_options("ymargin", None)

    def tearDown(self):
        tplot_options("xmargin", None)
        tplot_options("ymargin", None)
        del_data("*")
        plt.close("all")

    def test_xmargin_global_inches(self):
        # Specifying inches with default xsize=10
        tplot_options("xmargin", [1.0, 2.0])
        fig, axes = tplot(["var1", "var2"], xsize=10, ysize=6, display=False, return_plot_objects=True)
        self.assertIsNone(fig.get_layout_engine())
        subplotpars = fig.subplotpars
        # left = 1.0 / 10 = 0.1, right = 1.0 - 2.0 / 10 = 0.8
        self.assertAlmostEqual(subplotpars.left, 0.10, places=3)
        self.assertAlmostEqual(subplotpars.right, 0.80, places=3)

    def test_ymargin_global_inches(self):
        # ymargin in inches with ysize=8
        tplot_options("ymargin", [1.6, 0.8])
        fig, axes = tplot(["var1", "var2"], xsize=10, ysize=8, display=False, return_plot_objects=True)
        self.assertIsNone(fig.get_layout_engine())
        subplotpars = fig.subplotpars
        # top = 1.0 - 1.6 / 8 = 0.80, bottom = 0.8 / 8 = 0.10
        self.assertAlmostEqual(subplotpars.top, 0.80, places=3)
        self.assertAlmostEqual(subplotpars.bottom, 0.10, places=3)

    def test_tplot_direct_argument_override(self):
        # Direct argument should work even if global option is set
        tplot_options("xmargin", [1.0, 1.0])
        fig, axes = tplot(["var1"], xsize=10, xmargin=[2.5, 2.5], display=False, return_plot_objects=True)
        subplotpars = fig.subplotpars
        # left = 2.5 / 10 = 0.25, right = 1.0 - 2.5 / 10 = 0.75
        self.assertAlmostEqual(subplotpars.left, 0.25, places=3)
        self.assertAlmostEqual(subplotpars.right, 0.75, places=3)

    def test_default_without_margins_uses_constrained_layout(self):
        # Without margins, constrained layout is preserved
        fig, axes = tplot(["var1"], display=False, return_plot_objects=True)
        self.assertIsNotNone(fig.get_layout_engine())


if __name__ == "__main__":
    unittest.main()
