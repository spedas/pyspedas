from . import tplot_common
from .timestamp import TimeStamp
from . import tplot_utilities


def timebar(t, varname = None, databar = False, delete = False, color = 'black', thick = 1, dash = False):    
    if not isinstance(t, (int, float, complex)):
        t = tplot_utilities.str_to_int(t)
    
    dim = 'height'
    if databar is True:
        dim = 'width'
    
    dash_pattern = 'solid'
    if dash is True:
        dash_pattern = 'dashed'
        
    # Convert single value to a list so we don't have to write code to deal with
    # both single values and lists.
    if not isinstance(t, list):
        t = [t]
    # Convert values to seconds by multiplying by 1000
    if databar is False:
        num_bars = len(t)
        for j in range(num_bars):
            t[j] *= 1000
            
    if delete is True:
        tplot_utilities.timebar_delete(t, varname, dim)
        return
    # If no varname specified, add timebars to every plot
    if varname is None:
        num_bars = len(t)
        for i in range(num_bars):
            tbar = {}
            tbar['location'] = t[i]
            tbar['dimension'] = dim
            tbar['line_color'] = color
            tbar['line_width'] = thick
            tbar['line_dash'] = dash_pattern
            for name in tplot_common.data_quants:
                temp_data_quants = tplot_common.data_quants[name]
                temp_data_quants['time_bar'].append(tbar)
    else:
        if not isinstance(varname, list):
            varname = [varname]
        for j in varname:
            if j not in tplot_common.data_quants.keys():
                print(str(j) + "is currently not in pytplot")
            else:
                num_bars = len(t)
                for i in range(num_bars):
                    tbar = Span(location = t[i], dimension = dim, line_color = color, line_width = thick, line_dash = dash_pattern)
                    temp_data_quants = tplot_common.data_quants[j]
                    temp_data_quants['time_bar'].append(tbar)
    return