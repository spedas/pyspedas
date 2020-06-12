# Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import copy

def subtract(tvar1,tvar2,new_tvar=None):
    """
    Subtracts two tplot variables.  Will interpolate if the two are not on the same time cadence.

    Parameters:
        tvar1 : str
            Name of first tplot variable.
        tvar2 : int/float
            Name of second tplot variable
        new_tvar : str
            Name of new tvar for added data.  If not set, then the data in tvar1 is replaced.

    Returns:
        None

    Examples:
        >>> pytplot.store_data('a', data={'x':[0,4,8,12,16], 'y':[1,2,3,4,5]})
        >>> pytplot.store_data('c', data={'x':[0,4,8,12,16,19,21], 'y':[1,4,1,7,1,9,1]})
        >>> pytplot.subtract('a','c','a-c')
        """

    #interpolate tvars
    tv2 = pytplot.tplot_math.tinterp(tvar1,tvar2)

    #separate and subtract data
    data1 = pytplot.data_quants[tvar1].values
    data2 = pytplot.data_quants[tv2].values
    data = data1 - data2

    #store subtracted data
    if new_tvar is None:
        pytplot.data_quants[tvar1].values = data
        return tvar1

    if 'spec_bins' in pytplot.data_quants[tvar1].coords:
        pytplot.store_data(new_tvar, data={'x': pytplot.data_quants[tvar1].coords['time'].values, 'y': data, 'v':pytplot.data_quants[tvar1].coords['spec_bins'].values})
        pytplot.data_quants[new_tvar].attrs = copy.deepcopy(pytplot.data_quants[tvar1].attrs)
    else:
        pytplot.store_data(new_tvar,data={'x': pytplot.data_quants[tvar1].coords['time'].values, 'y': data})
        pytplot.data_quants[new_tvar].attrs = copy.deepcopy(pytplot.data_quants[tvar1].attrs)

    return new_tvar
