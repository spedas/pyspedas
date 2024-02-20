# Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np

def makegap(var_data, dt = None, margin = 0.0, func='nan'):
    '''
    Fills gaps in the data either with NaNs or the last number.  This
    is identical to degap, except operates directly on the data and
    time arrays, rather than the tplot variable. This is intended for
    use with the data_gap option. This version actually puts the data
    into a temporary tplot variable, and call degap, then extracts
    that data into the proper form.

    Parameters:
        var_data : number, the data for the tplot variable, contains at least, tags for 'y' and 'times'
        dt : int/float
            Step size of the data in seconds, default is to use the median time interval
        margin : int/float, optional, default is 0.0 seconds (there is no margin in the IDL tplot makegap)
            The maximum deviation from the step size allowed before degapping occurs.  In other words, 
            if you'd like to fill in data every 4 seconds but occasionally the data is 4.1 seconds apart, 
            set the margin to .1 so that a data point is not inserted there.
        func : str, optional
            Either 'nan' or 'ffill', which overrides normal interpolation with NaN
            substitution or forward-filled values.

    Returns:
        None

    Examples:
        >>> # TODO

    '''
    #vt = var_data.times
    #gap_size = np.diff(vt) #vt is in nanoseconds, and np.diff works over day boundaries
    #Default for dt is the median value of gap_size, the time interval differences
    #if dt == None:
    #    dt = np.median(gap_size)
    #    dt0 = dt
    #else:
        #change dt to appropriate type
    #    dt0 = np.timedelta64(int(dt*1e9), 'ns')

    #gap_index_locations = np.where(gap_size > dt0)

    #First create a temporary tplot variable for the data, times need to be in unix time
    x = np.int64(var_data.times)/1e9
    if var_data.y.ndim == 1:
        pytplot.store_data('makegap_tmp', data = {'x':x, 'y':var_data.y})
    else: #multiple dimensions
        var_data_out = None
        pytplot.store_data('makegap_tmp', data = {'x':x, 'y':var_data.y})
#Check for values, v, or v1, v2, v3
        if len(var_data) == 2: #No v's
            pytplot.store_data('makegap_tmp', data = {'x':x, 'y':var_data.y})
        elif len(var_data) == 3: #v or v1,needs indexing if it's 2d
            pytplot.store_data('makegap_tmp', data = {'x':x, 'y':var_data.y, 'v':var_data[2]})
        elif len(var_data) == 4: #has both v1 and v2
            pytplot.store_data('makegap_tmp', data = {'x':x, 'y':var_data.y, 'v1':var_data[2], 'v2':var_data[3]})
        elif len(var_data) == 5: #has v1, v2, v3
            pytplot.store_data('makegap_tmp', data = {'x':x, 'y':var_data.y, 'v1':var_data[2], 'v2':var_data[3], 'v3':var_data[3]})
    #Now, degap the variable
    pytplot.degap('makegap_tmp', dt = dt, margin = margin, func = func, twonanpergap = True)
    #and return the getdata result
    var_data_out = pytplot.get_data('makegap_tmp', dt = True)
    pytplot.del_data('makegap_tmp')
    return var_data_out
#End of makegap.py
