# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot

#DATA CROPPING
#crop tvar arrays to same timespan
def crop(tvar1,tvar2, replace=False):
    # grab time and data arrays
    tv1 = pytplot.data_quants[tvar1].copy()
    tv2 = pytplot.data_quants[tvar2].copy()
    # find first and last time indices
    t0_1 = tv1.coords['time'][0]
    t0_2 = tv2.coords['time'][0]
    tx_1 = tv1.coords['time'][-1]
    tx_2 = tv2.coords['time'][-1]
    # find cut locations
    cut1 = max([t0_1, t0_2])
    cut2 = min([tx_1, tx_2])
    # trim data
    tv1 = tv1.sel(time=slice(cut1, cut2))
    tv2 = tv2.sel(time=slice(cut1, cut2))
    # Replace the variables if specified
    if replace:
        pytplot.data_quants[tvar1] = tv1
        pytplot.data_quants[tvar2] = tv2
        return None, None

    #return time and data arrays
    return tv1, tv2