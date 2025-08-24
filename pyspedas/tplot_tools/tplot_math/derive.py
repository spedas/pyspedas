# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pyspedas
from pyspedas.tplot_tools import store_data
import numpy as np
import copy
import logging

def derive(tvar,newname=None):
    """
    Takes the derivative of the tplot variable.

    Parameters
    ----------
        tvar : str
            Name of tplot variable.
        newname : str
            Name of new tplot variable.  If not set, then the data in tvar is replaced.

    Returns
    -------
        None

    Examples
    --------

        >>> pyspedas.store_data('b', data={'x':[2,5,8,11,14,17,20], 'y':[[1,1,1,1,1,1],[2,2,5,4,1,1],[100,100,3,50,1,1],[4,4,8,58,1,1],[5,5,9,21,1,1],[6,6,2,2,1,1],[7,7,1,6,1,1]]})
        >>> pyspedas.derive('b','dbdt')

    """

    a = pyspedas.tplot_tools.data_quants[tvar].differentiate('time')
    if newname is None:
        a.name = tvar
        a.attrs = copy.deepcopy(pyspedas.tplot_tools.data_quants[tvar].attrs)
        pyspedas.tplot_tools.data_quants[tvar] = a
    else:
        data = {'x':a.coords['time'], 'y':a.values * 1e09}  # Internal time in units of nanoseconds
        for coord in a.coords:
            if coord != 'time' and coord != 'spec_bins':
                data[coord] = a.coords[coord].values

        store_data(newname, data=data)
        pyspedas.tplot_tools.data_quants[newname].attrs = copy.deepcopy(pyspedas.tplot_tools.data_quants[tvar].attrs)

    return
