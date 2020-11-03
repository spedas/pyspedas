# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import copy

                              
def deflag(tvar,flag,new_tvar=None):
    """
    Change specified 'flagged' data to NaN.

    Parameters:
        tvar1 : str
            Name of tplot variable to use for data clipping.
        flag : int,list
            Flagged data will be converted to NaNs.
        newtvar : str
            Name of new tvar for deflagged data storage.  If not specified, then the data in tvar1 will be replaced.

    Returns:
        None

    Examples:
        >>> # Remove any instances of [100,90,7,2,57] from 'd', store in 'e'.
        >>> pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1],[2,2],[100,4],[4,90],[5,5],[6,6],[7,7]]})
        >>> pytplot.deflag('d',[100,90,7,2,57],'e')
    """

    a = copy.deepcopy(pytplot.data_quants[tvar].where(pytplot.data_quants[tvar]!=flag))


    if new_tvar is None:
        a.name = tvar
        pytplot.data_quants[tvar] = a
    else:
        if 'spec_bins' in a.coords:
            pytplot.store_data(new_tvar, data={'x': a.coords['time'], 'y': a.values, 'v': a.coords['spec_bins']})
            pytplot.data_quants[new_tvar].attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)
        else:
            pytplot.store_data(new_tvar, data={'x': a.coords['time'], 'y': a.values})
            pytplot.data_quants[new_tvar].attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)

    return
