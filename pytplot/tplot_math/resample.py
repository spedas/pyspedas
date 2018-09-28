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

                              
def resample(tvar1,times,newtvar='tvar_resample'):
    #create dummy dataframe for times to interpolate to
    pytplot.store_data('times_for_resample',data={'x':times,'y':np.zeros(len(times))})
    df_index = pytplot.data_quants[tvar1].data.columns.copy()
    new_df = []
    spec_df = []
    tvar_orig = pytplot.data_quants[tvar1].data.copy()
    
    if (pytplot.data_quants[tvar1].spec_bins is not None) and (pytplot.data_quants[tvar1].spec_bins_time_varying == True):
        spec_orig = pytplot.data_quants[tvar1].spec_bins.copy()
        
    #for each column of dataframe
    for i in df_index:
        tv2_col = [item[i] for item in tvar_orig.values]
        if (pytplot.data_quants[tvar1].spec_bins is not None) and (pytplot.data_quants[tvar1].spec_bins_time_varying == True):
            spec_col = [item[i] for item in spec_orig.values]
        #linear interpolation
        f = interp1d(tvar_orig.index,tv2_col,fill_value="extrapolate")
        new_df = new_df + [f(times)]
        
        if (pytplot.data_quants[tvar1].spec_bins is not None) and (pytplot.data_quants[tvar1].spec_bins_time_varying == True):
            g = interp1d(tvar_orig.index,spec_col,fill_value="extrapolate")
            spec_df = spec_df + [g(times)]
    new_df = np.transpose((list(new_df)))
    
    if (pytplot.data_quants[tvar1].spec_bins is not None) and (pytplot.data_quants[tvar1].spec_bins_time_varying == True):
        spec_df = np.transpose((list(spec_df)))
    #store interpolated tvar
    if (pytplot.data_quants[tvar1].spec_bins is not None) and (pytplot.data_quants[tvar1].spec_bins_time_varying == True):
        pytplot.store_data(newtvar, data={'x':times,'y':new_df,'v':spec_df})
    else:
        pytplot.store_data(newtvar, data={'x':times,'y':new_df})
    #delete dummy dataframe from pytplot.data_quants
    pytplot.del_data(name='times_for_resample')
    return
