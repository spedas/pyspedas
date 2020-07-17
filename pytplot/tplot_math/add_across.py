# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import numpy as np
import copy

def add_across(tvar,column_range=None,new_tvar=None):
    """
    Adds across columns in the tplot variable

    .. note::
        This analysis routine assumes the data is no more than 2 dimensions.  If there are more, they may become flattened!

    Parameters:
        tvar : str
            Name of tplot variable.
        column_range: list of ints
            The columns to add together.  For example, if [1,4] is given here, columns 1, 2, 3, and 4 will be added together.
            If not set, then every column is added.
        new_tvar : str
            Name of new tvar for averaged data.  If not set, then the variable is replaced

    Returns:
        None

    Examples:
        >>> #Add across every column in the data
        >>> pytplot.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1,50],[2,2,3],[100,4,47],[4,90,5],[5,5,99],[6,6,25],[7,7,-5]]})
        >>> pytplot.add_across('d',new_tvar='d_aa')
        >>> print(pytplot.data_quants['d_aa'].data)

        >>> #Add across specific columns in the data
        >>> pytplot.store_data('b', data={'x':[2,5,8,11,14,17,20], 'y':[[1,1,1,1,1,1],[2,2,5,4,1,1],[100,100,3,50,1,1],[4,4,8,58,1,1],[5,5,9,21,1,1],[6,6,2,2,1,1],[7,7,1,6,1,1]]})
        >>> pytplot.add_across('b',column_range=[[1,2],[3,4]],new_tvar='b_aap')
        >>> print(pytplot.data_quants['b_aap'].data)
    """
    # separate and add data

    if 'spec_bins' in pytplot.data_quants[tvar].coords:
        d, s = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar)
    else:
        d = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar, no_spec_bins=True)
        s = None

    time = d.index.copy()
    data1 = d.copy()
    if s is not None:
        data2 = s.copy()
    else:
        data2=None
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

    if data2 is not None:
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

    #pytplot.data_quants[new_tvar].attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)

    return

