# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from . import tplot_utilities
from .xlim import xlim

def timespan(t1, dt, keyword='days'):
    """
    This function will set the time range for all time series plots.  This is a wrapper for the function "xlim" to
    better handle time axes.  
    
    Parameters:
        t1 : flt/str
            The time to start all time series plots.  Can be given in seconds since epoch, or as a string
            in the format "YYYY-MM-DD HH:MM:SS"
        dt : flt
            The time duration of the plots.  Default is number of days.  
        keyword : str
            Sets the units of the "dt" variable.  Days, hours, minutes, and seconds are all accepted.  
            
    Returns:
        None
    
    Examples:
        >>> # Set the timespan to be 2017-07-17 00:00:00 plus 1 day
        >>> import pytplot
        >>> pytplot.timespan(1500249600, 1)
        
        >>> # The same as above, but using different inputs
        >>> pytplot.timespan("2017-07-17 00:00:00", 24, keyword='hours')

    """
    
    if keyword == 'days':
        dt *= 86400
    elif keyword == 'hours':
        dt *= 3600
    elif keyword == 'minutes':
        dt *= 60
    elif keyword == 'seconds':
        dt *= 1
    else:
        print("Invalid 'keyword' option.\nEnum(None, 'hours', 'minutes', 'seconds', 'days')")
        
    if not isinstance(t1, (int, float, complex)):
        t1 = tplot_utilities.str_to_int(t1)
    t2 = t1+dt
    xlim(t1, t2)
    
    return