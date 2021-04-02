# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from . import tplot_utilities
from bokeh.models import Span
import pytplot

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
        >>> pytplot.timebar(1500249600, color='green')
        
        >>> # Place a dashed data bar at 5500 on the y axis
        >>> pytplot.timebar(5500, dashed=True, databar=True)
        
        >>> Place 3 magenta time bars of thickness 5 
            at [2015-12-26 05:20:01, 2015-12-26 08:06:40, 2015-12-26 08:53:19]
            for variable 'sgx' plot
        >>> pytplot.timebar([1451107201,1451117200,1451119999],'sgx',color='m',thick=5)

    """
    
    # make sure t entered is a list
    if not isinstance(t, list):
        t = [t]
    
    # if entries in list not numerical, run str_to_int
    if not isinstance(t[0], (int, float, complex)):
        t1 = []
        for time in t:
            t1.append(tplot_utilities.str_to_int(time))
        t = t1
        
    dim = 'height'
    if databar is True:
        dim = 'width'
    
    dash_pattern = 'solid'
    if dash is True:
        dash_pattern = 'dashed'
        
            
    if delete is True:
        tplot_utilities.timebar_delete(t, varname, dim)
        return
    
    #if no varname specified, add timebars to every plot
    if varname is None:
        num_bars = len(t)
        for i in range(num_bars):
            tbar = {}
            tbar['location'] = t[i]
            tbar['dimension'] = dim
            tbar['line_color'] = pytplot.tplot_utilities.rgb_color(color)[0]
            tbar['line_width'] = thick
            tbar['line_dash'] = dash_pattern
            for name in pytplot.data_quants:
                temp_data_quants = pytplot.data_quants[name]
                if isinstance(temp_data_quants, dict):
                    # non-record varying variable
                    continue 
                temp_data_quants.attrs['plot_options']['time_bar'].append(tbar)
    #if varname specified
    else:
        if not isinstance(varname, list):
            varname = [varname]
        for j in varname:
            if j not in pytplot.data_quants.keys():
                print(str(j) + "is currently not in pytplot")
            else:
                num_bars = len(t)
                for i in range(num_bars):
                    tbar = {}
                    tbar['location'] = t[i]
                    tbar['dimension'] = dim
                    tbar['line_color'] = pytplot.tplot_utilities.rgb_color(color)[0]
                    tbar['line_width'] = thick
                    tbar['line_dash'] = dash_pattern
                    temp_data_quants = pytplot.data_quants[j]
                    if isinstance(temp_data_quants, dict):
                        # non-record varying variable
                        continue 
                    temp_data_quants.attrs['plot_options']['time_bar'].append(tbar)
    return