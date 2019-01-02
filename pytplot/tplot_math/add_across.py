# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot

#ADD ACROSS COLUMNS
#add tvar data across columns, store in new_tvar
def add_across(tvar1,new_tvar='tvar_aa'):
    #separate and add data
    time = pytplot.data_quants[tvar1].data.index.copy()
    data1 = pytplot.data_quants[tvar1].data.copy()
    data = data1.sum(axis=1)
    #store added data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar