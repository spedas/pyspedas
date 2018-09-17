# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot

#MULTIPLY
#multiply two tvar data arrays, store in new_tvar
def multiply(tvar1,tvar2,new_tvar='tvar_multiply',interp='linear'):
    #interpolate tvars
    tv1,tv2 = pytplot.interpolate(tvar1,tvar2,interp=interp)
    #separate and multiply data
    time = pytplot.data_quants[tv1].data.index
    data1 = pytplot.data_quants[tv1].data
    data2 = pytplot.data_quants[tv2].data
    data = data1*data2
    #store multiplied data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar