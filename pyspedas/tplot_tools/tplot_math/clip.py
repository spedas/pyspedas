# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pyspedas
from pyspedas.tplot_tools import store_data, tnames
import numpy as np
import copy
import logging

def clip(tvar,ymin,ymax,newname=None):
    """
    Change out-of-bounds data to NaN.

    Parameters
    ----------
        tvar : str or list[str]
            tplot variable names to clip (wildcards accepted)
        ymin : int/float
            Minimum value to keep (inclusive)
        ymax : int/float
            Maximum value to keep (inclusive)
        newname : str
            Name of new tvar for clipped data storage.  If not specified, tvar will be replaced
            THIS is not an option for multiple variable input, for multiple or pseudo variables, the data is overwritten.

    Returns
    -------
        None

    Examples
    --------

        >>> Make any values below 2 and above 6 equal to NaN.
        >>> pyspedas.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1],[2,2],[100,100],[4,4],[5,5],[6,6],[7,7]]})
        >>> pyspedas.clip('d',2,6,'e')

    """

    #check for globbed or array input, and call recursively
    tn = tnames(tvar)
    if len(tn) == 0:
        return
    elif len(tn) > 1:
        for j in range(len(tn)):
            clip(tn[j],ymin,ymax)
        return


    a = copy.deepcopy(pyspedas.tplot_tools.data_quants[tvar].where(pyspedas.tplot_tools.data_quants[tvar] >= ymin))
    a = copy.deepcopy(a.where(a <= ymax))

    if newname is None:
        a.name = tvar
        pyspedas.tplot_tools.data_quants[tvar] = a
    else:
        if 'spec_bins' in a.coords:
            store_data(newname, data={'x': a.coords['time'], 'y': a.values, 'v': a.coords['spec_bins']})
            pyspedas.tplot_tools.data_quants[newname].attrs = copy.deepcopy(pyspedas.tplot_tools.data_quants[tvar].attrs)
        else:
            store_data(newname, data={'x': a.coords['time'], 'y': a.values})
            pyspedas.tplot_tools.data_quants[newname].attrs = copy.deepcopy(pyspedas.tplot_tools.data_quants[tvar].attrs)

    return
