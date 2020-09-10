# Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import pandas as pd
import copy
import xarray as xr

#JOIN TVARS
#join TVars into single TVar with multiple columns
def join_vec(tvars,new_tvar=None, merge=False):
    """
    Joins 1D tplot variables into one tplot variable.

    .. note::
        This analysis routine assumes the data is no more than 2 dimensions.  If there are more, they may become flattened!

    Parameters:
        tvars : list of str
            Name of tplot variables to join together
        new_tvar : str, optional
            The name of the new tplot variable. If not specified, a name will be assigned.
        merge : bool, optional
            Whether or not to merge the created variable into an older variable

    Returns:
        None

    Examples:
        >>> pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1,50],[2,2,3],[100,4,47],[4,90,5],[5,5,99],[6,6,25],[7,7,-5]]})
        >>> pytplot.store_data('e', data={'x':[2,5,8,11,14,17,21], 'y':[[np.nan,1,1],[np.nan,2,3],[4,np.nan,47],[4,np.nan,5],[5,5,99],[6,6,25],[7,np.nan,-5]]})
        >>> pytplot.store_data('g', data={'x':[0,4,8,12,16,19,21], 'y':[[8,1,1],[100,2,3],[4,2,47],[4,39,5],[5,5,99],[6,6,25],[7,-2,-5]]})
        >>> pytplot.join_vec(['d','e','g'],'deg')
        >>> print(pytplot.data_quants['deg'].values)
    """

    if not isinstance(tvars, list):
        tvars = [tvars]
    if new_tvar is None:
        new_tvar = '-'.join(tvars)+'_joined'

    to_merge=False
    if new_tvar in pytplot.data_quants.keys() and merge:
        prev_data_quant = pytplot.data_quants[new_tvar]
        to_merge = True

    for i,val in enumerate(tvars):
        if i == 0:
            if 'spec_bins' in pytplot.data_quants[tvars[i]].coords:
                df, s = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvars[i])
            else:
                df = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvars[i], no_spec_bins=True)
                s = None
        else:
            if 'spec_bins' in pytplot.data_quants[tvars[i]].coords:
                d = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvars[i], no_spec_bins=True)
            else:
                d = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvars[i], no_spec_bins=True)
            df = pd.concat([df,d],axis=1)

    if s is None:
        pytplot.store_data(new_tvar,data={'x': df.index,'y': df.values})
    else:
        pytplot.store_data(new_tvar, data={'x': df.index, 'y': df.values, 'v': s.values})

    if to_merge is True:
        cur_data_quant = pytplot.data_quants[new_tvar]
        plot_options = copy.deepcopy(pytplot.data_quants[new_tvar].attrs)
        pytplot.data_quants[new_tvar] = xr.concat([prev_data_quant, cur_data_quant], dim='time').sortby('time')
        pytplot.data_quants[new_tvar].attrs = plot_options

    return new_tvar
