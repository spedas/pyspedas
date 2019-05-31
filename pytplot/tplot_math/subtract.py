# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
#SUBTRACT
#subtract two tvar data arrays, store in new_tvar
def subtract(tvar1,tvar2,new_tvar='tvar_subtract',interp='linear'):
    '''
    :param tvar1: The first tvar
    :param tvar2: The second tvar
    :param new_tvar: The name of the new tplot variable
    :param interp: Method to interpolate tvar2 to the tvar1 time cadence
    :return: New tplot variable created.
    '''
    #interpolate tvars
    tv1,tv2 = pytplot.interpolate(tvar1,tvar2,interp=interp)
    #separate and subtract data
    time = pytplot.data_quants[tv1].data.index
    data1 = pytplot.data_quants[tv1].data
    data2 = pytplot.data_quants[tv2].data
    data = data1 - data2
    #store subtracted data
    pytplot.store_data(new_tvar,data={'x': time, 'y': data})
    return new_tvar