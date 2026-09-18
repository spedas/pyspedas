"""Plot tests that load ERG mission data."""

import os
import unittest
import pyspedas
from pyspedas.projects import erg
from pyspedas import del_data, options, split_vec, timespan, tplot, tplot_options

from pyspedas.utilities.config_testing import TESTING_CONFIG

global_display = False
save_dir = os.path.join(TESTING_CONFIG["local_testing_dir"], "utilities")
os.makedirs(save_dir, exist_ok=True)


class PlotTestCases(unittest.TestCase):
    def test_erg_specplot(self):
        del_data("*")

        # ERG specplots, only vertical lines on the bottom panel for original resample...
        erg.hep(trange=["2017-03-27", "2017-03-28"])
        timespan("2017-03-27", 1, "days")
        tplot_options("title", "Time varying spectral bins, should render correctly")
        tplot(
            ["erg_hep_l2_FEDO_L", "erg_hep_l2_FEDO_H"],
            display=global_display,
            save_png=os.path.join(save_dir, "ERG_test.png"),
        )
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests


    def test_original_tplot_vlabels(self):
        # Test alternate varlabel implementation from Tomo Hori
        del_data("*")

        timespan("2017-03-27", 1, "days")
        erg.mgf()
        erg.orb()

        split_vec("erg_orb_l2_pos_rmlatmlt")
        split_vec("erg_orb_l2_pos_Lm")
        options("erg_orb_l2_pos_rmlatmlt_x", "ytitle", "R")
        options("erg_orb_l2_pos_rmlatmlt_y", "ytitle", "Mlat")
        options("erg_orb_l2_pos_rmlatmlt_z", "ytitle", "MLT")

        var_label = [
            "erg_orb_l2_pos_Lm_x",
            "erg_orb_l2_pos_rmlatmlt_x",
            "erg_orb_l2_pos_rmlatmlt_y",
            "erg_orb_l2_pos_rmlatmlt_z",
        ]
        # tplot_options('var_label', var_label)

        plot_vars = [
            "erg_mgf_l2_mag_8sec_sm",
            "erg_mgf_l2_igrf_8sec_sm",
            "erg_orb_l2_pos_Lm_x",
        ]
        tplot_options("varlabel_style", "extra_axes")

        tplot(
            plot_vars,
            var_label=var_label,
            display=global_display,
            save_png=os.path.join(save_dir, "original_varlabel.png"),
        )
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests
        tplot_options("title", "")


    def test_original_tplot_vlabels_custom_fontsize(self):
        # Test alternate varlabel implementation from Tomo Hori
        del_data("*")

        # Preserve original axis_font_size and charsize

        old_axis_font_size = pyspedas.tplot_tools.tplot_opt_glob.get('axis_font_size')
        old_charsize = pyspedas.tplot_tools.tplot_opt_glob.get('charsize')

        tplot_options('axis_font_size',20)
        tplot_options('charsize',20)
        tplot_options("title", 'varlabel annotations should match rest of plot')
        timespan("2017-03-27", 1, "days")
        erg.mgf()
        erg.orb()

        split_vec("erg_orb_l2_pos_rmlatmlt")
        split_vec("erg_orb_l2_pos_Lm")
        options("erg_orb_l2_pos_rmlatmlt_x", "ytitle", "R")
        options("erg_orb_l2_pos_rmlatmlt_y", "ytitle", "Mlat")
        options("erg_orb_l2_pos_rmlatmlt_z", "ytitle", "MLT")

        var_label = [
            "erg_orb_l2_pos_Lm_x",
            "erg_orb_l2_pos_rmlatmlt_x",
            "erg_orb_l2_pos_rmlatmlt_y",
            "erg_orb_l2_pos_rmlatmlt_z",
        ]
        # tplot_options('var_label', var_label)

        plot_vars = [
            "erg_mgf_l2_mag_8sec_sm",
            "erg_mgf_l2_igrf_8sec_sm",
            "erg_orb_l2_pos_Lm_x",
        ]

        tplot_options("varlabel_style", "extra_axes")

        tplot(
            plot_vars,
            var_label=var_label,
            display=global_display,
            save_png=os.path.join(save_dir, "original_varlabel_custom_fontsize.png"),
        )
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests
        tplot_options("title", "")
        tplot_options('axis_font_size',old_axis_font_size)
        tplot_options('charsize',old_charsize)


    def test_tplot_vlabels_extra_panel(self):
        # Test alternate varlabel implementation from Tomo Hori
        del_data("*")
        timespan("2017-03-27", 1, "days")
        erg.mgf()
        erg.orb()

        split_vec("erg_orb_l2_pos_rmlatmlt")
        split_vec("erg_orb_l2_pos_Lm")
        options("erg_orb_l2_pos_rmlatmlt_x", "ytitle", "R")
        options("erg_orb_l2_pos_rmlatmlt_y", "ytitle", "Mlat")
        options("erg_orb_l2_pos_rmlatmlt_z", "ytitle", "MLT")

        var_label = [
            "erg_orb_l2_pos_Lm_x",
            "erg_orb_l2_pos_rmlatmlt_x",
            "erg_orb_l2_pos_rmlatmlt_y",
            "erg_orb_l2_pos_rmlatmlt_z",
        ]
        # tplot_options('var_label', var_label)
        tplot_options("varlabel_style", "extra_panel")
        plot_vars = [
            "erg_mgf_l2_mag_8sec_sm",
            "erg_mgf_l2_igrf_8sec_sm",
            "erg_orb_l2_pos_Lm_x",
        ]

        tplot(
            plot_vars,
            var_label=var_label,
            display=global_display,
            save_png=os.path.join(save_dir, "varlabel_extra_panel.png"),
        )

        options(var_label, "var_label_format", "{:.1f}")
        tplot_options("title", "Var labels should all have 1 digit after the decimal point")
        tplot(
            plot_vars,
            var_label=var_label,
            display=global_display,
            save_png=os.path.join(save_dir, "varlabel_extra_panel_single_decimal.png"),
        )
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests
        tplot_options("varlabel_style", None)
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests


if __name__ == "__main__":
    unittest.main()
