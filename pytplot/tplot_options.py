# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from . import tplot_common
from . import tplot_utilities

def tplot_options(option, value):
    """
    This function allows the user to set several global options for the generated plots.  
    
    Parameters:
        option : str
            The name of the option.  See section below  
        value : str/int/float/list
            The value of the option.  See section below.  
            
    Options:
        ============  ==========   =====
        Options       Value type   Notes
        ============  ==========   =====
        title         str          Title of the the entire output
        title_size    int          Font size of the output 
        wsize         [int, int]   [height, width], pixel size of the plot window
        title_align   int          Offset position in pixels of the title   
        var_label     srt          Name of the tplot variable to be used as another x axis
        alt_range     [flt, flt]   The min and max altitude to be plotted on all alt plots 
        ============  ==========   =====
    
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
    
    tplot_common.tplot_opt_glob = tplot_utilities.set_tplot_options(option, value, tplot_common.tplot_opt_glob)
    
    return
