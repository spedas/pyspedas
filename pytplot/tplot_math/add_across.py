# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot

#ADD ACROSS COLUMNS
#add tvar data across columns, store in new_tvar
def add_across(tvar1,new_tvar=None):
    #separate and add data
    if new_tvar is None:
        new_tvar=tvar1+"_summed"
    if 'spec_bins' in pytplot.data_quants.coords:
        d,_ = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar1)
    else:
        d = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar1)

    time = d.index.copy()
    data1 = d.values.copy()
    data = data1.sum(axis=1)
    #store added data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return