# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import pandas as pd

#JOIN TVARS
#join TVars into single TVar with multiple columns
def join_vec(tvars,new_tvar=None):

    if not isinstance(tvars, list):
        tvars = [tvars]
    if new_tvar is None:
        new_tvar = '-'.join(tvars)+'_joined'


    for i,val in enumerate(tvars):
        if i == 0:
            if 'spec_bins' in pytplot.data_quants[tvars[i]].coords:
                df, s = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvars[i])
            else:
                df = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvars[i])
                s = None
        else:
            if 'spec_bins' in pytplot.data_quants[tvars[i]].coords:
                d, _ = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvars[i])
            else:
                d = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvars[i])
            df = pd.concat([df,d],axis=1)

    if s is None:
        pytplot.store_data(new_tvar,data={'x': df.index,'y': df.values})
    else:
        pytplot.store_data(new_tvar, data={'x': df.index, 'y': df.values, 'v': s.values})
    return