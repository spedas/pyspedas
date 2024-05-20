# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot
import numpy as np
import pytplot
from collections import namedtuple
import logging
from astropy import units as u


def get_data(name, xarray=False, metadata=False, dt=False, units=False, data_quant_in=None):
    """
    This function extracts the data from the tplot Variables stored in memory.
    
    Parameters
    ----------
        name : str 
            Name of the tplot variable
        xarray : bool, optional
            Keep the variable as an xarray object
        metadata : bool, optional
            Return the metadata of the object (the attr dictionary) instead of the actual data
        dt: bool, optional
            Return the times as np.datetime64[ns] objects instead of unix times
            (significantly faster)
        units: bool, optional
            Attach the astropy units to the data and dependencioes prior to returning
         
    Returns
    --------
    times: ndarray[float]
        numpy array of seconds since 1970
    y: ndarray
        n-dimensional numpy array of the data values
    v: ndarray
        If exists, an array of bin values for 1-D data types
    spec_bins: ndarray
        If exists, an array of the spectrogram bins for the bin values
    v1: ndarray
        If exists, numpy array of the v1 dimension coordinates
    v2: ndarray
        If exists, numpy array of the v2 dimension coordinates
    v3: ndarray
        If exists, numpy array of the v3 dimension coordinates



    Notes:
    ------

    If metadata==True, the return value is a dict containing variable attributes and plot options.
    Otherwise, the return value is a named tuple with the fields described above.

    Examples
    --------
        >>> # Retrieve the data from Variable 1
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> time, data = pytplot.get_data("Variable1")
        >>> metadata = pytplot.get_data("Variable1", metadata=True)

    """

    #check for an input data_quant object
    if data_quant_in is not None:
        temp_data_quant = data_quant_in
    else:
        if name not in pytplot.data_quants.keys():
            logging.info("The name " + str(name) + " is currently not in pytplot")
            return
    
        temp_data_quant = pytplot.data_quants[name]

    if isinstance(temp_data_quant, dict):
        # non-record varying variables are stored as dicts
        return temp_data_quant['data']

    if xarray:
        return temp_data_quant

    if metadata:
        return temp_data_quant.attrs

    error = temp_data_quant.attrs['plot_options']['error']

    if not dt:
        times = np.int64(temp_data_quant.time.values)/1e9
        #times = np.array([int(time)/1e9 for time in temp_data_quant.time.values])
        #times = np.array([(time - np.datetime64('1970-01-01T00:00:00'))/np.timedelta64(1, 's') for time in temp_data_quant.time.values])
    else:
        times = temp_data_quant.time.values

    coord_names = temp_data_quant.coords.keys()
    data_values = temp_data_quant.data
    v1_values = None
    v2_values = None
    v3_values = None

    data_att_set = 'data_att' in temp_data_quant.attrs

    if 'v' in coord_names:
        v1_values = temp_data_quant.coords['v'].values
    if 'spec_bins' in coord_names:
        v1_values = temp_data_quant.coords['spec_bins'].values
    if 'v1' in coord_names:
        v1_values = temp_data_quant.coords['v1'].values
    if 'v2' in coord_names:
        v2_values = temp_data_quant.coords['v2'].values
    if 'v3' in coord_names:
        v3_values = temp_data_quant.coords['v3'].values

    if data_att_set and units:
        data_units = temp_data_quant.attrs['data_att'].get('units')
        v1_units = temp_data_quant.attrs['data_att'].get('depend_1_units')
        v2_units = temp_data_quant.attrs['data_att'].get('depend_2_units')
        v3_units = temp_data_quant.attrs['data_att'].get('depend_3_units')

        try:
            if data_units is not None:
                data_values = data_values * u.Unit(data_units)
            if v1_values is not None and v1_units is not None:
                v1_values = v1_values * u.Unit(v1_units)
            if v2_values is not None and v2_units is not None:
                v2_values = v2_values * u.Unit(v2_units)
            if v3_values is not None and v3_units is not None:
                v3_values = v3_values * u.Unit(v3_units)
        except ValueError:
            # occurs when there's a problem converting the units string
            # to astropy units
            pass

    if 'v1' in coord_names and 'v2' in coord_names and 'v3' in coord_names:
        variable = namedtuple('variable', ['times', 'y', 'v1', 'v2', 'v3'])
        return variable(times, data_values, v1_values, v2_values, v3_values)
    elif 'v1' in coord_names and 'v2' in coord_names:
        variable = namedtuple('variable', ['times', 'y', 'v1', 'v2'])
        return variable(times, data_values, v1_values, v2_values)
    elif 'v1' in coord_names:
        variable = namedtuple('variable', ['times', 'y', 'v1'])
        return variable(times, data_values, v1_values)
    elif 'v' in coord_names:
        variable = namedtuple('variable', ['times', 'y', 'v'])
        return variable(times, data_values, v1_values)
    elif 'spec_bins' in coord_names:
        variable = namedtuple('variable', ['times', 'y', 'v'])
        return variable(times, data_values, v1_values)

    if error is not None:
        variable = namedtuple('variable', ['times', 'y', 'dy'])
        return variable(times, data_values, error)
    else:
        variable = namedtuple('variable', ['times', 'y'])
        return variable(times, data_values)


def get(name, xarray=False, metadata=False, dt=True, units=True):
    """
    This function extracts the data from the tplot Variables stored in memory.

    Parameters:
        name : str
            Name of the tplot variable
        xarray : bool
            Keep the variable as an xarray object
        metadata : bool
            Return the metadata of the object (the attr dictionary) instead of the actual data
        dt : bool
            Return the times as np.datetime64[ns] objects instead of unix times
            (significantly faster); defaults to True for pytplot.get
        units: bool
            Attach the astropy units to the data and dependencioes prior to returning
            defaults to True for pytplot.get

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
        >>> pytplot.store("Variable1", data={'x':x_data, 'y':y_data})
        >>> time, data = pytplot.get("Variable1")

    """
    return get_data(name, xarray=xarray, metadata=metadata, dt=dt, units=units)
