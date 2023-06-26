# Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np
import pandas as pd
import copy
import datetime
from collections import namedtuple

def makegap(var_data, dt = None, margin = 0.0, func='nan'):
    '''
    Fills gaps in the data either with NaNs or the last number.
    This is identical to degap, except operates directly on the data and 
    time arrays, rather than the tplot variable. This is intended for use 
    with the data_gap option

    Parameters:
        var_data : number, the data for the tplot variable, contains at least, tags for 'y' and 'times'
        dt : int/float
            Step size of the data in seconds, default is to use the median time interval
        margin : int/float, optional, default is 0.0 seconds (there is no margin in the IDL tplot makegap)
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
    vt = var_data.times
    gap_size = np.diff(vt) #vt is in nanoseconds, and np.diff works over day boundaries
    #Default for dt is the median value of gap_size, the time interval differences
    if dt == None:
        dt = np.median(gap_size)
        dt0 = dt
    else:
        #change dt to appropriate type
        dt0 = np.timedelta64(int(dt*1e9), 'ns')

    gap_index_locations = np.where(gap_size > dt0)

    icount = 0
    for i in gap_index_locations[0]:
        if icount == 0:
            values_to_add = np.arange(vt[i], vt[i+1], dt0)
        else:
            values_to_add = np.append(values_to_add, np.arange(vt[i], vt[i+1], dt0))

        icount = icount+1
        
    new_vt = np.sort(np.unique(np.concatenate((values_to_add, vt))))

    if func == 'nan':
        method = None
    if func == 'ffill':
        method = 'ffill'

    # Use pandas.reindex, but you cannot reindex the var_data variable directly, so recreate it
    if var_data.y.ndim == 1:
        var_data_out = namedtuple('var_data_out', ['times', 'y']) #similar to get_data.py
        a = pd.Series(var_data.y, index = vt)
        a = a.reindex(new_vt, method=method)
        return var_data_out(new_vt, a.values)
    else: #multiple dimensions
        a = pd.DataFrame(var_data.y, index = vt)
        a = a.reindex(new_vt, method=method)
        #Check for values, v, or v1, v2, v3
        if len(var_data) == 2: #No v's
            var_data_out = namedtuple('var_data_out', ['times', 'y'])
            return var_data_out(new_vt, a.values)
        elif len(var_data) == 3: #v or v1,needs indexing if it's 2d
            var_data_out = namedtuple('var_data_out', ['times', 'y', 'v'])
            if var_data[2].ndim > 1:
                b = pd.DataFrame(var_data[2], index = vt)
                b = b.reindex(new_vt, method=method)
                return var_data_out(new_vt, a.values, b.values)
            else: #1-d v
                return var_data_out(new_vt, a.values, var_data[2])
        elif len(var_data) == 4: #has both v1 and v2
            var_data_out = namedtuple('var_data_out', ['times', 'y', 'v1', 'v2'])
            if var_data[2].ndim > 1:
                b = pd.DataFrame(var_data[2], index = vt)
                b = b.reindex(new_vt, method=method)
                bv = b.values
            else:
                bv = var_data[2]
            if var_data[3].ndim > 1:
                c = pd.DataFrame(var_data[3], index = vt)
                c = c.reindex(new_vt, method=method)
                cv = c.values
            else:
                cv = var_data[3]
            return var_data_out(new_vt, a.values, bv, cv)
        elif len(var_data) == 5: #has both v1 and v2
            var_data_out = namedtuple('var_data_out', ['times', 'y', 'v1', 'v2', 'v3'])
            if var_data[2].ndim > 1:
                b = pd.DataFrame(var_data[2], index = vt)
                b = b.reindex(new_vt, method=method)
                bv = b.values
            else:
                bv = var_data[2]
            if var_data[3].ndim > 1:
                c = pd.DataFrame(var_data[3], index = vt)
                c = c.reindex(new_vt, method=method)
                cv = c.values
            else:
                cv = var_data[3]
            if var_data[4].ndim > 1:
                d = pd.DataFrame(var_data[4], index = vt)
                d = d.reindex(new_vt, method=method)
                dv = d.values
            else:
                dv = var_data[4]
            return var_data_out(new_vt, a.values, bv, cv, dv)

#End of makegap.py
