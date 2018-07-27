# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot
import pydivide
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import pandas as pd

#ADD ACROSS COLUMNS
#add tvar data across columns, store in new_tvar
def add_across(tvar1,new_tvar):
    #separate and add data
    time = pytplot.data_quants[tvar1].data.index
    data1 = pytplot.data_quants[tvar1].data
    data = data1.sum(axis=1)
    #store added data
    pytplot.store_data(new_tvar,data={'x':time, 'y':data})
    return new_tvar