  # Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np
import pandas as pd
import copy
import datetime

def degap(tvar,dt = None, margin = 0.25, func='nan', new_tvar = None):
    '''
    Fills gaps in the data either with NaNs or the last number.

    Parameters:
        tvar : str
            Name of tplot variable to modify
        dt : int/float
            Step size of the data in seconds, default is to use the median time interval
        margin : int/float, optional, default is 0.25 seconds
            The maximum deviation from the step size allowed before degapping occurs.  In other words, if you'd like to fill in data every 4 seconds
            but occasionally the data is 4.1 seconds apart, set the margin to .1 so that a data point is not inserted there.
        func : str, optional
            Either 'nan' or 'ffill', which overrides normal interpolation with NaN
            substitution or forward-filled values.
        new_tvar : str, optional
            The new tplot variable name to store the data into.  If None, then the data is overwritten.

    Returns:
        None

    Examples:
        >>> # TODO
    '''

    #fix from T.Hori, 2023-04-10, jimm02
    #    gap_size = np.diff(pytplot.data_quants[tvar].coords['time']) This is in Nanoseconds, and causes a type mismatch with dt+margin
    #    new_tvar_index = pytplot.data_quants[tvar].coords['time']
    new_tvar_index = pytplot.get_data(tvar)[0] #Unix time float64
    gap_size = np.diff(new_tvar_index)

    #Default for dt is the median value of gap_size, the time interval differences
    if dt == None:
        dt = np.median(gap_size)

    gap_index_locations = np.where(gap_size > dt+margin)
    values_to_add = np.array([])
    for i in gap_index_locations[0]:
        values_to_add = np.append(values_to_add, np.arange(new_tvar_index[i], new_tvar_index[i+1], dt))

    #new_index = np.sort(np.unique(np.concatenate((values_to_add, new_tvar_index))))
    new_index_float64 = np.sort(np.unique(np.concatenate((values_to_add, new_tvar_index))))
    new_index = np.array([datetime.datetime.utcfromtimestamp(t) if np.isfinite(t) else
                          datetime.datetime.utcfromtimestamp(0) for t in new_index_float64])
 
    if func == 'nan':
        method = None
    if func == 'ffill':
        method = 'ffill'

    a = pytplot.data_quants[tvar].reindex({'time': new_index}, method=method)

    if new_tvar is None:
        a.name = tvar
        a.attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)
        pytplot.data_quants[tvar] = copy.deepcopy(a)
    else:
        if 'spec_bins' in a.coords:
            pytplot.store_data(new_tvar, data={'x': a.coords['time'], 'y': a.values, 'v': a.coords['spec_bins']})
            pytplot.data_quants[new_tvar].attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)
        else:
            pytplot.store_data(new_tvar, data={'x': a.coords['time'], 'y': a.values})
            pytplot.data_quants[new_tvar].attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)

    return
