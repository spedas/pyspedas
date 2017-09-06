# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from . import tplot_common
from .timestamp import TimeStamp
from . import tplot_utilities
from bokeh.models import Span

#HELLO IGNORE THIS

def timebar(t, varname = None, databar = False, delete = False, color = 'black', thick = 1, dash = False):    
    """
    This function will add a vertical bar to all time series plots.  This is useful if you
    want to bring attention to a specific time.  
    
    Parameters:
        t : flt/list
            The time in seconds since Jan 01 1970 to place the vertical bar.  If a list of numbers are supplied,
            multiple bars will be created.  If "databar" is set, then "t" becomes the point on the y axis to 
            place a horizontal bar.  
        varname : str/list, optional
            The variable(s) to add the vertical bar to.  If not set, the default is to add it to all current plots.  
        databar : bool, optional
            This will turn the timebar into a horizontal data bar.  If this is set True, then variable "t" becomes 
            the point on the y axis to place a horizontal bar.  
        delete : bool, optional
            If set to True, at lease one varname must be supplied.  The timebar at point "t" for variable "varname"
            will be removed.  
        color : str
            The color of the bar
        thick : int
            The thickness of the bar
        dash : bool
            If set to True, the bar is dashed rather than solid
            
    Returns:
        None
    
    Examples:
        >>> # Place a green time bar at 2017-07-17 00:00:00
        >>> import pytplot
        >>> pytplot.timebar(1500249600, color='grean)
        
        >>> # Place a dashed data bar at 5500 on the y axis
        >>> pytplot.timebar(5500, dashed=True, databar=True)

    """
    
    
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
                temp_data_quants.time_bar.append(tbar)
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
                    temp_data_quants.time_bar.append(tbar)
    return