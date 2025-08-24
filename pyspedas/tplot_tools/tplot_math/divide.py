# Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pyspedas
from pyspedas.tplot_tools import store_data, tinterp
import numpy as np
import copy
import logging

def divide(tvar1,tvar2,newname=None):
    """
    Divides two tplot variables.  Will interpolate if the two are not on the same time cadence.

    Parameters
    ----------
        tvar1 : str
            Name of first tplot variable.
        tvar2 : int/float
            Name of second tplot variable
        newname : str
            Name of new tvar for divided data.  If not set, then the data in tvar1 is replaced.

    Returns
    -------
        None

    Examples
    --------

        >>> pyspedas.store_data('a', data={'x':[0,4,8,12,16], 'y':[1,2,3,4,5]})
        >>> pyspedas.store_data('c', data={'x':[0,4,8,12,16,19,21], 'y':[1,4,1,7,1,9,1]})
        >>> pyspedas.divide('a','c','a_over_c')
        """

    # interpolate tvars
    tv2 = tinterp(tvar1, tvar2)
    # separate and divide data
    data1 = pyspedas.tplot_tools.data_quants[tvar1].values
    data2 = pyspedas.tplot_tools.data_quants[tv2].values
    data = data1 / data2
    # store divided data
    if newname is None:
        pyspedas.tplot_tools.data_quants[tvar1].values = data
        return tvar1
    if 'spec_bins' in pyspedas.tplot_tools.data_quants[tvar1].coords:
        store_data(newname, data={'x': pyspedas.tplot_tools.data_quants[tvar1].coords['time'].values, 'y': data,
                                           'v': pyspedas.tplot_tools.data_quants[tvar1].coords['spec_bins'].values})
        pyspedas.tplot_tools.data_quants[newname].attrs = copy.deepcopy(pyspedas.tplot_tools.data_quants[tvar1].attrs)
    else:
       store_data(newname, data={'x':pyspedas.tplot_tools.data_quants[tvar1].coords['time'].values, 'y': data})
       pyspedas.tplot_tools.data_quants[newname].attrs = copy.deepcopy(pyspedas.tplot_tools.data_quants[tvar1].attrs)

    return newname
