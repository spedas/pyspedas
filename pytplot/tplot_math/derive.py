# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np
import copy

def derive(tvar,new_tvar=None):
    """
    Takes the derivative of the tplot variable.

    Parameters:
        tvar : str
            Name of tplot variable.
        new_tvar : str
            Name of new tplot variable.  If not set, then the data in tvar is replaced.

    Returns:
        None

    Examples:
        >>> pytplot.store_data('b', data={'x':[2,5,8,11,14,17,20], 'y':[[1,1,1,1,1,1],[2,2,5,4,1,1],[100,100,3,50,1,1],[4,4,8,58,1,1],[5,5,9,21,1,1],[6,6,2,2,1,1],[7,7,1,6,1,1]]})
        >>> pytplot.derive('b','dbdt')
        >>> print(pytplot.data_quants['dbdt'].values)
    """

    a = pytplot.data_quants[tvar].differentiate('time')
    if new_tvar is None:
        a.name = tvar
        a.attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)
        pytplot.data_quants[tvar] = a
    else:
        data = {'x':a.coords['time'], 'y':a.values}
        for coord in a.coords:
            if coord != 'time' and coord != 'spec_bins':
                data[coord] = a.coords[coord].values

        pytplot.store_data(new_tvar, data=data)
        pytplot.data_quants[new_tvar].attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)

    return
