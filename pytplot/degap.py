# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np

"""
    Fills data within margin(s) where data may not be correct.
    
    Required Arguments:
        tvar : str
            Name of tvar to modify.  
        margin : list
            Index values between which data values will be modified
        dt : int/float
            Step size to interpolate rows, then modify
    
    Optional Arguments:
        func : str
            Either 'nan' or 'ffill', which overrides normal interpolation with NaN
            substitution or forward-filled values.
    Returns:
        None
    
    Examples:
        >>> Null data between [3,7], and [13,17], with step size 2.3.
        >>> pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1],[2,2],[100,100],[4,4],[5,5],[6,6],[7,7]]})
        >>> pytplot.degap('d',[[3,7],[13,17]],2.3,func='nan')  
    """

#pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1],[2,2],[100,100],[4,4],[5,5],[6,6],[7,7]]})
def degap(tvar,margin,dt,func=None):
    tv1 = pytplot.data_quants[tvar].data
    indices = []
    #create array of dt between margin parameters
    for m in margin:
        if type(m) == int:
            new_index = np.arange(margin[0],margin[1],dt)
        else:
            new_index = np.arange(m[0],m[1],dt)
        new_index = np.append(new_index,new_index[-1]+dt)
        indices = indices + [new_index]
    #add any new indices to current dataframe indices
    new_index = np.unique(np.append(indices,tv1.index))
    #interpolate to create data for new values
    pytplot.tplot_resample(tvar,new_index,tvar+'_interp')
        
    if func == 'nan':
        tv1 = pytplot.data_quants[tvar+'_interp'].data
        #any location between margins will be changed to NaN
        for i in indices:
            tv1.loc[i[0]:i[-1]] = np.nan
        pytplot.store_data(tvar+'_nan',data = {'x':tv1.index.values,'y':tv1})
        pytplot.del_data(name=tvar+'_interp')

    if func == 'ffill':
        tv1 = pytplot.data_quants[tvar+'_interp'].data
        #any location between margins will be changed to NaN
        for i in indices:
            tv1.loc[i[0]:i[-1]] = np.nan
        #forward fill NaNs in the dataframe
        tv1 = tv1.fillna(method='ffill')
        pytplot.store_data(tvar+'_ffill',data = {'x':tv1.index.values,'y':tv1})
        pytplot.del_data(name=tvar+'_interp')

    return
          