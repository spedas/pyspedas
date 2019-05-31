# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import pandas as pd
import numpy as np
import datetime

from pytplot import data_quants, TVar
from .del_data import del_data
import pytplot
import xarray as xr

tplot_num = 1


def store_data(name, data=None, delete=False, newname=None):
    
    """
    This function creates a "Tplot Variable" based on the inputs, and
    stores this data in memory.  Tplot Variables store all of the information
    needed to generate a plot.  
    
    Parameters:
        name : str 
            Name of the tplot variable that will be created
        data : dict
            A python dictionary object.  
            
            'x' should be a 1-dimensional array that represents the data's x axis.  Typically this data is time,
            represented in seconds since epoch (January 1st 1970)
            
            'y' should be the data values. This can be 2 dimensions if multiple lines or a spectrogram are desired.
            
            'v' is optional, and is only used for spectrogram plots.  This will be a list of bins to be used.  If this
            is provided, then 'y' should have dimensions of x by z.
            
            'x' and 'y' can be any data format that can be read in by the pandas module.  Python lists, numpy arrays,
            or any pandas data type will all work.
        delete : bool, optional
            Deletes the tplot variable matching the "name" parameter
        newname: str
            Renames TVar to new name
        
    .. note::
        If you want to combine multiple tplot variables into one, simply supply the list of tplot variables to the
        "data" parameter.  This will cause the data to overlay when plotted.
        
    Returns:
        None
        
    Examples:
        >>> # Store a single line
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
    
        >>> # Store a two lines
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [[1,5],[2,4],[3,3],[4,2],[5,1]]
        >>> pytplot.store_data("Variable2", data={'x':x_data, 'y':y_data})
        
        >>> # Store a spectrogram
        >>> x_data = [1,2,3]
        >>> y_data = [ [1,2,3] , [4,5,6], [7,8,9] ]
        >>> v_data = [1,2,3]
        >>> pytplot.store_data("Variable3", data={'x':x_data, 'y':y_data, 'v':v_data})
        
        >>> # Combine two different line plots
        >>> pytplot.store_data("Variable1and2", data=['Variable1', 'Variable2'])
        
        >>> #Rename TVar
        >>> pytplot.store_data('a', data={'x':[0,4,8,12,16], 'y':[1,2,3,4,5]})
        >>> pytplot.store_data('a',newname='f')

    """
    
    global tplot_num
    create_time = datetime.datetime.now()
    
    if delete is True:
        del_data(name)
        return

    if data is None and newname is None:
        print('Please provide data.')
        return
    
    if newname is not None:
        pytplot.tplot_rename(name, newname)
        return
    
    if isinstance(data, list):
        base_data = get_base_tplot_vars(data)
        data_quants[name] = data_quants[base_data[0]]
        data_quants[name].attrs['overplots'] = base_data[1:]
        return
    else:
        data['times'] = data.pop('x')
        values = data['y']
        times = data['times']

        # If given a list of datetime objects, convert times to seconds since epoch.
        if any(isinstance(t, datetime.datetime) for t in times):
            for tt, time in enumerate(times):
                times[tt] = (time-datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds()
        # If given a list of datetime string, convert times to seconds since epoch
        elif any(isinstance(t, str) for t in times):
            for tt, time in enumerate(times):
                times[tt] = pytplot.tplot_utilities.str_to_int(time)

        if len(times) != len(values):
            print("The lengths of x and y do not match!")
            return

        trange = [np.nanmin(times), np.nanmax(times)]

        spec_bins_exist = False
        if 'v' in data or 'v1' in data or 'v2' in data or 'v3' in data:
            # Generally the data is 1D, but occasionally
            # the bins will vary in time.
            spec_bins_exist = True
            if 'v' in data:
                spec_bins = data['v']
            else:
                spec_bins = data['v2']
            
            if type(spec_bins) is not pd.DataFrame:
                spec_bins = pd.DataFrame(spec_bins)
                if len(spec_bins.columns) != 1:
                    # The spec_bins are time varying
                    spec_bins_time_varying = True
                    if len(spec_bins) != len(times):
                        print("Length of v and x do not match.  Cannot create tplot variable.")
                        return 
                else:
                    spec_bins = spec_bins.transpose()
                    spec_bins_time_varying = False
        else:
            spec_bins = None

    # Set up xarray dimension and coordinates
    data_key_list = list(data.keys())
    temp = xr.DataArray(data, dims=data_key_list)
    temp.coords['time'] = ('time', times)
    if spec_bins_exist:
        if spec_bins_time_varying:
            temp.coords['spec_bins'] = (('x', 'y'), spec_bins.values)
        else:
            temp.coords['spec_bins'] = ('y', spec_bins.values)
        for d in data_key_list:
            try:
                temp.coords[d] = (d, data[d])
            except:
                pass

    # Set up Attributes Dictionaries
    xaxis_opt = dict(axis_label='Time')
    yaxis_opt = dict(axis_label=name) if (spec_bins is None) else dict(axis_label='')
    zaxis_opt = dict(axis_label='Z-Axis') if (spec_bins is None) else dict(axis_label=name)
    xaxis_opt['crosshair'] = 'X'
    yaxis_opt['crosshair'] = 'Y'
    zaxis_opt['crosshair'] = 'Z'
    xaxis_opt['x_axis_type'] = 'linear'
    yaxis_opt['y_axis_type'] = 'linear'
    zaxis_opt['z_axis_type'] = 'linear'
    line_opt = {}
    time_bar = []
    # Dictionary to keep track of extra details needed for plotting
    #     that aren't actual attributes in Bokeh
    extras = dict(panel_size=1, char_size=10)
    links = {}

    # Add dicts to the xarray attrs
    temp.name = name
    temp.attrs['xaxis_opt'] = xaxis_opt
    temp.attrs['yaxis_opt'] = yaxis_opt
    temp.attrs['zaxis_opt'] = zaxis_opt
    temp.attrs['line_opt'] = line_opt
    temp.attrs['trange'] = trange
    temp.attrs['time_bar'] = time_bar
    temp.attrs['extras'] = extras
    temp.attrs['create_time'] = create_time
    temp.attrs['links'] = links
    temp.attrs['spec_bins_ascending'] = _check_spec_bins_ordering(times, spec_bins)

    data_quants[name] = temp

    data_quants[name].attrs['yaxis_opt']['y_range'] = get_y_range(values, spec_bins)
    
    return


def get_base_tplot_vars(data):
    base_vars = []
    if not isinstance(data, list):
        data = [data]
    for var in data:
        if isinstance(data_quants[var].data, list):
            base_vars += get_base_tplot_vars(data_quants[var].data)
        else:
            base_vars += [var]
    return base_vars


def get_y_range(data, spec_bins):
    # This is for the numpy RuntimeWarning: All-NaN axis encountered
    # with np.nanmin below
    import warnings
    warnings.filterwarnings("error")

    if spec_bins is not None:
        ymin = np.nanmin(spec_bins)
        ymax = np.nanmax(spec_bins)
        return [ymin, ymax]
    else:
        datasets = []
        y_min_list = []
        y_max_list = []
        if isinstance(data, list):
            for oplot_name in data:
                datasets.append(data_quants[oplot_name].data)
        else:
            datasets.append(data)
    
        for dataset in datasets:
            dataset_temp = dataset.replace([np.inf, -np.inf], np.nan)
            try:
                y_min_list.append(np.nanmin(dataset_temp.min(skipna=True).tolist()))
                y_max_list.append(np.nanmax(dataset_temp.max(skipna=True).tolist()))
            except RuntimeWarning:
                y_min_list.append(np.nan)
                y_max_list.append(np.nan)
        
        y_min = min(y_min_list)
        y_max = max(y_max_list)
        
        if y_min == y_max:
            # Show 10% and 10% below the straight line
            y_min = y_min-(.1*np.abs(y_min))
            y_max = y_max+(.1*np.abs(y_max))
        warnings.resetwarnings()
        return [y_min, y_max]


def _check_spec_bins_ordering(times, spec_bins):
    """
    This is a private function, this is run during
    object creation to check if spec_bins are ascending or descending
    """
    if spec_bins is None:
        return
    if len(spec_bins) == len(times):
        break_top_loop = False
        for index, row in spec_bins.iterrows():
            if row.isnull().values.all():
                continue
            else:
                for i in row.index:
                    if np.isfinite(row[i]) and np.isfinite(row[i + 1]):
                        ascending = row[i] < row[i + 1]
                        break_top_loop = True
                        break
                    else:
                        continue
                if break_top_loop:
                    break
    else:
        ascending = spec_bins[0].iloc[0] < spec_bins[1].iloc[0]
    return ascending