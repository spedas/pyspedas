# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np

#DATA CROPPING
#crop tvar arrays to same timespan
def crop(tvar1,tvar2):
    #grab time and data arrays
    tv1_t = np.asarray(pytplot.data_quants[tvar1].data.index.copy().tolist())
    tv1_d = np.asarray(pytplot.data_quants[tvar1].data.copy())
    tv2_t = np.asarray(pytplot.data_quants[tvar2].data.index.copy().tolist())
    tv2_d = np.asarray(pytplot.data_quants[tvar2].data.copy())
    #find first and last time indices
    t0_1 = tv1_t[0]
    t0_2 = tv2_t[0]
    tx_1 = tv1_t[-1]
    tx_2 = tv2_t[-1]
    #find cut locations
    cut1 = max([t0_1, t0_2])
    cut2 = min([tx_1, tx_2])
    #trim data
    while tv1_t[-1] > cut2:
        tv1_t = np.delete(tv1_t,-1,axis=0)
        tv1_d = np.delete(tv1_d,-1,axis=0)
    while tv1_t[0] < cut1:
        tv1_t = np.delete(tv1_t,0,axis=0)
        tv1_d = np.delete(tv1_d,0,axis=0)
    while tv2_t[-1] > cut2:
        tv2_t = np.delete(tv2_t,-1,axis=0)
        tv2_d = np.delete(tv2_d,-1,axis=0)
    while tv2_t[0] < cut1:
        tv2_t = np.delete(tv2_t,0,axis=0)
        tv2_d = np.delete(tv2_d,0,axis=0)
    #return time and data arrays
    return tv1_t,tv1_d,tv2_t,tv2_d