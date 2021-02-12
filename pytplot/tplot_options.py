# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pytplot
from . import tplot_utilities

def tplot_options(option, value):
    """
    This function allows the user to set GLOBAL options for the generated plots.
    
    Parameters:
        option : str
            The name of the option.  See section below  
        value : str/int/float/list
            The value of the option.  See section below.  
            
    Options:
        ================  ==========   =====
        Options           Value type   Notes
        ================  ==========   =====
        title             str          Title of the the entire output
        title_size        int          Font size of the output
        wsize             [int, int]   [height, width], pixel size of the plot window
        title_align       int          Offset position in pixels of the title
        var_label         srt          Name of the tplot variable to be used as another x axis
        alt_range         [flt, flt]   The min and max altitude to be plotted on all alt plots
        map_x_range       [int, int]   The min and max longitude to be plotted on all map plots
        map_y_range       [int, int]   The min and max latitude to be plotted on all map plots
        x_range           [flt, flt]   The min and max x_range (usually time) to be plotted on all Spec/1D plots
        data_gap          int          Number of seconds with consecutive nan values allowed before no interp should occur
        roi               [str, str]   Times between which there's a region of interest for a user
        crosshair         bool         Option allowing crosshairs and crosshair legend
        vertical_spacing  int          The space in pixels between two plots
        show_all_axes     bool         Whether or not to just use one axis at the bottom of the plot
        black_background  bool         Whether or not to make plot backgrounds black w/ white text
        axis_font_size    int          The font size of the axis ticks.  Default is 10.
        axis_tick_num     [tuples]     A list of tuples that determines how many ticks appear.  See pyqtgraph textFillLimits
        yaxis_width       int          The number of pixels wide of the y axis
        y_axis_zoom       bool         Set True if the mouse wheel should zoom in on the y axis as well as the x on plots.
        ================  ==========   =====
    
    Returns:
        None
    
    Examples:
        >>> # Set the plot title
        >>> import pytplot
        >>> pytplot.tplot_options('title', 'SWEA Data for Orbit 1563')
        
        >>> # Set the window size 
        >>> pytplot.tplot_options('wsize', [1000,500])
        
    
    """
    
    option = option.lower()
    
    temp = tplot_utilities.set_tplot_options(option, value, pytplot.tplot_opt_glob)
    pytplot.tplot_opt_glob = temp
    
    return
