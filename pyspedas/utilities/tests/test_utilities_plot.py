"""Test plotting functions (mostly for pseudovariables)"""

import os
import unittest
import numpy as np
from pyspedas.projects import themis, elfin, fast, erg, maven, mms, psp
from pyspedas import (
    store_data,
    options,
    timespan,
    tplot,
    tplot_options,
    degap,
    del_data,
    databar,
    ylim,
    xlim,
    zlim,
    time_double,
    timebar,
    highlight,
    get_data,
    tplot_copy,
    split_vec,
    count_traces,
    annotate,
    is_pseudovariable,
)
from pyspedas.utilities.config_testing import TESTING_CONFIG

# Whether to display plots during testing
global_display = TESTING_CONFIG["global_display"]
# Directory to save testing output files
output_dir = TESTING_CONFIG["local_testing_dir"]
# Ensure output directory exists
save_dir = os.path.join(output_dir, "utilities")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

default_trange = ["2007-03-23", "2007-03-24"]


class PlotTestCases(unittest.TestCase):
    """Test plot functions."""

    def test_markers_and_symbols(self):
        # Regression test for lineplot crash when marker sizes are set
        # Taken from pytplot markers and symbols notebook in pyspedas_examples
        del_data("*")
        store_data("data", data={"x": [1, 2, 3, 4, 5, 6], "y": [1, 1, 1, 1, 1, 1]})
        timespan("1970-01-01", 10, "seconds")
        tplot_options("title", "Simple line plot")
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "simple_lineplot.png"))
        options("data", "marker", "X")
        tplot_options("title", "Simple line plot with X markers")
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "markers_lineplot.png"))
        options("data", "linestyle", "None")
        tplot_options("title", "Symbol-only plot with X markers")
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "noline_lineplot.png"))
        options("data", "marker_size", 200)
        tplot_options("title", "Symbol-only plot with size 200 markers")
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "markersize_lineplot.png"))
        options("data", "line_style_name", "solid")
        tplot_options("title", "Line+symbol plot with size 200 markers")
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "markersize_nosymbols_lineplot.png"))
        options("data", "marker_size", 20)
        tplot_options("title", "Line+symbol plot with error bars and size 20 markers")
        tplot(
            "data",
            display=global_display,
            save_png=os.path.join(save_dir, "markersize20_nosymbols_lineplot.png"),
        )
        options("data", "markevery", 2)
        tplot_options("title", "Line+symbol plot with error bars and markers every 2 data points")
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "markevery_lineplot.png"))
        options("data", "marker", "H")
        tplot_options("title", "Line plot with error bars and hexagon markers")
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "hexagons_lineplot.png"))
        timespan("2007-03-23", 1, "days")  # reset to avoid interfering with other tests
        tplot_options("title", "")

    def test_markers_and_symbols_error_bars(self):
        # Regression test for lineplot crash when marker sizes are set
        # Taken from pytplot markers and symbols notebook in pyspedas_examples
        del_data("*")
        store_data(
            "data",
            data={"x": [1, 2, 3, 4, 5, 6], "y": [1, 1, 1, 1, 1, 1], "dy": [0.25] * 6},
        )
        timespan("1970-01-01", 10, "seconds")
        tplot_options("title", "Line plot with error bars")
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "simple_lineplot_errbars.png"))
        options("data", "marker", "X")
        tplot_options("title", "Line plot with error bars and X markers")
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "markers_lineplot_errbars.png"))
        options("data", "line_style", "None")
        tplot_options("title", "X markers and error bars with no lines")
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "symbols_lineplot_errbars.png"))
        options("data", "marker_size", 30)
        tplot_options("title", "No lines, size 30 X markers and error bars")
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "markersize_lineplot_errbars.png"))
        options("data", "marker", None)
        options("data", "line_style", "solid")
        tplot_options("title", "Line plot without markers with error bars")
        tplot(
            "data",
            display=global_display,
            save_png=os.path.join(save_dir, "markersize_nosymbols_lineplot_errbars.png"),
        )
        options("data", "marker_size", 20)
        options("data", "line_style", "None")
        options("data", "symbols", False)
        tplot_options("title", "Error bars, no lines, with size 20 markers but symbols=False")
        tplot(
            "data",
            display=global_display,
            save_png=os.path.join(save_dir, "markersize20_nosymbols_lineplot_errbars.png"),
        )
        options("data", "markevery", 2)
        options("data", "marker", "X")
        options("data", "line_style", "solid")
        tplot_options("title", "Line plot error bars and markers every 2 data points")
        options("data", "markevery", 2)
        options("data", "errorevery", 3)
        options("data", "marker", "X")
        options("data", "line_style", "solid")
        tplot_options("title", "Line plot error bars every 3 and markers every 2 data points")
        tplot(
            "data",
            display=global_display,
            save_png=os.path.join(save_dir, "markevery_errorevery_lineplot_errbars.png"),
        )
        options("data", "marker", "H")
        tplot_options("title", "Line plot with error bars and hexagon markers")
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "hexagons_lineplot_errbars.png"))
        options("data", "capsize", 10)
        options("data", "ecolor", "r")
        options("data", "elinewidth", 5)
        tplot_options("title", "Line plot with red error bars and hexagon markers, capsize=10")
        tplot(
            "data",
            display=global_display,
            save_png=os.path.join(save_dir, "hexagons_lineplot_errbars_cap10redwidth5.png"),
        )
        timespan("2007-03-23", 1, "days")  # reset to avoid interfering with other tests
        tplot_options("title", "")

    def test_plot_titles(self):
        # Regression test for lineplot crash when marker sizes are set
        # Taken from pytplot markers and symbols notebook in pyspedas_examples
        del_data("*")
        store_data("data", data={"x": [1, 2, 3, 4, 5, 6], "y": [1, 1, 1, 1, 1, 1]})
        timespan("1970-01-01", 10, "seconds")
        tplot_options("title", "This title should be visible")
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "simple_title.png"))
        tplot_options("title", "This title should be in a larger font")
        tplot_options("title_size", 20)
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "title_titlesize.png"))
        tplot_options("title_size", 12)
        tplot_options("title", "")
        options("data", "xtitle", "There should be no main title displayed. char_size=20")
        options("data", "xsubtitle", "this is an x subtitle")
        options("data", "xtitle_color", "red")
        options("data", "ytitle", "This is a ytitle")
        options("data", "ysubtitle", "this is a y subtitle")
        options("data", "ytitle_color", "green")
        options("data", "char_size", 20)
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "title_emptystring.png"))
        tplot_options("title", None)
        options("data", "xtitle", "There should be no main title displayed")
        tplot("data", display=global_display, save_png=os.path.join(save_dir, "title_none.png"))
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # reset to avoid interfering with other tests

    def test_time_data_bars(self):
        del_data("*")
        timespan("2007-03-23", 1, "days")  # reset to avoid interfering with other tests
        themis.fgm(probe="c", trange=default_trange)
        # use timebar to place a databar
        timebar(t=10000.0, varname="thc_fge_dsl", databar=True, color="black")
        # use databar to place a databar
        databar("thc_fgs_dsl", -10000.0, color="red", dash=True)
        timebar(t=-10000.0, varname="thc_fge_dsl", databar=True, color="red", dash=True)
        timebar(
            t=time_double("2007-03-23/14:00"),
            varname="thc_fge_btotal",
            color="magenta",
        )
        timebar(t=time_double("2007-03-23/14:30"), color="blue")
        timebar(t=time_double("2007-03-23/15:30"), color="green", dash=True)
        tplot_options(
            "title",
            "Databars at +/- 10000 top panel, timebars at 14:30 and 15:30 all panels, timebar at 14:00 bottom panel, linestyles and colors as specified",
        )
        tplot(
            ["thc_fge_dsl", "thc_fge_btotal"],
            display=global_display,
            save_png=os.path.join(save_dir, "timebars.png"),
        )
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # reset to avoid interfering with other tests

    def test_line_pseudovariables(self):
        del_data("*")
        # Test that tplot variables with different number of traces can be combined into a pseudovariable and plotted correctly.
        # Both plots should have 4 properly labeled traces.
        themis.fgm(probe="c", trange=default_trange)
        timespan("2007-03-23", 1, "days")  # reset to avoid interfering with other tests
        store_data("comb_3_1", data=["thc_fge_dsl", "thc_fge_btotal"])
        store_data("comb_1_3", data=["thc_fge_btotal", "thc_fge_dsl"])
        tplot_options("title", "Pseudovariable with one+three line traces")
        tplot("comb_1_3", display=global_display, save_png=os.path.join(save_dir, "pseudovars_comb_1_3.png"))
        tplot_options("title", "Pseudovariable with three+one line traces")
        tplot("comb_3_1", display=global_display, save_png=os.path.join(save_dir, "pseudovars_comb_3_1.png"))
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # reset to avoid interfering with other tests

    def test_pseudovar_color_options(self):
        del_data("*")
        themis.fgm(probe="c", trange=default_trange)
        timespan("2007-03-23", 1, "days")
        store_data("test_pseudo_colors", data=["thc_fge_dsl", "thc_fge_btotal"])
        # Set the color option on the pseudovariable (4 traces total, so 4 colors)
        options("test_pseudo_colors", "color", ["k", "r", "g", "b"])
        tplot_options("title", "Trace colors should be black, red, green, blue")
        tplot(
            "test_pseudo_colors",
            display=global_display,
            save_png=os.path.join(save_dir, "test_pseudo_colors_4color.png"),
        )  # should plot without "incorrect number of line colors" messages
        options("test_pseudo_colors", "color", ["k"])  # All black
        tplot_options("title", "Trace colors all black")
        tplot(
            "test_pseudo_colors",
            display=global_display,
            save_png=os.path.join(save_dir, "test_pseudo_colors_allsamecolor.png"),
        )
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

    def test_var_line_options(self):
        del_data("*")
        themis.fgm(probe="c", trange=default_trange)
        timespan("2007-03-23", 1, "days")
        options("thc_fgs_dsl", "line_style", ["solid", "dot", "dash"])
        tplot_options("title", "Line styles solid, dot, dash")
        tplot("thc_fgs_dsl", display=global_display, save_png=os.path.join(save_dir, "test_linestyle_3styles.png"))
        options("thc_fgs_dsl", "line_style", "dot")  # gets used for all lines
        tplot_options("title", "Line styles all dot")
        tplot("thc_fgs_dsl", display=global_display, save_png=os.path.join(save_dir, "test_linestyle_allsame.png"))
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

    def test_ytick_options(self):
        del_data("*")
        themis.fgm(probe="c", trange=default_trange)
        timespan("2007-03-23", 1, "days")
        tplot_options(
            "title",
            "Default major and minor ticks, major ticks every 5000 nT from -5000 to 20000",
        )
        tplot("thc_fgs_dsl", display=global_display, save_png=os.path.join(save_dir, "ticks_default.png"))
        options(
            "thc_fgs_dsl",
            "y_major_ticks",
            [
                -7500,
                -5000,
                -2500,
                0,
                2500,
                5000,
                7500,
                10000,
                12500,
                15000,
                17500,
                20000,
                22500,
                25000,
            ],
        )
        tplot_options("title", "Manual major ticks, every 2500 nT from -7500 to 25000")
        tplot("thc_fgs_dsl", display=global_display, save_png=os.path.join(save_dir, "ticks_major_every2500.png"))
        options("thc_fgs_dsl", "y_minor_tick_interval", 1250)
        tplot_options(
            "title",
            "Manual major and minor ticks, every 2500/1250 nT from -7500 to 25000",
        )
        tplot(
            "thc_fgs_dsl",
            display=global_display,
            save_png=os.path.join(save_dir, "ticks_major_every2500_minor1250.png"),
        )

        tplot_options(
            "title",
            "Y tick options: length 20, tick color green, width 5, labelcolor green, direction inout",
        )
        options("thc_fgs_gse", "ytick_length", 20)
        options("thc_fgs_gse", "ytick_color", "green")
        options("thc_fgs_gse", "ytick_width", 5)
        options("thc_fgs_gse", "ytick_direction", "inout")
        options("thc_fgs_gse", "ytick_labelcolor", "green")
        tplot("thc_fgs_gse", display=global_display, save_png=os.path.join(save_dir, "ytick_multi_options.png"))

        options("thc_fgs_gse", "ytick_length", None)
        options("thc_fgs_gse", "ytick_color", None)
        options("thc_fgs_gse", "ytick_width", None)
        options("thc_fgs_gse", "ytick_direction", None)
        options("thc_fgs_gse", "ytick_labelcolor", None)
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests
        tplot_options("title", "")

    def test_xtick_options(self):
        del_data("*")
        themis.fgm(probe="c", trange=default_trange)
        timespan("2007-03-23", 1, "days")

        tplot_options(
            "title",
            "X tick options: length 20, tick color green, width 5, labelcolor green, direction inout",
        )
        options("thc_fgs_gse", "xtick_length", 20)
        options("thc_fgs_gse", "xtick_color", "green")
        options("thc_fgs_gse", "xtick_width", 5)
        options("thc_fgs_gse", "xtick_direction", "inout")
        options("thc_fgs_gse", "xtick_labelcolor", "green")
        tplot("thc_fgs_gse", display=global_display, save_png=os.path.join(save_dir, "xtick_multi_options.png"))
        options("thc_fgs_gse", "xtick_length", None)
        options("thc_fgs_gse", "xtick_color", None)
        options("thc_fgs_gse", "xtick_width", None)
        options("thc_fgs_gse", "xtick_direction", None)
        options("thc_fgs_gse", "xtick_labelcolor", None)
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests
        tplot_options("title", "")

    def test_ylim(self):
        del_data("*")
        themis.fgm(probe="c", trange=default_trange)
        timespan("2007-03-23", 1, "days")
        ylim("thc_fgs_dsl", -100, 100)
        tplot_options("title", "Y limit [-100, 100]")
        tplot("thc_fgs_dsl", display=global_display, save_png=os.path.join(save_dir, "test_ylim.png"))
        ylim("thc_fgs_dsl", 1, 100, 1)
        tplot_options("title", "Y limit [1, 100, 1] (should be log scaled)")
        tplot("thc_fgs_dsl", display=global_display, save_png=os.path.join(save_dir, "test_ylim_1_100_log.png"))
        ylim("thc_fgs_dsl", 1, 200)
        tplot_options("title", "Y limit [1, 200] (should still be log scaled)")
        tplot("thc_fgs_dsl", display=global_display, save_png=os.path.join(save_dir, "test_ylim_1_200_log.png"))
        ylim("thc_fgs_dsl", 1, 200, logflag=False)
        tplot_options("title", "Y limit [1, 200, False] (should now be linear scale)")
        tplot("thc_fgs_dsl", display=global_display, save_png=os.path.join(save_dir, "test_ylim_1_200_linear.png"))
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

    def test_highlight(self):
        del_data("*")
        themis.fgm(probe="c", trange=default_trange)
        timespan("2007-03-23", 1, "days")
        t1 = time_double("2007-03-23/03:00:00")
        t2 = time_double("2007-03-23/04:00:00")
        t3 = time_double("2007-03-23/05:00:00")
        highlight("thc_fgs_dsl", range=[t1, t2], color="red", alpha=0.2)
        highlight("thc_fgs_*", range=[t2, t3], color="green", alpha=0.2, hatch="o")
        tplot(
            "thc_fgs_dsl thc_fgs_gsm",
            display=global_display,
            save_png=os.path.join(save_dir, "test_highlight.png"),
        )

    def test_annotations(self):
        del_data("*")
        themis.fgm(probe="c", trange=default_trange)
        timespan("2007-03-23", 1, "days")
        t2 = np.datetime64("2007-03-23T18:00")
        y2 = 10000
        # Position relative to panel size
        annotate(
            "thc_fgs_dsl",
            text="Annotation 1",
            position=[0.5, 0.5],
            color="red",
            fontsize=10,
        )
        # Position in data coordinates
        annotate(
            "thc_fgs_gsm",
            text="Annotation 2",
            position=(t2, y2),
            xycoords="data",
            color="blue",
            fontsize=20,
        )
        # Multi-variable annotations using wildcard
        annotate("thc_fgs_*", text="Multi Annotation", position=[0.1, 0.8], color="green")
        tplot(
            "thc_fgs_dsl thc_fgs_gsm",
            display=global_display,
            save_png=os.path.join(save_dir, "test_annotations.png"),
        )
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

    def test_is_pseudovar(self):
        del_data("*")

        themis.fgm(probe="c", trange=default_trange)
        timespan("2007-03-23", 1, "days")
        store_data("test_pseudo_colors", data=["thc_fge_dsl", "thc_fge_btotal"])
        self.assertTrue(is_pseudovariable("test_pseudo_colors"))
        self.assertFalse(is_pseudovariable("thc_fgs_dsl"))
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

    def test_xytitles(self):
        del_data("*")
        themis.fgm(probe="c", trange=default_trange)
        options("thc_fgs_dsl", "xtitle", "thc_fgs_dsl xtitle")
        options("thc_fgs_gsm", "xtitle", "thc_fgs_gsm xtitle")
        options("thc_fgs_dsl", "xsubtitle", "thc_fgs_dsl xsubtitle")
        options("thc_fgs_gsm", "xsubtitle", "thc_fgs_gsm xsubtitle")
        options("thc_fgs_dsl", "ytitle", "thc_fgs_dsl ytitle")
        options("thc_fgs_gsm", "ytitle", "thc_fgs_gsm ytitle")
        options("thc_fgs_dsl", "ysubtitle", "thc_fgs_dsl ysubtitle")
        options("thc_fgs_gsm", "ysubtitle", "thc_fgs_gsm ysubtitle")
        tplot_options("title", "xtitle and xsubtitle should show below each variable panel")
        tplot("thc_fgs_dsl", display=global_display, save_png=os.path.join(save_dir, "test_titles_single.png"))
        tplot(
            "thc_fgs_dsl thc_fgs_gsm",
            display=global_display,
            save_png=os.path.join(save_dir, "test_titles_multi.png"),
        )
        tplot_options("title", "")

    def test_legend(self):
        del_data("*")
        themis.fgm(probe="c", trange=default_trange)
        options("thc_fgs_dsl", "marker", "x")
        options("thc_fgs_dsl", "legend_names", ["X-DSL", "Y-DSL", "Z-DSL"])
        options("thc_fgs_dsl", "legend_title", "legend title")
        options("thc_fgs_dsl", "legend_titlesize", 20)
        options("thc_fgs_dsl", "legend_color", "green")
        options("thc_fgs_dsl", "legend_edgecolor", "blue")
        options("thc_fgs_dsl", "legend_facecolor", "gray")
        options("thc_fgs_dsl", "legend_markerscale", 2)
        options("thc_fgs_dsl", "legend_markerfirst", True)
        options("thc_fgs_dsl", "legend_linewidth", 6)
        options("thc_fgs_dsl", "legend_ncols", 3)
        options("thc_fgs_dsl", "legend_shadow", True)
        options("thc_fgs_dsl", "legend_frameon", True)
        options("thc_fgs_dsl", "legend_location", "spedas")
        tplot("thc_fgs_dsl", display=global_display, save_png=os.path.join(save_dir, "test_legend.png"))

    def test_count_traces(self):
        del_data("*")

        themis.fgm(probe="c", trange=default_trange)
        store_data("test_pseudo_colors", data=["thc_fge_dsl", "thc_fge_btotal"])
        tr_fge = count_traces("thc_fge_dsl")
        tr_btotal = count_traces("thc_fge_btotal")
        tr_pseudo = count_traces("test_pseudo_colors")
        self.assertEqual(tr_fge, 3)
        self.assertEqual(tr_btotal, 1)
        self.assertEqual(tr_pseudo, 4)
        # We need to ensure thc_fge_dsl has a 'v' component, so we can pretend this variable is a spectrogram
        fgs_data = get_data("thc_fge_dsl")
        fgs_meta = get_data("thc_fge_dsl", metadata=True)
        self.assertTrue(fgs_meta is not None)
        store_data("thc_fge_dsl", data={"x": fgs_data.times, "y": fgs_data.y, "v": [0, 1, 2]})
        options("thc_fge_dsl", "spec", 1)
        tr_pseudo_spec = count_traces("test_pseudo_colors")
        self.assertEqual(tr_pseudo_spec, 1)
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

    def test_pseudovar_line_options(self):
        del_data("*")
        themis.fgm(probe="c", trange=default_trange)
        timespan("2007-03-23", 1, "days")
        store_data("test_pseudo_lineopts", data=["thc_fge_dsl", "thc_fge_btotal"])
        # Set the line_style on the pseudovariable (4 traces total, so 4 styles)
        options("test_pseudo_lineopts", "line_style", ["dot", "dash", "solid", "dash_dot"])
        tplot_options("title", "Pseudovar line styles dot, dash, solid, dash_dot")
        tplot(
            "test_pseudo_lineopts",
            display=global_display,
            save_png=os.path.join(save_dir, "test_pseudo_lineopts_4style.png"),
        )
        # Set all traces to the same style
        options("test_pseudo_lineopts", "line_style", "dot")
        tplot_options("title", "Pseudovar line styles all dot")
        tplot(
            "test_pseudo_lineopts",
            display=global_display,
            save_png=os.path.join(save_dir, "test_pseudo_lineopts_allsame"),
        )
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

    def test_specplot_optimizations(self):
        del_data("*")
        ask_vars = themis.ask(trange=["2013-11-05", "2013-11-06"])
        self.assertTrue(len(ask_vars) > 0)
        timespan("2013-11-05", 1, "days")
        # Should plot without errors, show something other than all-blue or vertical lines
        tplot_options("title", "Should be mostly dark with a few lighter features")
        tplot(["thg_ask_atha"], display=global_display, save_png=os.path.join(save_dir, "thg_ask_atha.png"))
        options("thg_ask_atha", "y_no_resample", 1)
        tplot_options("title", "Should be mostly dark with a few lighter features")
        tplot("thg_ask_atha", display=global_display, save_png=os.path.join(save_dir, "thg_ask_atha_no_resample.png"))
        tplot_options("title", "Should be somewhat lighter now with logarithmic z scale")
        options("thg_ask_atha", "zlog", "log")
        tplot(
            "thg_ask_atha",
            display=global_display,
            save_png=os.path.join(save_dir, "thg_ask_atha_no_resample_zlog.png"),
        )
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

    def test_themis_peef_bins(self):
        del_data("*")
        themis.esa(probe="a", trange=["2016-12-11", "2016-12-12"])
        timespan("2016-12-11", 1, "days")
        options("tha_peef_en_eflux", "yrange", [1000, 3000])
        tplot_options(
            "title",
            "Logarithmic bin boundaries: should be a boundary at y~=1947 eV, just below the tick mark at y=2000",
        )
        tplot("tha_peef_en_eflux", display=global_display, save_png=os.path.join(save_dir, "tha_peef_en_eflux.png"))
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

    def test_themis_peef_bins_interp_x(self):
        del_data("*")
        themis.esa(probe="a", trange=["2016-12-11", "2016-12-12"])
        timespan("2016-12-11", 1, "hours")
        options("tha_peef_en_eflux", "yrange", [1000, 3000])
        options("tha_peef_en_eflux", "x_interp", 1)
        options("tha_peef_en_eflux", "x_interp_points", 500)
        tplot_options("title", "Interpolated along time axis")
        tplot(
            "tha_peef_en_eflux",
            display=global_display,
            save_png=os.path.join(save_dir, "tha_peef_en_eflux_interp_x.png"),
        )
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests
        options("tha_peef_en_eflux", "x_interp", 0)  # reset for other tests

    def test_themis_peef_bins_interp_y(self):
        del_data("*")
        themis.esa(probe="a", trange=["2016-12-11", "2016-12-12"])
        timespan("2016-12-11", 1, "hours")
        options("tha_peef_en_eflux", "yrange", [1000, 3000])
        options("tha_peef_en_eflux", "y_interp", 1)
        options("tha_peef_en_eflux", "y_interp_points", 200)
        tplot_options("title", "Interpolated along y axis")
        tplot(
            "tha_peef_en_eflux",
            display=global_display,
            save_png=os.path.join(save_dir, "tha_peef_en_eflux_interp_y.png"),
        )
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests
        options("tha_peef_en_eflux", "y_interp", 0)  # reset for other tests

    def test_themis_peef_bins_interp_both(self):
        del_data("*")
        themis.esa(probe="a", trange=["2016-12-11", "2016-12-12"])
        timespan("2016-12-11", 1, "hours")
        options("tha_peef_en_eflux", "yrange", [1000, 3000])
        options("tha_peef_en_eflux", "x_interp", 1)
        options("tha_peef_en_eflux", "x_interp_points", 500)
        options("tha_peef_en_eflux", "y_interp", 1)
        options("tha_peef_en_eflux", "y_interp_points", 200)
        tplot_options("title", "Interpolated along both x and y axes")
        tplot(
            "tha_peef_en_eflux",
            display=global_display,
            save_png=os.path.join(save_dir, "tha_peef_en_eflux_interp_both.png"),
        )
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests
        options("tha_peef_en_eflux", "x_interp", 0)  # reset for other tests
        options("tha_peef_en_eflux", "y_interp", 0)  # reset for other tests

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

    def test_elfin_specplot(self):
        del_data("*")

        # ELFIN data with V values that oscillate, the original problem that resulted in the resample, this is an angular distrubtion
        timespan("2021-07-14/11:55", 10, "minutes")
        epd_var = elfin.epd(
            trange=["2021-07-14/11:55", "2021-07-14/12:05"],
            probe="a",
            level="l2",
            type_="nflux",
            fullspin=False,
        )
        self.assertTrue("ela_pef_hs_nflux_ch0" in epd_var)
        tplot_options("title", "ELFIN data with time-varying bins, should render accurately")
        tplot("ela_pef_hs_nflux_ch0", display=global_display, save_png=os.path.join(save_dir, "ELFIN_test.png"))
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # reset to avoid interfering with other tests

    def test_fast_specplot(self):
        del_data("*")

        # FAST TEAMS has fill values -1e31 in V, top is an energy distribution, the bottom two are pitch angle distributions
        teams_vars = fast.teams(["1998-09-05", "1998-09-06"], level="k0")
        self.assertTrue(len(teams_vars) > 0)
        timespan("1998-09-05", 1, "days")
        tplot_options("title", "Fill should be removed, bottom two panels should go to Y=-90 deg")
        # Specify variables to plot as a space-delimited string with wildcards
        tplot("*H+ *H+_low *H+_high", display=global_display, save_png=os.path.join(save_dir, "TEAMS_test.png"))
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # reset to avoid interfering with other tests

    def test_themis_esa_specplot(self):
        del_data("*")

        # THEMIS ESA has monotonically decreasing energies, time varying energies, and also has fill
        esa_vars = themis.esa(trange=["2016-07-23", "2016-07-24"], probe="a")
        self.assertTrue(len(esa_vars) > 0)
        timespan("2016-07-23", 1, "days")
        tplot_options(
            "title",
            "Decreasing and time-varying energies, fillvals, should render correctly",
        )
        tplot("tha_peef_en_eflux", display=global_display, save_png=os.path.join(save_dir, "PEEF_test.png"))
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

    def test_themis_esa_copy_specplot(self):
        del_data("*")

        # THEMIS ESA has monotonically decreasing energies, time varying energies, and also has fill
        esa_vars = themis.esa(trange=["2016-07-23", "2016-07-24"], probe="a")
        self.assertTrue(len(esa_vars) > 0)
        timespan("2016-07-23", 1, "days")
        tplot_options(
            "title",
            "Decreasing and time-varying energies, fillvals, should render correctly",
        )
        tplot_copy("tha_peef_en_eflux", new_name="tha_peef_copy")
        tplot("tha_peef_copy", display=global_display, save_png=os.path.join(save_dir, "PEEF_copy_test.png"))
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

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

    # @unittest.skip(reason="Failing until we establish a default for spec_dim_to_plot")
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
        # Setting the "spec" option also sets the spec_dim_to_plot option to v2 in this case
        tplot_options("title", "Plotting as spectrum with default spec_dim_to_plot (v2)")
        tplot("diff_en_fluxes", display=global_display, save_png=os.path.join(save_dir, "MAVEN_fluxes_test_v2.png"))
        # Test that the "v1" option also works (it used to crash looking for "v" and not checking "v1")
        options("diff_en_fluxes", "spec_dim_to_plot", "v1")
        tplot_options("title", "Plotting as spectrum with spec_dim_to_plot=v1")
        tplot("diff_en_fluxes", display=global_display, save_png=os.path.join(save_dir, "MAVEN_fluxes_test_v1.png"))
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

    def test_pseudovars_title(self):
        del_data("*")

        themis.state(probe="c", trange=default_trange)
        store_data("ps1", ["thc_spin_initial_delta_phi", "thc_spin_idpu_spinper"])
        store_data("ps2", ["thc_spin_initial_delta_phi", "thc_spin_idpu_spinper"])
        store_data("ps3", ["thc_spin_initial_delta_phi", "thc_spin_idpu_spinper"])
        tplot_options("title", "Plot title should only appear once at top of plot")
        plotvars = ["thc_pos", "ps1", "thc_vel", "ps2", "thc_pos_gse", "ps3"]
        # Should have only one title at the top of the plot
        tplot(plotvars, save_png=os.path.join(save_dir, "test_pseudovars_title.png"), display=global_display)
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

    def test_pseudovars_spectra(self):
        del_data("*")

        # Load ESA and SST data
        themis.esa(probe="a", trange=default_trange)
        themis.sst(probe="a", trange=default_trange)

        # Make a combined variable with both ESA and SST spectral data (disjoint energy ranges)
        store_data("combined_spec", ["tha_peif_en_eflux", "tha_psif_en_eflux"])
        options("tha_peif_en_eflux", "y_no_resample", 1)
        # options('combined_spec','y_range',[5.0, 7e+06])
        vars = ["tha_psif_en_eflux", "combined_spec", "tha_peif_en_eflux"]
        tplot_options(
            "title",
            "Pseudovar with two spectra, disjoint energies: top=SST, middle=combined, bottom=ESA\nMiddle plot y range should go down to near zero",
        )
        tplot(
            vars,
            display=global_display,
            save_png=os.path.join(save_dir, "test_pseudo_spectra_disjoint_energies.png"),
        )

        tplot_options("title", "Original burst variable")
        tplot("tha_peib_en_eflux", display=global_display)
        degap("tha_peib_en_eflux", dt=4.0)
        tplot_options("title", "Degapped burst variable")
        tplot("tha_peib_en_eflux", display=global_display)
        # Make a combined variable with full & burst data (same energy ranges, intermittent burst data at higher cadence)
        store_data("esa_srvy_burst", ["tha_peif_en_eflux", "tha_peib_en_eflux"])
        # zlim('tha_peif_en_eflux', 1.0e3, 1.0e7)
        # options('tha_peif_en_eflux', 'y_range', [0.5, 1.0e6])

        options("tha_peib_en_eflux", "y_no_resample", 1)
        # zlim('tha_peib_en_eflux', 1.0e3, 1.0e7)
        # options('tha_peib_en_eflux', 'y_range', [0.5, 1.0e6])
        options("tha_peib_en_eflux", "data_gap", 4.0)
        vars = ["tha_peif_en_eflux", "esa_srvy_burst", "tha_peib_en_eflux"]
        tplot_options(
            "title",
            "Combining full & burst cadence with same energies: top=fast, middle=combined, bot=burst",
        )
        tplot(vars, display=global_display, save_png=os.path.join(save_dir, "test_pseudo_spectra_full_burst.png"))
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

        # Zoom in o a burst interval
        # timespan('2007-03-23/12:20', 10, 'minutes')
        tplot_options(
            "title",
            "Combined full and burst cadence with same energies (zoomed in) top=fast, mid=combined, bot=burst",
        )
        tplot(
            vars,
            trange=["2007-03-23/12:20", "2007-03-23/12:30"],
            display=global_display,
            save_png=os.path.join(save_dir, "test_pseudo_spectra_full_burst_zoomed.png"),
        )
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests
        tplot_options("title", "")

    def test_pseudovars_spectra_explicit_yzranges(self):
        del_data("*")

        # Load ESA and SST data
        themis.esa(probe="a", trange=default_trange)
        themis.sst(probe="a", trange=default_trange)

        # Make a combined variable with both ESA and SST spectral data (disjoint energy ranges)
        store_data("combined_spec", ["tha_peif_en_eflux", "tha_psif_en_eflux"])
        options("tha_peif_en_eflux", "y_no_resample", 1)
        options("combined_spec", "y_range", [0.1, 7e06])
        vars = ["tha_psif_en_eflux", "combined_spec", "tha_peif_en_eflux"]
        tplot_options(
            "title",
            "Pseudovar with two spectra, disjoint energies: top=SST, middle=combined, bottom=ESA\nMiddle plot y range should go down to 0.1",
        )
        tplot(
            vars,
            display=global_display,
            save_png=os.path.join(save_dir, "test_pseudo_spectra_disjoint_energies_explicityrange.png"),
        )

        tplot_options(
            "title",
            "Pseudovar with two spectra, disjoint energies: top=SST, middle=combined, bottom=ESA\nMiddle plot should have linear Y axis",
        )
        options("combined_spec", "ylog", False)
        tplot(
            vars,
            display=global_display,
            save_png=os.path.join(save_dir, "test_pseudo_spectra_disjoint_energies_explicityrange_linear.png"),
        )

        store_data("esa_srvy_burst", ["tha_peif_en_eflux", "tha_peib_en_eflux"])
        options("tha_peib_en_eflux", "y_no_resample", 1)
        zlim("tha_peib_en_eflux", 1.0e3, 1.0e7)
        options("tha_peib_en_eflux", "y_range", [0.5, 1.0e6])
        options("tha_peib_en_eflux", "data_gap", 4.0)
        vars = ["tha_peif_en_eflux", "esa_srvy_burst", "tha_peib_en_eflux"]
        zlim("esa_srvy_burst", 1.0e3, 1.0e20)
        tplot_options(
            "title",
            "Combining full & burst cadence with same energies: top=fast, middle=combined, bot=burst\nMiddle panel should have an expanded zrange (high max)",
        )
        tplot(
            vars,
            display=global_display,
            save_png=os.path.join(save_dir, "test_pseudo_spectra_full_burst_explicitzrange.png"),
        )
        zlim("esa_srvy_burst", 1.0e5, 1.0e6, False)
        tplot_options(
            "title",
            "Combining full & burst cadence with same energies: top=fast, middle=combined, bot=burst\nMiddle panel should have a reduced zrange with linear scaling",
        )
        tplot(
            vars,
            display=global_display,
            save_png=os.path.join(save_dir, "test_pseudo_spectra_full_burst_explicitzrange_zlin.png"),
        )
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests
        tplot_options("title", "")

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
        options("mms1_des_energyspectr_omni_fast", "ztitle", "This is a ztitle")
        options("mms1_des_energyspectr_omni_fast", "zsubtitle", "This is a z subtitle")
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

    def test_psp_flux_plot(self):
        del_data("*")

        spi_vars = psp.spi(
            trange=["2022-12-12/00:00", "2022-12-12/23:59"],
            datatype="sf00_l3_mom",
            level="l3",
            time_clip=True,
        )
        self.assertTrue(len(spi_vars) > 0)
        d0 = get_data("psp_spi_EFLUX_VS_ENERGY")
        time = d0.times
        # print(time)

        d1 = get_data("psp_spi_EFLUX_VS_ENERGY")
        energy_channel = d1.v
        # print(energy_channel)

        d2 = get_data("psp_spi_EFLUX_VS_ENERGY")
        energy_flux = d2.y
        # print(energy_flux)
        # e_flux = data_quants["psp_spi_EFLUX_VS_ENERGY"].coords["v"].values
        energy_flux[energy_flux == 0] = np.nan
        store_data("E_Flux", data={"x": time.T, "y": energy_flux, "v": energy_channel})
        options("E_Flux", opt_dict={"Spec": 1, "zlog": 1, "Colormap": "jet", "ylog": 1})
        timespan("2022-12-12", 1, "days")
        tplot_options("title", "Parker Solar Probe E_flux")
        tplot("E_Flux", display=global_display, save_png=os.path.join(save_dir, "psp_E_Flux.png"))
        tplot_options("title", "")
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests

    def test_save_with_plot_objects(self):
        # Test that output files are saved when return_plot_objects is True

        themis.state(probe="a")
        local_png = os.path.join(save_dir, "ret_plot_objs.png")
        if os.path.exists(local_png):
            os.remove(local_png)
        tplot_options("title", "Should create ret_plot_objs.png ")
        tplot(
            "tha_pos",
            display=global_display,
            return_plot_objects=True,
            save_png=local_png,
        )
        self.assertTrue(os.path.exists(local_png))
        tplot_options("title", "")

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

        tplot(
            plot_vars,
            var_label=var_label,
            display=global_display,
            save_png=os.path.join(save_dir, "original_varlabel.png"),
        )
        timespan("2007-03-23", 1, "days")  # Reset to avoid interfering with other tests
        tplot_options("title", "")

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

    def test_tplot_trange(self):
        del_data("*")
        themis.fit(probe="e", trange=["2007-03-23", "2007-03-24"])
        tplot_options("title", "No timespan or xlim set, full time range of loaded data")
        tplot("the_fgs_dsl", display=global_display, save_png=os.path.join(save_dir, "notrange_default.png"))
        tplot_options("title", "No timespan or xlim set, using trange to plot 12:00 to 23:59")
        tplot(
            "the_fgs_dsl",
            trange=["2007-03-23/12:00", "2007-03-24/00:00"],
            display=global_display,
            save_png=os.path.join(save_dir, "trange_pm.png"),
        )
        tplot_options("title", "Using xlim to set time range from 00:00 to 12:00")
        xlim("2007-03-23/00:00:00", "2007-03-23/12:00:00")
        tplot("the_fgs_dsl", display=global_display, save_png=os.path.join(save_dir, "xlim_am.png"))
        tplot_options("title", "Xlim set to 00:00 to 12:00, overriding with trange from 10:00 to 12:00")
        tplot(
            "the_fgs_dsl",
            trange=["2007-03-23/10:00", "2007-03-23/12:00:00"],
            display=global_display,
            save_png=os.path.join(save_dir, "xlim_am_trange_override.png"),
        )
        tplot_options("title", "")


if __name__ == "__main__":
    unittest.main()
