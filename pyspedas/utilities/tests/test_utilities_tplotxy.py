"""Test plotting functions (mostly for pseudovariables)"""

import os
import unittest
import numpy as np
from pyspedas.projects import themis
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
    tplotxy,
    tkm2re,
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

default_trange = ["2020-01-01", "2020-01-02"]
global_display=False


class PlotTestCases(unittest.TestCase):
    """Test plot functions."""

    def test_themis_orbit1(self):
        # Test a simple THEMIS orbit plot in the XY plane, plot units in re
        themis.state(trange=default_trange, probe=['a','b','c','d','e'])
        tplotxy('th?_pos_gse', reverse_x=True, reverse_y=True, plot_units='re', display=global_display, save_png='orbits_thm_art_re.png')

    def test_themis_orbit2(self):
        # Test a simple THEMIS orbit plot in the XY plane,plot units in km
        themis.state(trange=default_trange, probe=['a','b','c','d','e'])
        tplotxy('th?_pos_gse', reverse_x=True, reverse_y=True, plot_units='km', display=global_display, save_png='orbits_thm_art_km.png')

    def test_themis_orbit3(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units km, mixed input units
        themis.state(trange=default_trange, probe=['a','d', 'e'])
        tkm2re('the_pos_gse', km=False)
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse_re'], reverse_x=True, reverse_y=True, plot_units='km', display=global_display, save_png='orbits_thm_mixed_km.png')

    def test_themis_orbit4(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        themis.state(trange=default_trange, probe=['a','d', 'e'])
        tkm2re('the_pos_gse', km=False)
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse_re'], reverse_x=True, reverse_y=True, plot_units='re', display=global_display, save_png='orbits_thm_mixed_re.png')

if __name__ == "__main__":
    unittest.main()
