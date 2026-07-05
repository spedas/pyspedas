"""Test plotting functions (mostly for pseudovariables)"""

import os
import unittest
import datetime as dt
from pyspedas.tplot_tools.MPLPlotter.tplot_map import tplot_map, add_markers, tplot_trace_tvars_to_tmap, add_station_fovs
import matplotlib.pyplot as plt

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
import pyspedas

# Whether to display plots during testing
#global_display = TESTING_CONFIG["global_display"]
global_display = False
# Directory to save testing output files
output_dir = TESTING_CONFIG["local_testing_dir"]
# Ensure output directory exists
save_dir = os.path.join(output_dir, "utilities")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

default_trange = ["2007-03-23", "2007-03-24"]


class PlotTestCases(unittest.TestCase):
    """Test plot functions."""

    def test_basic_map(self):
        # Initialize map:
        tmap = tplot_map(projection="merc", resolution='i', llcrnrlon=-170,llcrnrlat=35.,urcrnrlon=-45,urcrnrlat=75)
        # tmap._params.drawmapboundary = {"fill_color":"lightskyblue"}
        # tmap._params.fillcontinents = {"color":"palegreen","lake_color":"lightskyblue"}
        tmap.add_map_boundary()
        tmap.add_fillcontinents()
        tmap.add_coastlines(linewidth=0.25)
        plt.savefig('tplot_map_basic.png', dpi=300)
        if global_display:
            tmap.show()

    def test_full_map(self):
        from pyspedas.projects.themis import state
        from pyspedas.projects.themis.ground import gmag

        date_str = '2026-02-03'
        state(trange=[date_str, date_str], probe='a')
        state(trange=[date_str, date_str], probe='d')

        # Initialize map:
        tmap = tplot_map(lat_0=50, lon_0=-100,)
        # tmap._params.drawmapboundary = {"fill_color":"lightskyblue"}
        # tmap._params.fillcontinents = {"color":"palegreen","lake_color":"lightskyblue"}

        # Add ground tracks:
        tmap = tplot_trace_tvars_to_tmap(tmap=tmap, tvar=['tha_pos_gsm', 'thd_pos_gsm'])

        # Add ground station markers
        # tplot_map_add_markers(map_obj, marker_latitude_list, marker_longitude_list, marker_symbol, marker_color)
        themis_gmag_dict = gmag.Themis_gmag()
        for station_dict in themis_gmag_dict.get_gmag_list():
            if station_dict['variom'] == 'Y':
                tmap = add_markers(coords=np.array([0, float(station_dict['lat']), float(station_dict['lng'])]),
                                   tmap=tmap, label=station_dict['ccode'], ms=3)

        # Add field of view circles for each ground station
        tmap = add_station_fovs(coords=[np.array([0, 48, -128]), np.array([0, 30, -110])], tmap=tmap)

        tmap.add_map_boundary()
        tmap.add_fillcontinents()
        tmap.add_coastlines(linewidth=0.25)
        tmap.add_nightshade(date=dt.datetime.strptime(date_str + " 15:00:00", '%Y-%m-%d %H:%M:%S'))

        plt.savefig('tplot_map_full.png',dpi=300)
        if global_display:
            tmap.show()
        print("done")


if __name__ == "__main__":
    unittest.main()
