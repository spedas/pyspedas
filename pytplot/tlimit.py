from __future__ import division
import os
import datetime
from bokeh.io import output_file, show, gridplot
import pickle
import math
import pandas as pd
import numpy as np
import pytz
from bokeh.plotting import output_server
from bokeh.models import CustomJS, ColumnDataSource, Label, LogColorMapper, LogTicker, ColorBar, LinearColorMapper, BasicTicker, Legend
from bokeh.plotting.figure import Figure
from bokeh.models import (ColumnDataSource, CustomJS, DatetimeAxis,
                          HoverTool, LinearAxis, LogAxis, PanTool, Plot, Range1d, 
                          SaveTool, Span, Title, WheelZoomTool)
from bokeh.models.formatters import DatetimeTickFormatter, FuncTickFormatter,\
    NumeralTickFormatter
from bokeh.models.glyphs import Line
from bokeh.models.tools import RedoTool, UndoTool, CrosshairTool, LassoSelectTool, BoxZoomTool, ResetTool
from bokeh.driving import cosine
from bokeh.layouts import gridplot, widgetbox, layout
from openpyxl.worksheet import datavalidation
from _collections import OrderedDict
from bokeh.models.widgets.inputs import TextInput

from . import tplot_common
from .timestamp import TimeStamp
from . import tplot_utilities

from .xlim import xlim

def tlimit(arg):
    global lim_info
    
    if arg is 'last':
        xlast = tplot_common.lim_info['xlast']
        tplot_common.lim_info['xlast'] = tplot_common.tplot_opt_glob['x_range']
        tplot_common.tplot_opt_glob['x_range'] = xlast
    elif arg is 'full':
        tplot_common.tplot_opt_glob['x_range'] = tplot_common.lim_info['xfull']
    elif isinstance(arg, list):
        min = arg[0]
        max = arg[1]
        xlim(min, max)
        
    return