# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d


                              
def tplot_resample(tvar1,times,newtvar):
    pytplot.store_data('times_for_resample',data={'x':times,'y':np.zeros(len(times))})
    df_index = pytplot.data_quants[tvar1].data.columns
    new_df = []
    tvar_orig = pytplot.data_quants[tvar1]
    for i in df_index:
        tv2_col = [item[i] for item in tvar_orig.data.values]
        f = interp1d(tvar_orig.data.index,tv2_col,fill_value="extrapolate")
        new_df = new_df + [f(times)]
    new_df = np.transpose((list(new_df)))
    #store interpolated tvars as 'X_interp'
    pytplot.store_data(newtvar, data={'x':times,'y':new_df})
    return
