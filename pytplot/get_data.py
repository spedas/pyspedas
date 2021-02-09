# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pytplot
from collections import namedtuple

def get_data(name, xarray=False, metadata=False):
    """
    This function extracts the data from the tplot Variables stored in memory.
    
    Parameters:
        name : str 
            Name of the tplot variable
        xarray : bool
            Keep the variable as an xarray object
        metadata : bool
            Return the metadata of the object (the attr dictionary) instead of the actual data

         
    Returns: tuple of data/dimensions/metadata stored in pytplot
        time_val : numpy array of seconds since 1970
        data_val : n-dimensional array of data
        spec_bins_val (if exists) : spectral bins if the plot is a spectrogram
        v1_val (if exists) : numpy array of v1 dimension coordinates
        v2_val {if exists} : numpy array of v2 dimension coordinates
        v3_val (if exists) : numpy array of v3 dimension coordinates

            
    Examples:
        >>> # Retrieve the data from Variable 1
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> time, data = pytplot.get_data("Variable1")

    """

    if name not in pytplot.data_quants.keys():
        print("That name is currently not in pytplot")
        return
    
    temp_data_quant = pytplot.data_quants[name]

    if isinstance(temp_data_quant, dict):
        # non-record varying variables are stored as dicts
        return temp_data_quant['data']

    if xarray:
        return temp_data_quant

    if metadata:
        return temp_data_quant.attrs

    if 'v1' in temp_data_quant.coords.keys() and 'v2' in temp_data_quant.coords.keys() and 'v3' in temp_data_quant.coords.keys():
        variable = namedtuple('variable', ['times', 'y', 'v1', 'v2', 'v3'])
        return variable(temp_data_quant.time.values, temp_data_quant.data, temp_data_quant.coords['v1'].values, temp_data_quant.coords['v2'].values, temp_data_quant.coords['v3'].values)
    elif 'v1' in temp_data_quant.coords.keys() and 'v2' in temp_data_quant.coords.keys():
        variable = namedtuple('variable', ['times', 'y', 'v1', 'v2'])
        return variable(temp_data_quant.time.values, temp_data_quant.data, temp_data_quant.coords['v1'].values, temp_data_quant.coords['v2'].values)
    elif 'v1' in temp_data_quant.coords.keys():
        variable = namedtuple('variable', ['times', 'y', 'v1'])
        return variable(temp_data_quant.time.values, temp_data_quant.data, temp_data_quant.coords['v1'].values)
    elif 'v' in temp_data_quant.coords.keys():
        variable = namedtuple('variable', ['times', 'y', 'v'])
        return variable(temp_data_quant.time.values, temp_data_quant.data, temp_data_quant.coords['v'].values)
    elif 'spec_bins' in temp_data_quant.coords.keys():
        variable = namedtuple('variable', ['times', 'y', 'v'])
        return variable(temp_data_quant.time.values, temp_data_quant.data, temp_data_quant.coords['spec_bins'].values)
    variable = namedtuple('variable', ['times', 'y'])

    return variable(temp_data_quant.time.values, temp_data_quant.data)
