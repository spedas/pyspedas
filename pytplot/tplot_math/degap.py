# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np
import pandas as pd
import copy
    
def degap(tvar,dt,margin,func='nan'):
    '''
    Fills data within margin(s) where data may not be correct.

    Required Arguments:
        tvar : str
            Name of tvar to modify.
        dt : int/float
            Step size of the data in seconds
        margin : int/float
            The maximum deviation from the step size allowed before degapping occurs

    Optional Arguments:
        func : str
            Either 'nan' or 'ffill', which overrides normal interpolation with NaN
            substitution or forward-filled values.
    Returns:
        None

    Examples:
        Null data between [3,7], and [13,17], with step size 2.3.
         pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1],[2,2],[100,100],[4,4],[5,5],[6,6],[7,7]]})
         pytplot.degap('d',[[3,7],[13,17]],2.3,func='nan')
    '''

    new_tvar = copy.deepcopy(pytplot.data_quants[tvar])
    gap_size = np.diff(new_tvar.data.index)
    gap_index_locations = np.where(gap_size > dt+margin)
    new_tvar_index = new_tvar.data.index.values
    values_to_add = np.array([])
    for i in gap_index_locations[0]:
        values_to_add = np.append(values_to_add, np.arange(new_tvar_index[i], new_tvar_index[i+1], dt))

    new_index = pd.Index(np.sort(np.unique(np.concatenate((values_to_add, new_tvar_index)))))

    if func == 'nan':
        #add any new indices to current dataframe indices
        new_tvar.data.reindex(new_index)
        new_tvar.number = len(pytplot.data_quants)
        pytplot.data_quants[tvar+"_degapped"] = new_tvar
    if func == 'ffill':
        #interpolate to create data for new values
        pytplot.tplot_math.resample(tvar,new_index,tvar+'_degapped')

    return