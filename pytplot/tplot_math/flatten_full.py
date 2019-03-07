# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot

#FULL FLATTEN
#take average of each column of data, divide column by column average
def flatten_full(tvar1,new_tvar='tvar_ff'):
    df = pytplot.data_quants[tvar1].data
    df_index = list(df.columns)
    #divide by column average
    for i in df_index:
        df[i] = df[i]/df[i].mean()
    pytplot.store_data(new_tvar,data = {'x':df.index,'y':df})
    return new_tvar