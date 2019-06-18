# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np

def clip(tvar1,ymin,ymax,newtvar=None):
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


    if newtvar is None:
        newtvar=tvar1+'_clipped'

    if 'spec_bins' in pytplot.data_quants.coords:
        d, s = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar1)
    else:
        d = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar1)

    #grab column indices
    df_index = d.columns.copy()
    new_df = []
    tvar_orig = d
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
        pytplot.store_data(newtvar, data={'x':tvar_orig.data.index,'y':new_df,'v':s.values})
    else:
        pytplot.store_data(newtvar, data={'x':tvar_orig.data.index,'y':new_df})
    return
