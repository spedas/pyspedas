# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from collections import OrderedDict

import os
import sys
import xarray as xr

# xarray options
xr.set_options(keep_attrs=True)


# Global Variables
data_quants = OrderedDict()
tplot_opt_glob = dict(
    tools="xpan,crosshair,reset",
    min_border_top=12,
    min_border_bottom=12,
    title_align="center",
    window_size=[800, 800],
    title_size="12",
    title_text="",
    crosshair=True,
    data_gap=0,
    black_background=False,
    axis_font_size=12,
    axis_tick_num=[
        (0, 1000000000),
        (3, 1),
    ],
    y_axis_zoom=False,
)
lim_info = {}
extra_layouts = {}

from .get_y_range import get_y_range
from .tplot_rename import tplot_rename
from .del_data import del_data
from .replace_metadata import replace_metadata
from .store_data import store_data, store
from .get_data import get_data, get
from .str_to_float_fuzzy import str_to_float_fuzzy
from .tplot_names import tplot_names
from .wildcard_routines import (
    wildcard_expand,
    tplot_wildcard_expand,
    tname_byindex,
    tindex_byname,
)
from .options import options
from .xlim import xlim
from .ylim import ylim
from .zlim import zlim
from .tlimit import tlimit
from . import spedas_colorbar
from .exporters.tplot_save import tplot_save
from .tnames import tnames
from .convert_tplotxarray_to_pandas_dataframe import (
    convert_tplotxarray_to_pandas_dataframe,
)
from .importers.tplot_restore import tplot_restore
from .is_pseudovariable import is_pseudovariable
from .count_traces import count_traces
from .get_timespan import get_timespan
from .tplot_options import tplot_options
from .tplot_copy import tplot_copy
from .replace_data import replace_data
from .replace_metadata import replace_metadata
from .get_ylimits import get_ylimits
from .rgb_color import rgb_color
from .timebar import timebar
from .databar import databar
from .timespan import timespan
from .timestamp import timestamp
from .time_double import time_float, time_double, time_float_one
from .time_string import time_string, time_datetime, time_string_one
from .importers.sts_to_tplot import sts_to_tplot
from .data_att_getters_setters import set_coords, get_coords, set_units, get_units
from .data_exists import data_exists
from .link import link
from .tres import tres

from .tplot_math.tinterp import tinterp
from .tplot_math.add_across import add_across
from .tplot_math.add import add
from .tplot_math.avg_res_data import avg_res_data
from .tplot_math.clip import clip
from .tplot_math.crop import crop
from .tplot_math.deflag import deflag
from .tplot_math.degap import degap
from .tplot_math.derive import derive
from .tplot_math.divide import divide
from .tplot_math.interp_nan import interp_nan
from .tplot_math.tinterp import tinterp
from .tplot_math.join_vec import join_vec
from .tplot_math.multiply import multiply
from .tplot_math.spec_mult import spec_mult
from .tplot_math.split_vec import split_vec
from .tplot_math.subtract import subtract
from .tplot_math.pwr_spec import pwr_spec
from .tplot_math.tsmooth import smooth
from .tplot_math.tsmooth import tsmooth
from .tplot_math.tdotp import tdotp
from .tplot_math.tcrossp import tcrossp
from .tplot_math.tnormalize import tnormalize
from .tplot_math.subtract_average import subtract_average
from .tplot_math.subtract_median import subtract_median
from .tplot_math.clean_spikes import clean_spikes
from .tplot_math.time_clip import time_clip
from .tplot_math.tkm2re import tkm2re
from .tplot_math.makegap import makegap
from .tplot_math.tdeflag import tdeflag
from .tplot_math.pwrspc import pwrspc
from .tplot_math.tpwrspc import tpwrspc
from .tplot_math.dpwrspc import dpwrspc
from .tplot_math.tdpwrspc import tdpwrspc

from .reduce_spec_dataset import reduce_spec_dataset
from .MPLPlotter.lineplot import lineplot
from .MPLPlotter.specplot import specplot, specplot_make_1d_ybins
from .MPLPlotter.get_var_label_ticks import get_var_label_ticks
from .MPLPlotter.var_labels import var_label_panel
from .MPLPlotter.ctime import ctime
from .MPLPlotter.highlight import highlight
from .MPLPlotter.annotate import annotate
from .MPLPlotter.tplot import tplot
from .importers.cdf_to_tplot import cdf_to_tplot
from .importers.netcdf_to_tplot import netcdf_to_tplot
from .exporters.tplot_ascii import tplot_ascii
