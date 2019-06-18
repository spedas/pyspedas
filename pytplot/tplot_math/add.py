# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot

#ADD TWO ARRAYS
#add two tvar data arrays, store in new_tvar
def add(tvar1,tvar2,new_tvar=None):
    """
        Adds two tplot variables together

        Parameters:
            tvar1 : str
                Name of first tplot variable.
            tvar2 : int/float
                Name of second tplot variable
            new_tvar : str
                Name of new tvar for added data.  If none,

        Returns:
            None

        Examples:
            >>> Make any values below 2 and above 6 equal to NaN.
            >>> pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1],[2,2],[100,100],[4,4],[5,5],[6,6],[7,7]]})
            >>> pytplot.clip('d',2,6,'e')
        """
    #interpolate tvars
    # interpolate tvars
    tv2 = pytplot.tplot_math.tinterp(tvar1, tvar2)
    # separate and subtract data
    data1 = pytplot.data_quants[tvar1].values
    data2 = tv2.values
    data = data1 + data2
    # store subtracted data

    if new_tvar is None:
        new_tvar = tvar1 + '_plus_' + tvar2
        return

    if 'spec_bins' in pytplot.data_quants[tvar1].coords:
        pytplot.store_data(new_tvar, data={'x': pytplot.data_quants[tvar1].coords['time'].values, 'y': data,
                                           'v': pytplot.data_quants[tvar1].coords['spec_bins'].values})
    else:
        pytplot.store_data(new_tvar, data={'x': pytplot.data_quants[tvar1].coords['time'].values, 'y': data})

    return