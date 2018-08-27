# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np

#PARTIAL ADD ACROSS COLUMNS
#add tvar data across specific columns, store in new_tvar
def add_across_partial(tvar1,column_range,new_tvar):
    #separate and add data
    time = pytplot.data_quants[tvar1].data.index.copy()
    data1 = pytplot.data_quants[tvar1].data.copy()
    data = []
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
    #store added data
    pytplot.store_data(new_tvar,data={'x':time, 'y':np.transpose(data)})
    return new_tvar
