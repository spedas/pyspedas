# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np

#DERIVE
#take derivative w.r.t. time, store in new_tvar
def derive(tvar1,new_tvar='tvar_derive'):
    #separate and derive data
    time = pytplot.data_quants[tvar1].data.index
    data1 = pytplot.data_quants[tvar1].data
    df_index = pytplot.data_quants[tvar1].data.columns
    new_df = []
    for i in df_index:
        tv1_col = data1[i]
        data = np.diff(tv1_col)/np.diff(time)
        new_df = new_df + [data]
    new_df = np.transpose((list(new_df)))
    time = np.delete(time,0)
    #store differentiated data
    if (pytplot.data_quants[tvar1].spec_bins is not None) and (pytplot.data_quants[tvar1].spec_bins_time_varying == True):
        pytplot.store_data(new_tvar,data={'x':time, 'y':new_df, 'v':pytplot.data_quants[tvar1].spec_bins})
    else:
        pytplot.store_data(new_tvar,data={'x':time, 'y':new_df})
    return new_tvar