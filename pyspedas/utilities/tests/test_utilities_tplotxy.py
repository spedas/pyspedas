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
global_display=True


class PlotTestCases(unittest.TestCase):
    """Test XY plot functions."""

    def test_themis_orbit_km(self):
        # Test a simple THEMIS orbit plot in the XY plane, plot units in re
        themis.state(trange=default_trange, probe=['a','b','c','d','e'])
        tplotxy('th?_pos_gse', title='THEMIS orbit plot', reverse_x=True, reverse_y=True, plot_units='re', display=global_display, save_png='orbits_thm_art_re.png')


    def test_themis_orbit_km_legends(self):
        # Test a simple THEMIS orbit plot in the XY plane, plot units in re
        themis.state(trange=default_trange, probe=['a','b','c','d','e'])
        tplotxy('th?_pos_gse', legend_names=['THEMIS-A','THEMIS-B','THEMIS-C', 'THEMIS-D', 'THEMIS-E'], reverse_x=True, reverse_y=True, plot_units='re', display=global_display, save_png='orbits_thm_art_re_legends.png')

    def test_themis_orbit_km_badlegends(self):
        # Test a simple THEMIS orbit plot in the XY plane, plot units in re
        themis.state(trange=default_trange, probe=['a','b','c','d','e'])
        tplotxy('th?_pos_gse', legend_names=['THEMIS-A','THEMIS-B'], reverse_x=True, reverse_y=True, plot_units='re', display=global_display, save_png='orbits_thm_art_re_badlegends.png')

    def test_themis_orbit_km_xz(self):
        # Test a simple THEMIS orbit plot in the XY plane, plot units in re
        themis.state(trange=default_trange, probe=['a','b','c','d','e'])
        tplotxy('th?_pos_gse', reverse_x=True, reverse_y=False, plane='xz', plot_units='re', display=global_display, save_png='orbits_thm_art_xz_re.png')

    def test_themis_orbit_km_yz(self):
        # Test a simple THEMIS orbit plot in the XY plane, plot units in re
        themis.state(trange=default_trange, probe=['a','b','c','d','e'])
        tplotxy('th?_pos_gse', reverse_x=False, reverse_y=False, plane='yz', plot_units='re', display=global_display, save_png='orbits_thm_art_yz_re.png')

    def test_themis_orbit_re(self):
        # Test a simple THEMIS orbit plot in the XY plane,plot units in km
        themis.state(trange=default_trange, probe=['a','b','c','d','e'])
        tplotxy('th?_pos_gse', reverse_x=True, reverse_y=True, plot_units='km', display=global_display, save_png='orbits_thm_art_km.png')

    def test_themis_orbit_inner_mixedunits_km(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units km, mixed input units
        themis.state(trange=default_trange, probe=['a','d', 'e'])
        tkm2re('the_pos_gse', km=False)
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse_re'], reverse_x=True, reverse_y=True, plot_units='km', display=global_display, save_png='orbits_thm_mixed_km.png')

    def test_themis_orbit_inner_mixedunits_re(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        themis.state(trange=default_trange, probe=['a','d', 'e'])
        tkm2re('the_pos_gse', km=False)
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse_re'], reverse_x=True, reverse_y=True, plot_units='re', display=global_display, save_png='orbits_thm_mixed_re.png')

    def test_themis_orbit_inner_linestyles(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        themis.state(trange=default_trange, probe=['a','d', 'e'])
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'], legend_names=['THEMIS-A','THEMIS-B','THEMIS-C', 'THEMIS-D', 'THEMIS-E'], reverse_x=True, reverse_y=True, plot_units='re', linestyles=['solid','dotted','dashdot'], display=global_display, save_png='orbits_thm_linestyles.png')

    def test_themis_orbit_inner_markers(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        themis.state(trange=default_trange, probe=['a','d', 'e'])
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'], legend_names=['THEMIS-A','THEMIS-B','THEMIS-D', 'THEMIS-E'], reverse_x=True, reverse_y=True, plot_units='re', markers=['x','.','+'], markevery=60, display=global_display, save_png='orbits_thm_markers.png')

    def test_themis_orbit_inner_startendmarkers(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        themis.state(trange=default_trange, probe=['a','d', 'e'])
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'], reverse_x=True, reverse_y=True, plot_units='re', startmarkers=['x','.','+'], endmarkers=['x','.','+'], markers=None, display=global_display, save_png='orbits_thm_startendmarkers.png')

    def test_themis_orbit_inner_startmarkers(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        themis.state(trange=default_trange, probe=['a','d', 'e'])
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'], reverse_x=True, reverse_y=True, plot_units='re', startmarkers=['x','.','+'], markers=None, display=global_display, save_png='orbits_thm_startmarkers.png')

    def test_themis_orbit_inner_linewidths(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        themis.state(trange=default_trange, probe=['a','d', 'e'])
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'], reverse_x=True, reverse_y=True, plot_units='re', linewidths=[1,2,3], display=global_display, save_png='orbits_thm_linewidths.png')

    def test_themis_orbit_inner_showearth_xy(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        themis.state(trange=default_trange, probe=['a','d', 'e'])
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'], reverse_x=True, reverse_y=True, plot_units='re', show_centerbody=True, display=global_display, save_png='orbits_thm_showearth_xy.png')

    def test_themis_orbit_inner_showearth_xz(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        themis.state(trange=default_trange, probe=['a','d', 'e'])
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'], plane='xz', reverse_x=True, reverse_y=False, plot_units='re', show_centerbody=True, display=global_display, save_png='orbits_thm_showearth_xz.png')


    def test_themis_orbit_inner_showearth_yz(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        themis.state(trange=default_trange, probe=['a','d', 'e'])
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'], plane='yz', reverse_x=True, reverse_y=False, plot_units='re', show_centerbody=True, display=global_display, save_png='orbits_thm_showearth_yz.png')

    def test_themis_orbit_inner_showearth_yz_nocenter(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        themis.state(trange=default_trange, probe=['a','d', 'e'])
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'], plane='yz', center_origin = False, reverse_x=True, reverse_y=False, plot_units='re', show_centerbody=True, display=global_display, save_png='orbits_thm_showearth_yz_nocenter.png')

if __name__ == "__main__":
    unittest.main()
