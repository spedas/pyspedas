from . import tplot_common
from . import tplot_utilities
from bokeh.models import Range1d

def xlim(min, max):
    if not isinstance(min, (int, float, complex)):
        min = tplot_utilities.str_to_int(min)
    if not isinstance(max, (int, float, complex)):
        max = tplot_utilities.str_to_int(max)
    if 'x_range' in tplot_common.tplot_opt_glob:
        tplot_common.lim_info['xlast'] = tplot_common.tplot_opt_glob['x_range']
    else:
        tplot_common.lim_info['xfull'] = Range1d(min, max)
        tplot_common.lim_info['xlast'] = Range1d(min, max)
    tplot_common.tplot_opt_glob['x_range'] = Range1d(min, max)
    tplot_common.time_range_adjusted = False
    return