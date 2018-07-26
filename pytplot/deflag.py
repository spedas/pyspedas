# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d

"""
    Change specified 'flagged' data to NaN.
    
    Parameters:
        tvar1 : str
            Name of tvar to use for data clipping.  
        flags : int,list
            Flagged data will be converted to NaNs.
        newtvar : str
            Name of new tvar for deflagged data storage
            
    Returns:
        None
    
    Examples:
        >>> Remove any instances of [100,90,7,2,57] from 'd', store in 'e'.
        >>> pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1],[2,2],[100,4],[4,90],[5,5],[6,6],[7,7]]})
        >>> pytplot.deflag('d',[100,90,7,2,57],'e')
    """

                              
def deflag(tvar1,flags,newtvar):
    #if int input, make list
    if not isinstance(flags,list):
        flags = [flags]
    #grab column indices
    df_index = pytplot.data_quants[tvar1].data.columns
    new_df = []
    tvar_orig = pytplot.data_quants[tvar1]
    #for each column of dataframe
    for i in df_index:
        tv2_col = [item[i] for item in tvar_orig.data.values]
        for j,valj in enumerate(tv2_col):
            #if one of flagged values, convert to NaN
            if valj in flags:
                tv2_col[j] = np.NaN
        new_df = new_df + [tv2_col]
    new_df = np.transpose((list(new_df)))
    #store deflagged tvar
    pytplot.store_data(newtvar, data={'x':tvar_orig.data.index,'y':new_df})
    return
