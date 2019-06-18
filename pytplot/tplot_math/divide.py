# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np

#DIVIDE
#divide two tvar data arrays, store in new_tvar
def divide(tvar1,tvar2,new_tvar=None):
    """
        Divides two tplot variables.  Will interpolate if the two are not on the same time cadence.

        Parameters:
            tvar1 : str
                Name of first tplot variable.
            tvar2 : int/float
                Name of second tplot variable
            new_tvar : str
                Name of new tvar for divided data.  If not set, then the data in tvar1 is replaced.

        Returns:
            None

        Examples:
            >>> pytplot.store_data('a', data={'x':[0,4,8,12,16], 'y':[1,2,3,4,5]})
            >>> pytplot.store_data('c', data={'x':[0,4,8,12,16,19,21], 'y':[1,4,1,7,1,9,1]})
            >>> pytplot.divide('a','c','a_over_c')
        """
    # interpolate tvars
    tv2 = pytplot.tplot_math.tinterp(tvar1, tvar2)
    # separate and divide data
    data1 = pytplot.data_quants[tvar1].values
    data2 = tv2.values
    data = data1 / data2
    # store divided data
    if new_tvar is None:
        pytplot.data_quants[tvar1].values = data
        return
    if 'spec_bins' in pytplot.data_quants[tvar1].coords:
        pytplot.store_data(new_tvar, data={'x': pytplot.data_quants[tvar1].coords['time'].values, 'y': data,
                                           'v': pytplot.data_quants[tvar1].coords['spec_bins'].values})
    else:
        pytplot.store_data(new_tvar, data={'x': pytplot.data_quants[tvar1].coords['time'].values, 'y': data})
    return