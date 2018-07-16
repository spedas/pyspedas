# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d

"""
    Linearly interpolates data to user-specified values 
    
    Parameters:
        tvar1 : str
            Name of tvar whose data will be interpolated to specified times.  
        times : int/list
            Desired times for interpolation.
        newtvar : str
            Name of new tvar in which to store interpolated data.
            
    Returns:
        None
    
    Examples:
        >>> Interpolate data for 'd' to values [3,4,5,6,7,18].
        >>> pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1],[2,2],[100,100],[4,4],[5,5],[6,6],[7,7]]})
        >>> pytplot.tplot_resample('d',[3,4,5,6,7,18],'d_resampled')
    """

                              
def tplot_resample(tvar1,times,newtvar):
    #create dummy dataframe for times to interpolate to
    pytplot.store_data('times_for_resample',data={'x':times,'y':np.zeros(len(times))})
    df_index = pytplot.data_quants[tvar1].data.columns
    new_df = []
    tvar_orig = pytplot.data_quants[tvar1]
    #for each column of dataframe
    for i in df_index:
        tv2_col = [item[i] for item in tvar_orig.data.values]
        #linear interpolation
        f = interp1d(tvar_orig.data.index,tv2_col,fill_value="extrapolate")
        new_df = new_df + [f(times)]
    new_df = np.transpose((list(new_df)))
    #store interpolated tvar'
    pytplot.store_data(newtvar, data={'x':times,'y':new_df})
    #delete dummy dataframe from pytplot.data_quants
    pytplot.del_data(name='times_for_resample')
    return
