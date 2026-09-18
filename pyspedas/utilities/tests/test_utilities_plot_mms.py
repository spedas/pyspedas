"""Plot tests that load MMS mission data."""

import os
import unittest
from pyspedas.projects import mms
from pyspedas import del_data, options, store_data, timespan, tplot, tplot_copy, tplot_options

from pyspedas.utilities.config_testing import TESTING_CONFIG

global_display = False
save_dir = os.path.join(TESTING_CONFIG["local_testing_dir"], "utilities")
os.makedirs(save_dir, exist_ok=True)


class PlotTestCases(unittest.TestCase):
    def test_mms_epsd_specplot(self):
        del_data("*")

        timespan("2015-08-01", 1, "days")
        # Logarithmic Y scale with lowest bin boundary = 0.0 by linear extrapolation from bin centers
        data = mms.mms_load_dsp(
            trange=["2015-08-01", "2015-08-02"],
            datatype=["epsd", "bpsd"],
            level="l2",
            data_rate="fast",
        )
        self.assertTrue("mms1_dsp_epsd_omni" in data)
        # options('mms1_dsp_epsd_omni','yrange',[8.0,130000.0])
        tplot(
            ["mms1_dsp_epsd_omni", "mms1_dsp_bpsd_omni"],
            display=global_display,
            save_png=os.path.join(save_dir, "mms1_epsd_omni.png"),
        )
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests


    def test_pseudo_spectra_plus_line(self):
        del_data("*")

        mms.fpi(datatype="des-moms", trange=["2015-10-16", "2015-10-17"])
        mms.edp(trange=["2015-10-16", "2015-10-17"], datatype="scpot")
        # Create a pseudovariable with an energy spectrum plus a line plot of spacecraft potential
        store_data("spec", data=["mms1_des_energyspectr_omni_fast", "mms1_edp_scpot_fast_l2"])
        # Set some options so that the spectrum, trace, and y axes are legible
        options("mms1_edp_scpot_fast_l2", "yrange", [10, 100])
        options("mms1_edp_scpot_fast_l2", "alpha", 0.5)
        # options('mms2_edp_scpot_fast_l2', 'right_axis', True)
        options("spec", "right_axis", "True")
        options("mms1_des_energyspectr_omni_fast", "ztitle", "This is a green ztitle")
        options("mms1_des_energyspectr_omni_fast", "zsubtitle", "This is a green z subtitle")
        options("mms1_des_energyspectr_omni_fast", "ztitle_color", "green")
        options("mms1_des_energyspectr_omni_fast", "second_axis_size", 0.14)
        tplot_options("xmargin", [0.1, 0.2])
        timespan("2015-10-16", 1, "days")
        tplot_options(
            "title",
            "Pseudovar with energy spectrum plus line plot of s/c potential, combined var has right_axis set\nTop: spec Middle: combined Bottom: line",
        )
        tplot(
            "mms1_des_energyspectr_omni_fast spec mms1_edp_scpot_fast_l2",
            xsize=12,
            display=global_display,
            save_png=os.path.join(save_dir, "MMS_pseudo_spec_plus_line.png"),
        )
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests


    def test_pseudo_spectra_plus_line_pseudovar_options(self):
        del_data("*")

        mms.fpi(datatype="des-moms", trange=["2015-10-16", "2015-10-17"])
        mms.edp(trange=["2015-10-16", "2015-10-17"], datatype="scpot")
        # Create a pseudovariable with an energy spectrum plus a line plot of spacecraft potential
        store_data("spec", data=["mms1_des_energyspectr_omni_fast", "mms1_edp_scpot_fast_l2"])
        # Set some options so that the spectrum, trace, and y axes are legible
        options("mms1_edp_scpot_fast_l2", "yrange", [10, 100])
        options("mms1_edp_scpot_fast_l2", "alpha", 0.5)
        # options('mms2_edp_scpot_fast_l2', 'right_axis', True)
        options("spec", "right_axis", "True")
        options("spec", "ztitle", "This is a ztitle")
        options("spec", "zsubtitle", "This is a z subtitle")
        options("spec", "ztitle_color", "green")
        # Pseudovar option should override base variable option
        options("mms1_des_energyspectr_omni_fast", "ztitle_color", "red")
        options("spec", "second_axis_size", 0.14)
        tplot_options("xmargin", [0.1, 0.2])
        timespan("2015-10-16", 1, "days")
        tplot_options(
            "title",
            "Pseudovar with energy spectrum plus line plot of s/c potential, combined var has right_axis set\nTop: spec with red ztitle Middle: combined Bottom: line\nShould have ztitle, zsubtitle in green on center panel only",
        )
        tplot(
            "mms1_des_energyspectr_omni_fast spec mms1_edp_scpot_fast_l2",
            xsize=12,
            display=global_display,
            save_png=os.path.join(save_dir, "MMS_pseudo_spec_plus_line_pseudovar_options.png"),
        )
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests


    def test_pseudo_spectra_plus_line_copy(self):
        del_data("*")

        mms.fpi(datatype="des-moms", trange=["2015-10-16", "2015-10-17"])
        mms.edp(trange=["2015-10-16", "2015-10-17"], datatype="scpot")
        # Create a pseudovariable with an energy spectrum plus a line plot of spacecraft potential
        store_data("spec", data=["mms1_des_energyspectr_omni_fast", "mms1_edp_scpot_fast_l2"])
        # Set some options so that the spectrum, trace, and y axes are legible
        options("mms1_edp_scpot_fast_l2", "yrange", [10, 100])
        # options('mms2_edp_scpot_fast_l2', 'right_axis', True)
        options("spec", "right_axis", "True")
        tplot_options("xmargin", [0.1, 0.2])
        timespan("2015-10-16", 1, "days")
        tplot_options("title", "Pseudovar with energy spectrum plus line plot of s/c potential")
        tplot_copy("spec", "spec_copy")
        tplot(
            "spec_copy",
            xsize=12,
            display=global_display,
            save_png=os.path.join(save_dir, "MMS_pseudo_spec_plus_line.png"),
        )
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests


if __name__ == "__main__":
    unittest.main()
