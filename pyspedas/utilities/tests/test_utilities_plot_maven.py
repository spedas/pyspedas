"""Plot tests that load MAVEN mission data."""

import os
import unittest
from pyspedas.projects import maven
from pyspedas import del_data, options, timespan, tplot, tplot_options

from pyspedas.config import CONFIG

global_display = False
save_dir = os.path.join(CONFIG["testing"]["output_dir"], "utilities")
os.makedirs(save_dir, exist_ok=True)


class PlotTestCases(unittest.TestCase):
    def test_maven_specplot(self):
        del_data("*")

        sta_vars = maven.spdf.load(
            trange=["2020-12-30", "2020-12-31"],
            instrument="static",
            datatype="c0-64e2m",
        )
        print(sta_vars)
        timespan("2020-12-30", 1, "days")
        # This variable contains all zeroes, and is set to plot with log scaling
        tplot_options("title", "Should be all the same color")
        tplot("bkg", display=global_display, save_png=os.path.join(save_dir, "MAVEN_test.png"))
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests


    def test_maven_fluxes_specplot(self):
        del_data("*")

        swe_vars = maven.spdf.load(trange=["2014-10-18", "2014-10-19"], instrument="swea")
        print(swe_vars)
        timespan("2014-10-18", 1, "days")
        # This variable has 3 dimensions but is not marked in the CDF as being a specplot.
        # This used to crash in reduce_spec_dataset because the spec_dim_to_plot option was missing.
        tplot_options("title", "Spec data plotted as lines")
        tplot(
            "diff_en_fluxes",
            display=global_display,
            save_png=os.path.join(save_dir, "MAVEN_fluxes_test_nospec.png"),
        )
        options("diff_en_fluxes", "spec", 1)
        options('diff_en_fluxes', 'sort_spec_bins',True)
        # Setting the "spec" option also sets the spec_dim_to_plot option to v2 in this case
        tplot_options("title", "Plotting as spectrum with default spec_dim_to_plot (v2)")
        tplot("diff_en_fluxes", display=global_display, save_png=os.path.join(save_dir, "MAVEN_fluxes_test_v2.png"))
        # Test that the "v1" option also works (it used to crash looking for "v" and not checking "v1")
        options("diff_en_fluxes", "spec_dim_to_plot", "v1")
        tplot_options("title", "Plotting as spectrum with spec_dim_to_plot=v1")
        tplot("diff_en_fluxes", display=global_display, save_png=os.path.join(save_dir, "MAVEN_fluxes_test_v1.png"))
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests


if __name__ == "__main__":
    unittest.main()
