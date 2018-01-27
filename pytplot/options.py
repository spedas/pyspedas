# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from pytplot import data_quants
from .tplot_utilities import set_options
from astropy.wcs.docstrings import name

def options(name, option, value):
    
    """
    This function allows the user to set a large variety of options for individual plots.  
    
    Parameters:
        name : str 
            Name of the tplot variable
        option : str
            The name of the option.  See section below  
        value : str/int/float/list
            The value of the option.  See section below.  
            
    Options:
        ============  ==========   =====
        Options       Value type   Notes
        ============  ==========   =====
        Color         str/list     Red, Orange, Yellow, Green, Blue, etc
        Colormap      str/list     https://matplotlib.org/examples/color/colormaps_reference.html
        Spec          int          1 sets the Tplot Variable to spectrogram mode, 0 reverts
        Alt           int          1 sets the Tplot Variable to altitude plot mode, 0 reverts   
        Map           int          1 sets the Tplot Variable to latitude/longitude mode, 0 reverts
        ylog          int          1 sets the y axis to log scale, 0 reverts
        zlog          int          1 sets the z axis to log scale, 0 reverts (spectrograms only)
        legend_names  list         A list of strings that will be used to identify the lines
        line_style    str          solid_line, dot, dash, dash_dot, dash_dot_dot_dot, long_dash
        name          str          The title of the plot
        panel_size    flt          Number between (0,1], representing the percent size of the plot
        basemap       str          Full path and name of a background image for "Map" plots
        alpha         flt          Number between [0,1], gives the transparancy of the plot lines
        yrange        flt list     Two numbers that give the y axis range of the plot
        zrange        flt list     Two numbers that give the z axis range of the plot
        ytitle        str          Title shown on the y axis
        ztitle        str          Title shown on the z axis.  Spec plots only.  
        ============  ==========   =====
    
    Returns:
        None
    
    Examples:
        >>> # Change the y range of Variable1 
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> pytplot.options('Variable1', 'yrange', [2,4])
        
        >>> # Change Variable1 to use a log scale
        >>> pytplot.options('Variable1', 'ylog', 1)
        
        >>> # Change the line color of Variable1
        >>> pytplot.options('Variable1', 'ylog', 1)
    
    """
    if isinstance(name,int):
        name = list(data_quants.keys())[name-1]
    if not isinstance(name, list):
        name = [name]
    
    option = option.lower()
    for i in name:
        if i not in data_quants.keys():
            print(str(i) + " is currently not in pytplot.")
            return
        (new_yaxis_opt, new_zaxis_opt, new_line_opt, new_extras,full_data) = set_options(option, value, data_quants[i].yaxis_opt, data_quants[i].zaxis_opt, data_quants[i].line_opt, data_quants[i].extras,data_quants[i])

        data_quants[i].yaxis_opt = new_yaxis_opt
        data_quants[i].zaxis_opt = new_zaxis_opt
        data_quants[i].line_opt = new_line_opt
        data_quants[i].extras = new_extras
        
    
    return
        
    