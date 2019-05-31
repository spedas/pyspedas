# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import pandas as pd

#JOIN TVARS
#join TVars into single TVar with multiple columns
def join_vec(tvars,newtvar='tvar_join'):
    if not isinstance(tvars, list):
        tvars = [tvars]
    if newtvar == 'tvar_join':
        newtvar = '-'.join(tvars)+'_joined'

    df = pytplot.data_quants[tvars[0]].data
    for i,val in enumerate(tvars):
        if i == 0:
            pass
        else:
            df = pd.concat([df,pytplot.data_quants[val].data],axis=1)

    pytplot.store_data(newtvar,data={'x': df.index,'y': df})
    return