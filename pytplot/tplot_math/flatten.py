# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot

#PARTIAL FLATTEN
#take average of each column of data, divide column by average over specified time
def flatten(tvar1,start_t,end_t,new_tvar='tvar_flat'):
    df = pytplot.data_quants[tvar1].data
    time = df.index
    #if time given not an index, choose closest time
    if start_t not in time:
        tdiff = abs(time - start_t)
        start_t = time[tdiff.argmin()]
    if end_t not in time:
        tdiff = abs(time - end_t)
        end_t = time[tdiff.argmin()]
    df_index = list(df.columns)
    #divide by specified time average
    for i in df_index:
        df[i] = df[i]/((df.loc[start_t:end_t])[i]).mean()
    pytplot.store_data(new_tvar,data = {'x':df.index,'y':df})
    return new_tvar