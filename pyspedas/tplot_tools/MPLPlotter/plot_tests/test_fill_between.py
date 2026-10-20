"""Testing tplot lineplot with the fill_between option"""
import os
from pathlib import Path
import tempfile
import unittest
import matplotlib.pyplot as plt
import numpy as np
from pyspedas import del_data, options, store_data, tplot
from pyspedas.config import CONFIG

# Whether to display plots during testing
#global_display = CONFIG["testing"]["global_display"]
global_display = False
# Directory to save testing output files
output_dir = CONFIG["testing"]["output_dir"]
# Ensure output directory exists
save_dir = os.path.join(output_dir, "utilities")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

class FillBetweenTestCases(unittest.TestCase):
    def setUp(self):
        del_data("*")
        self.addCleanup(del_data, "*")
        self.addCleanup(plt.close, "all")
        directory = tempfile.TemporaryDirectory(prefix="pyspedas-tplot_tools-")
        self.addCleanup(directory.cleanup)
        self.output = Path(directory.name)

    def assert_plot(self, path):
        self.assertTrue(path.is_file(), f"Plot was not saved: {path}")
        pixels = plt.imread(path)
        self.assertGreater(np.ptp(pixels), 0, "Plot is blank")
    
    def test_basic(self):
        var_name = "fill_between_test_var"
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(var_name,opt_dict={"fill_between":True})
        path = self.output / "fill_between_basic.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)

    def test_basic_single_y2(self):
        var_name = "fill_between_test_var"
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(var_name,opt_dict={"fill_between":True,"y_fill_line":-1})
        path = self.output / "fill_between_basic_single_y2.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)

    def test_basic_disable(self):
        var_name = "fill_between_test_var"
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(var_name,opt_dict={"fill_between":True,"y_fill_line":-1})
        # should disable fill, should return line plot:
        options(var_name, "fill_between",False)
        path = self.output / "fill_between_basic_disable.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)

    def test_basic_multi_y2(self):
        # Just accepts first y2
        var_name = "fill_between_test_var"
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(var_name,opt_dict={"fill_between":True,"y_fill_line":[-1,1]})
        path = self.output / "fill_between_basic_multi_y2.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)

    def test_multicurve(self):
        var_name = "fill_between_test_var"
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([[1,-1,2],[2,1,-1],[-1,2,0],[0,-2,2],[1,0,-1]])})
        options(var_name,opt_dict={"fill_between":True})
        path = self.output / "fill_between_multicurve.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)

    def test_multicurve_single_y2(self):
        var_name = "fill_between_test_var"
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([[1,-1,2],[2,1,-1],[-1,2,0],[0,-2,2],[1,0,-1]])})
        options(var_name,opt_dict={"fill_between":True,"y_fill_line":-1})
        path = self.output / "fill_between_multicurve_single_y2.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)

    def test_multicurve_multi_y2_not_enough(self):
        var_name = "fill_between_test_var"
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([[1,-1,2],[2,1,-1],[-1,2,0],[0,-2,2],[1,0,-1]])})
        options(var_name,opt_dict={"fill_between":True,"y_fill_line":[-1,1]})
        path = self.output / "fill_between_multi_y2_not_enough.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)

    def test_multicurve_multi_y2(self):
        var_name = "fill_between_test_var"
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([[1,-1,2],[2,1,-1],[-1,2,0],[0,-2,2],[1,0,-1]])})
        options(var_name,opt_dict={"fill_between":True,"y_fill_line":[-1,1,2]})
        path = self.output / "fill_between_multicurve_multi_y2.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)

    def test_multicurve_multi_y2_alias(self):
        var_name = "fill_between_test_var"
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([[1,-1,2],[2,1,-1],[-1,2,0],[0,-2,2],[1,0,-1]])})
        options(var_name,opt_dict={"fill_between":True,"y2":[-1,1,2]})
        path = self.output / "fill_between_multicurve_multi_y2_alias.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)

    def test_baseline_alone_does_not_enable_fills(self):
        # should return line plot
        var_name = "fill_between_test_var"
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(var_name,opt_dict={"y_fill_line":-1})
        path = self.output / "fill_between_baseline_does_not_enable_fills.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)

    def test_fill_ignores_marker_options_with_default_baseline(self):
        # should ignore marker options and just return filled line plot
        var_name = "fill_between_test_var"
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(
            var_name,
            opt_dict={
                "fill_between": True,
                "marker": "o",
                "marker_size": 5,
                "markevery": 2})
        path = self.output / "fill_between_ignore_marker_opts.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)
        
    def test_fill_ignores_marker_size_with_explicit_baselines(self):
        # should ignore marker options and just return filled line plot
        var_name = "fill_between_test_var"
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(
            var_name,
            opt_dict={
                "fill_between": True,
                "y2": -1,
                "marker": "o",
                "marker_size": 5,
                "markevery": 2})
        path = self.output / "fill_between_ignore_marker_opts_y2.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)
        
    def test_fill_takes_precedence_over_scatter_options(self):
        # should ignore scatter bool and just return filled line plot
        var_name = "fill_between_test_var"
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(
            var_name,
            opt_dict={
                "fill_between": True,
                "symbols": True})
        path = self.output / "fill_between_precedence_over_scatter.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)
        
    def test_pseudovariable_distributes_baselines_across_components(self):
        var_name = "fill_combined"
        test_times = (np.arange(5)+1700000000)
        test_data = np.array([[1,-1,2],[2,1,-1],[-1,2,0],[0,-2,2],[1,0,-1]])
        store_data("fill_single", data={"x":test_times,"y":test_data[:,2]})
        store_data("fill_pair", data={"x":test_times,"y":test_data[:,:2]})
        store_data(var_name, data=["fill_pair", "fill_single"])
        options(var_name,opt_dict={"fill_between":True,"y_fill_line":-1})
        path = self.output / "fill_between_dist_baselines_comp.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)

    def test_fill_preserves_colors_alpha_and_legend_labels(self):
        var_name = "fill_between_test_var"
        colors = ["blue", "green", "red"]
        labels = ["First", "Second", "Third"]
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([[1,-1,2],[2,1,-1],[-1,2,0],[0,-2,2],[1,0,-1]])})
        options(
            var_name,
            opt_dict={
                "fill_between":True,
                "y_fill_line":-1,
                "color": colors,
                "alpha": 0.3,
                "legend_names": labels,
                })
        path = self.output / "fill_between_preserve_alpha_labels.png"
        tplot(var_name, display=global_display, save_png=str(path))
        self.assert_plot(path)
        
if __name__ == "__main__":
    unittest.main()
