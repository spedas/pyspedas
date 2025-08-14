# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pyspedas
import logging

def get_timespan(name=None):
    """
    This function extracts the time span from the Tplot Variables stored in memory.
    If called with no arguments, return the global timespan set by timespan(), or None if none has been set.
    
    Parameters
    ----------
        name : str 
            Name of the tplot variable
         
    Returns
    -------
    list of float
        time_begin : float
            The beginning of the time series
        time_end : float
            The end of the time series
            
    Examples
    --------
        >>> # Retrieve the time span from Variable 1
        >>> import pyspedas
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pyspedas.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> time1, time2 = pyspedas.get_timespan("Variable1")

    """

    if name is None:
        if 'x_range' in pyspedas.tplot_tools.tplot_opt_glob.keys():
            return pyspedas.tplot_tools.tplot_opt_glob['x_range']
        else:
            return None
    elif name not in pyspedas.tplot_tools.data_quants.keys():
        logging.info("The name %s is currently not in pyspedas",name)
        return None

    return pyspedas.tplot_tools.data_quants[name].attrs['plot_options']['trange'][0], pyspedas.tplot_tools.data_quants[name].attrs['plot_options']['trange'][1]