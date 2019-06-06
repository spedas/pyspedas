# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np

#ADD ACROSS COLUMNS
#add tvar data across specific columns, store in new_tvar
def add_across(tvar1,column_range=None,new_tvar=None):
    # separate and add data
    if new_tvar is None:
        new_tvar = tvar1 + "_summed"
    if 'spec_bins' in pytplot.data_quants.coords:
        d, s = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar1)
    else:
        d = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar1)
        s = None

    time = d.index.copy()
    data1 = d.values.copy()
    data2 = d.values.copy()
    data = []
    spec_data = []

    if column_range is None:
        column_range = [0, len(d.columns)-1]

    #grab column data
    if len(column_range)==2 and isinstance(column_range[0],int):
        range_start = column_range[0]
        range_end = column_range[1]
        add_col = list(range(range_start,range_end+1))
        datasum = data1[add_col].sum(axis=1)
        data = data + [list(datasum)]
    else:
        for i in column_range:
            #if not a list
            if type(i) == int:
                data = data + [list(data1[i])]
            #sum across listed column range
            else:
                range_start = i[0]
                range_end = i[1]
                add_col = list(range(range_start,range_end+1))
                datasum = data1[add_col].sum(axis=1)
                data = data + [list(datasum)]

    if s is not None:
        if len(column_range) == 2 and isinstance(column_range[0], int):
            range_start = column_range[0]
            range_end = column_range[1]
            add_col = list(range(range_start, range_end + 1))
            datasum = data2[add_col].mean(axis=1)
            spec_data = spec_data + [list(datasum)]
        else:
            for i in column_range:
                # if not a list
                if type(i) == int:
                    spec_data = spec_data + [list(data2[i])]
                # sum across listed column range
                else:
                    range_start = i[0]
                    range_end = i[1]
                    add_col = list(range(range_start, range_end + 1))
                    datasum = data2[add_col].mean(axis=1)
                    spec_data = spec_data + [list(datasum)]

    #store added data
    if s is None:
        pytplot.store_data(new_tvar,data={'x':time, 'y':np.transpose(data)})
    else:
        pytplot.store_data(new_tvar, data={'x': time, 'y':np.transpose(data), 'v': np.transpose(spec_data)})
    return
