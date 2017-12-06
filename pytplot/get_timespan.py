# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from pytplot import data_quants
from . import tplot_utilities


def get_timespan(name):
    """
    This function will get extract the time span from the Tplot Variables stored in memory.  
    
    Parameters:
        name : str 
            Name of the tplot variable
         
    Returns:
        time_begin : float
            The beginning of the time series
        time_end : float
            The end of the time series
            
    Examples:
        >>> # Retrieve the time span from Variable 1
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> time1, time2 = pytplot.get_timespan("Variable1")

    """
    
    if name not in data_quants.keys():
        print("That name is currently not in pytplot") 
        return
    print("Start Time: " + tplot_utilities.int_to_str(data_quants[name].trange[0]))
    print("End Time:   " + tplot_utilities.int_to_str(data_quants[name].trange[1]))
    
    return(data_quants[name].trange[0], data_quants[name].trange[1])