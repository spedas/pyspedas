# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import datetime
import numpy as np
from dateutil.parser import parse
import pyspedas
import copy


def convert_tplotxarray_to_pandas_dataframe(name, no_spec_bins=False):
    import pandas as pd
    # This function is not final, and will presumably change in the future
    # This function sums over all dimensions except for the second non-time one.
    # This collapses many dimensions into just a single "energy bin" dimensions

    matrix = pyspedas.tplot_tools.data_quants[name].values
    while len(matrix.shape) > 3:
        matrix = np.nansum(matrix, 3)
    if len(matrix.shape) == 3:
        matrix = np.nansum(matrix, 1)
    return_data = pd.DataFrame(matrix)
    return_data = return_data.set_index(pd.Index(pyspedas.tplot_tools.data_quants[name].coords['time'].values))

    if no_spec_bins:
        return return_data

    if 'spec_bins' in pyspedas.tplot_tools.data_quants[name].coords:
        spec_bins = pd.DataFrame(pyspedas.tplot_tools.data_quants[name].coords['spec_bins'].values)
        if len(pyspedas.tplot_tools.data_quants[name].coords['spec_bins'].shape) == 1:
            spec_bins = spec_bins.transpose()
        else:
            spec_bins = spec_bins.set_index(pd.Index(pyspedas.tplot_tools.data_quants[name].coords['time'].values))

        return return_data, spec_bins

    return return_data
