# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot

#PARTIAL FLATTEN
#take average of each column of data, divide column by average over specified time
def flatten(tvar1,range=None,new_tvar=None):
    if new_tvar is None:
        new_tvar = tvar1 + "_flattened"

    if 'spec_bins' in pytplot.data_quants[tvar1].coords:
        df, s = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar1)
    else:
        d = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar1)

    if range is None:
        pass

    time = df.index
    #if time given not an index, choose closest time
    if range is None:
        df_index = list(df.columns)
        # divide by column average
        for i in df_index:
            df[i] = df[i] / df[i].mean()
    else:
        if range[0] not in time:
            tdiff = abs(time - range[0])
            start_t = time[tdiff.argmin()]
        if range[1] not in time:
            tdiff = abs(time - range[1])
            end_t = time[tdiff.argmin()]
        df_index = list(df.columns)

        #divide by specified time average
        for i in df_index:
            df[i] = df[i]/((df.loc[start_t:end_t])[i]).mean()

    if s is not None:
        pytplot.store_data(new_tvar,data = {'x':df.index,'y':df.values, 'v': s.values})
    else:
        pytplot.store_data(new_tvar, data={'x': df.index, 'y': df.values})
    return