# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import copy

def interp_nan(tvar, new_tvar=None, s_limit=None):
    """
    Interpolates the tplot variable through NaNs in the data.  This is basically just a wrapper for xarray's interpolate_na function.

    .. note::
        This analysis routine assumes the data is no more than 2 dimensions.  If there are more, they may become flattened!

    Parameters:
        tvar : str
            Name of tplot variable.
        s_limit : int or float, optional
            The maximum size of the gap in seconds to not interpolate over.  I.e. if there are too many NaNs in a row, leave them there.
        new_tvar : str
            Name of new tvar for added data.  If not set, then the original tvar is replaced.

    Returns:
        None

    Examples:
        >>> # Interpolate through the np.NaN values
        >>> pytplot.store_data('e', data={'x':[2,5,8,11,14,17,21], 'y':[[np.nan,1,1],[np.nan,2,3],[4,np.nan,47],[4,np.nan,5],[5,5,99],[6,6,25],[7,np.nan,-5]]})
        >>> pytplot.interp_nan('e','e_nonan',s_limit=5)
        >>> print(pytplot.data_quants['e_nonan'].values)
    """

    x = pytplot.data_quants[tvar].interpolate_na(dim='time', limit=s_limit)
    x.attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)

    if new_tvar is None:
        pytplot.data_quants[tvar] = x
        x.name = tvar
    else:
        pytplot.data_quants[new_tvar] = x
        pytplot.data_quants[new_tvar].name = new_tvar


