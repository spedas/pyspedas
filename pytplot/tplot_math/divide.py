# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np

#DIVIDE
#divide two tvar data arrays, store in new_tvar
def divide(tvar1,tvar2,new_tvar='tvar_divide',interp='linear'):
    #interpolate tvars
    tv1,tv2 = pytplot.interpolate(tvar1,tvar2,interp=interp)
    #separate and divide data
    time = pytplot.data_quants[tv1].data.index
    data1 = pytplot.data_quants[tv1].data
    data2 = pytplot.data_quants[tv2].data
    data = data1/data2
    #if division by 0, replace with NaN
    data = data.replace([np.inf,-np.inf],np.nan)
    #store divided data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar