# Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import copy


def tinterp(tvar1,tvar2,replace=False):
    """
    Interpolates one tplot variable to another one's time cadence.  This is done automatically by other processing routines.

    Parameters:
        tvar1 : str
            Name of first tplot variable whose times will be used to interpolate tvar2's data.
        tvar2 : str
            Name of second tplot variable whose data will be interpolated.
        replace : bool, optional
            If true, the data in the original tplot variable is replaced.  Otherwise, a variable is created.

    Returns:
        new_var2, the name of the new tplot variable

    Examples:
        >>> pytplot.store_data('a', data={'x':[0,4,8,12,16], 'y':[1,2,3,4,5]})
        >>> pytplot.store_data('c', data={'x':[0,4,8,12,16,19,21], 'y':[1,4,1,7,1,9,1]})
        >>> pytplot.tinterp('a','c')
        >>> print(pytplot.data_quants['c_interp'].data)
    """
    new_tvar2 = pytplot.data_quants[tvar2].interp_like(pytplot.data_quants[tvar1])

    if replace:
        pytplot.data_quants[tvar2] = new_tvar2
        return
    else:
        pytplot.data_quants[tvar1 + '_tinterp'] = copy.deepcopy(new_tvar2)
        pytplot.data_quants[tvar1 + '_tinterp'].attrs = copy.deepcopy(new_tvar2.attrs)
        pytplot.data_quants[tvar1 + '_tinterp'].name = tvar1 + '_tinterp'

    return tvar1 + '_tinterp'
