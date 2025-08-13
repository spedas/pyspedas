# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from _collections import OrderedDict

import os
import sys
import xarray as xr

# xarray options
xr.set_options(keep_attrs=True)


# Global Variables
data_quants = OrderedDict()
interactive_window = None  # 2D interactive window that appears whenever plotting spectrograms w/ tplot.
# If option 't_average' is set by user, then x and y values on this plot are the average of the user-specified
# number of seconds for which the cursor location should be averaged.
static_window = None  # 2D window showing data at certain point in time from a spectrogram plot.
static_tavg_window = None  # 2D window showing averaged y and z data for a specified time range from a spectrogram plot.
tplot_opt_glob = dict(tools="xpan,crosshair,reset",
                      min_border_top=12, min_border_bottom=12,
                      title_align='center', window_size=[800, 800],
                      title_size='12', title_text='', crosshair=True,
                      data_gap=0, black_background=False, axis_font_size=12, axis_tick_num=[(0, 1000000000), (3, 1),],
                      y_axis_zoom=False)
lim_info = {}
extra_layouts = {}

from .store_data import store_data, store
from .tplot import tplot
from .get_data import get_data, get
from .xlim import xlim
from .ylim import ylim
from .zlim import zlim
from .tlimit import tlimit
from pyspedas.pytplot.exporters.tplot_save import tplot_save
from .wildcard_routines import wildcard_expand, tplot_wildcard_expand, tname_byindex, tindex_byname
from .tplot_names import tplot_names
from .tnames import tnames
from pyspedas.pytplot.importers.tplot_restore import tplot_restore
from .is_pseudovariable import is_pseudovariable
from .count_traces import count_traces
from .get_timespan import get_timespan
from .tplot_options import tplot_options
from .tplot_rename import tplot_rename
from .tplot_copy import tplot_copy
from .replace_data import replace_data
from .replace_metadata import replace_metadata
from .get_ylimits import get_ylimits
from .timebar import timebar
from .databar import databar
from .del_data import del_data
from .timespan import timespan
from .options import options
from .timestamp import timestamp
from .time_double import time_float,time_double, time_float_one
from .time_string import time_string, time_datetime, time_string_one
from pyspedas.pytplot.importers.cdf_to_tplot import cdf_to_tplot
from pyspedas.pytplot.importers.netcdf_to_tplot import netcdf_to_tplot
from pyspedas.pytplot.importers.sts_to_tplot import sts_to_tplot
from .data_att_getters_setters import set_coords, get_coords, set_units, get_units
from .data_exists import data_exists
from .link import link
from .tres import tres
from .format_sandbox import format_sandbox
from .tplot_math import *
from .wildcard_routines import wildcard_expand, tplot_wildcard_expand, tname_byindex, tindex_byname
from .MPLPlotter.var_labels import var_label_panel
from .MPLPlotter.ctime import ctime
from .MPLPlotter.highlight import highlight
from .MPLPlotter.annotate import annotate
