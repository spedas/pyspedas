"""Testing tplot lineplot with the fill_between option"""
import os
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
    def test_basic(self):
        var_name = "fill_between_test_var"
        del_data()
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(var_name,opt_dict={"fill_between":True})
        fig,axis = tplot(var_name,display=False,return_plot_objects=True)
        plt.savefig('fill_between_basic.png', dpi=300)
        if global_display:
            fig.canvas.draw()

    def test_basic_single_y2(self):
        var_name = "fill_between_test_var"
        del_data()
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(var_name,opt_dict={"fill_between":True,"y_fill_line":-1})
        fig,axis = tplot(var_name,display=False,return_plot_objects=True)
        plt.savefig('fill_between_basic_single_y2.png', dpi=300)
        if global_display:
            fig.canvas.draw()

    def test_basic_disable(self):
        var_name = "fill_between_test_var"
        del_data()
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(var_name,opt_dict={"fill_between":True,"y_fill_line":-1})
        # should disable fill, should return line plot:
        options(var_name, "fill_between",False)
        fig,axis = tplot(var_name,display=False,return_plot_objects=True)
        plt.savefig('fill_between_basic_disable.png', dpi=300)
        if global_display:
            fig.canvas.draw()

    def test_basic_multi_y2(self):
        # Just accepts first y2
        var_name = "fill_between_test_var"
        del_data()
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(var_name,opt_dict={"fill_between":True,"y_fill_line":[-1,1]})
        fig,axis = tplot(var_name,display=False,return_plot_objects=True)
        plt.savefig('fill_between_basic_multi_y2.png', dpi=300)
        if global_display:
            fig.canvas.draw()

    def test_multicurve(self):
        var_name = "fill_between_test_var"
        del_data()
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([[1,-1,2],[2,1,-1],[-1,2,0],[0,-2,2],[1,0,-1]])})
        options(var_name,opt_dict={"fill_between":True})
        fig,axis = tplot(var_name,display=False,return_plot_objects=True)
        plt.savefig('fill_between_multicurve.png', dpi=300)
        if global_display:
            fig.canvas.draw()

    def test_multicurve_single_y2(self):
        var_name = "fill_between_test_var"
        del_data()
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([[1,-1,2],[2,1,-1],[-1,2,0],[0,-2,2],[1,0,-1]])})
        options(var_name,opt_dict={"fill_between":True,"y_fill_line":-1})
        fig,axis = tplot(var_name,display=False,return_plot_objects=True)
        plt.savefig('fill_between_multicurve_single_y2.png', dpi=300)
        if global_display:
            fig.canvas.draw()

    def test_multicurve_multi_y2_not_enough(self):
        var_name = "fill_between_test_var"
        del_data()
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([[1,-1,2],[2,1,-1],[-1,2,0],[0,-2,2],[1,0,-1]])})
        options(var_name,opt_dict={"fill_between":True,"y_fill_line":[-1,1]})
        fig,axis = tplot(var_name,display=False,return_plot_objects=True)
        plt.savefig('fill_between_multi_y2_not_enough.png', dpi=300)
        if global_display:
            fig.canvas.draw()

    def test_multicurve_multi_y2(self):
        var_name = "fill_between_test_var"
        del_data()
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([[1,-1,2],[2,1,-1],[-1,2,0],[0,-2,2],[1,0,-1]])})
        options(var_name,opt_dict={"fill_between":True,"y_fill_line":[-1,1,2]})
        fig,axis = tplot(var_name,display=False,return_plot_objects=True)
        plt.savefig('fill_between_multicurve_multi_y2.png', dpi=300)
        if global_display:
            fig.canvas.draw()

    def test_multicurve_multi_y2_alias(self):
        var_name = "fill_between_test_var"
        del_data()
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([[1,-1,2],[2,1,-1],[-1,2,0],[0,-2,2],[1,0,-1]])})
        options(var_name,opt_dict={"fill_between":True,"y2":[-1,1,2]})
        fig,axis = tplot(var_name,display=False,return_plot_objects=True)
        plt.savefig('fill_between_multicurve_multi_y2_alias.png', dpi=300)
        if global_display:
            fig.canvas.draw()

    def test_baseline_alone_does_not_enable_fills(self):
        # should return line plot
        var_name = "fill_between_test_var"
        del_data()
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(var_name,opt_dict={"y_fill_line":-1})
        fig,axis = tplot(var_name,display=False,return_plot_objects=True)
        plt.savefig('fill_between_baseline_does_not_enable_fills.png', dpi=300)
        if global_display:
            fig.canvas.draw()
        
    def test_fill_ignores_marker_options_with_default_baseline(self):
        # should ignore marker options and just return filled line plot
        var_name = "fill_between_test_var"
        del_data()
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(
            var_name,
            opt_dict={
                "fill_between": True,
                "marker": "o",
                "marker_size": 5,
                "markevery": 2})
        fig,axis = tplot(var_name,display=False,return_plot_objects=True)
        plt.savefig('fill_between_ignore_marker_opts.png', dpi=300)
        if global_display:
            fig.canvas.draw()
        
    def test_fill_ignores_marker_size_with_explicit_baselines(self):
        # should ignore marker options and just return filled line plot
        var_name = "fill_between_test_var"
        del_data()
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(
            var_name,
            opt_dict={
                "fill_between": True,
                "y2": -1,
                "marker": "o",
                "marker_size": 5,
                "markevery": 2})
        fig,axis = tplot(var_name,display=False,return_plot_objects=True)
        plt.savefig('fill_between_ignore_marker_opts_y2.png', dpi=300)
        if global_display:
            fig.canvas.draw()
        
    def test_fill_takes_precedence_over_scatter_options(self):
        # should ignore scatter bool and just return filled line plot
        var_name = "fill_between_test_var"
        del_data()
        store_data(var_name, data={"x":(np.arange(5)+1700000000),"y":np.array([1,2,-1,0,1])})
        options(
            var_name,
            opt_dict={
                "fill_between": True,
                "symbols": True})
        fig,axis = tplot(var_name,display=False,return_plot_objects=True)
        plt.savefig('fill_between_precedence_over_scatter.png', dpi=300)
        if global_display:
            fig.canvas.draw()
        
    def test_pseudovariable_distributes_baselines_across_components(self):
        del_data(["fill_single","fill_pair"])
        test_times = (np.arange(5)+1700000000)
        test_data = np.array([[1,-1,2],[2,1,-1],[-1,2,0],[0,-2,2],[1,0,-1]])
        store_data("fill_single", data={"x":test_times,"y":test_data[:,2]})
        store_data("fill_pair", data={"x":test_times,"y":test_data[:,:2]})
        store_data("fill_combined", data=["fill_pair", "fill_single"])
        options("fill_combined",opt_dict={"fill_between":True,"y_fill_line":-1})
        fig,axis = tplot("fill_combined",display=False,return_plot_objects=True)
        plt.savefig('fill_between_dist_baselines_comp.png', dpi=300)
        if global_display:
            fig.canvas.draw()

    def test_fill_preserves_colors_alpha_and_legend_labels(self):
        colors = ["blue", "green", "red"]
        labels = ["First", "Second", "Third"]
        var_name = "fill_between_test_var"
        del_data()
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
        fig,axis = tplot(var_name,display=False,return_plot_objects=True)
        plt.savefig('fill_between_preserve_alpha_labels.png', dpi=300)
        if global_display:
            fig.canvas.draw()
        
if __name__ == "__main__":
    unittest.main()
