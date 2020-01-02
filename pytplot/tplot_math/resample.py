# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import copy
                              
def resample(tvar,times,new_tvar=None):
    """
    Linearly interpolates data to user-specified values.  To interpolate one tplot variable to another, use tinterp.

    .. note::
        This analysis routine assumes the data is no more than 2 dimensions.  If there are more, they may become flattened!

    Parameters:
        tvar : str
            Name of tvar whose data will be interpolated to specified times.
        times : int/list
            Desired times for interpolation.
        new_tvar : str
            Name of new tvar in which to store interpolated data.  If none is specified, tvar will be overwritten

    Returns:
        None

    Examples:
        >>> # Interpolate data for 'd' to values [3,4,5,6,7,18].
        >>> pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1],[2,2],[100,100],[4,4],[5,5],[6,6],[7,7]]})
        >>> pytplot.tplot_resample('d',[3,4,5,6,7,18],'d_resampled')
    """

    x = pytplot.data_quants[tvar].interp(time=times)

    if new_tvar is None:
        x.attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)
        pytplot.data_quants[tvar] = x
        x.name = tvar
    else:
        pytplot.data_quants[new_tvar] = copy.deepcopy(x)
        pytplot.data_quants[new_tvar].attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)
        pytplot.data_quants[new_tvar].name = new_tvar

    return
