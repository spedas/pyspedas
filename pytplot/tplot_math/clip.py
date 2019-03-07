# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np

"""
    Change out-of-bounds data to NaN.
    
    Parameters:
        tvar1 : str
            Name of tvar to use for data clipping.  
        ymin : int/float
            Minimum value to keep (inclusive)
        ymax : int/float
            Maximum value to keep (inclusive)
        newtvar : str
            Name of new tvar for clipped data storage
            
    Returns:
        None
    
    Examples:
        >>> Make any values below 2 and above 6 equal to NaN.
        >>> pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1],[2,2],[100,100],[4,4],[5,5],[6,6],[7,7]]})
        >>> pytplot.clip('d',2,6,'e')
    """

                              
def clip(tvar1,ymin,ymax,newtvar='tvar_clip'):
    #grab column indices
    df_index = pytplot.data_quants[tvar1].data.columns.copy()
    new_df = []
    tvar_orig = pytplot.data_quants[tvar1]
    #for each column of dataframe
    for i in df_index:
        tv2_col = [item[i] for item in tvar_orig.data.values]
        for j,valj in enumerate(tv2_col):
            #if value in column out of specified range, substitute NaN
            if (valj < ymin) or (valj > ymax):
                tv2_col[j] = np.NaN
        new_df = new_df + [tv2_col]
    new_df = np.transpose((list(new_df)))
    #store clipped tvar
    if pytplot.data_quants[tvar1].spec_bins is not None:
        pytplot.store_data(newtvar, data={'x':tvar_orig.data.index,'y':new_df,'v':pytplot.data_quants[tvar1].spec_bins})
    else:
        pytplot.store_data(newtvar, data={'x':tvar_orig.data.index,'y':new_df})
    return
