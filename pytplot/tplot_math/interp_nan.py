# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot

#LINEAR INTERPOLATION
#interpolate over NaN data
def interp_nan(tvar1,newtvar='tvar_interp_nan',s_limit=0):
    if newtvar=='tvar_interp_nan':
        newtvar = tvar1 +"_interp_nan"

    tv1 = pytplot.data_quants[tvar1].data.copy()
    tv1 = tv1.astype(float)
    cadence = tv1.index[1] - tv1.index[0]
    n_nans = int(round(s_limit/cadence))
    if s_limit == 0:
        tv1 = tv1.interpolate(method='linear')
    else:
        tv1 = tv1.interpolate(method='linear',limit=n_nans,limit_direction='both') 
    tv1 = tv1.astype(object)

    if (pytplot.data_quants[tvar1].spec_bins is not None):
        pytplot.store_data(newtvar,data = {'x':tv1.index,'y':tv1, 'v': pytplot.data_quants[tvar1].spec_bins})
    else:
        pytplot.store_data(newtvar, data={'x': tv1.index, 'y': tv1})
    return