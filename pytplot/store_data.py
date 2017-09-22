# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import datetime
import pandas as pd
import numpy as np
from . import tplot_common
from .del_data import del_data

tplot_num = 1

def store_data(name, data=None, delete=False):
    
    """
    This function creates a "Tplot Variable" based on the inputs, and
    stores this data in memory.  Tplot Variables store all of the information
    needed to generate a plot.  
    
    Parameters:
        name : str 
            Name of the tplot variable that will be created
        data : dict
            A python dictionary object.  
            
            'x' should be a 1-dimensional array that represents the data's x axis.  Typically this data is time, represented in seconds since epoch (January 1st 1970)
            
            'y' should be the data values. This can be 2 dimensions if multiple lines or a spectrogram are desired.
            
            'v' is optional, and is only used for spectrogram plots.  This will be a list of bins to be used.  If this is provided, then 'y' should have dimensions of x by z. 
            
            'x' and 'y' can be any data format that can be read in by the pandas module.  Python lists, numpy arrays, or any pandas data type will all work.   
        delete : bool, optional
            Deletes the tplot variable matching the "name" parameter
        
    .. note::
        If you want to combine multiple tplot variables into one, simply supply the list of tplot variables to the "data" parameter.  This will cause the data to overlay when plotted. 
        
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
        
        >>> # Store a specrogram
        >>> x_data = [1,2,3]
        >>> y_data = [ [1,2,3] , [4,5,6], [7,8,9] ]
        >>> v_data = [1,2,3]
        >>> pytplot.store_data("Variable3", data={'x':x_data, 'y':y_data, 'v':v_data})
        
        >>> # Combine two different line plots
        >>> pytplot.store_data("Variable1and2", data=['Variable1', 'Variable2'])

    """
    
    global tplot_num
    create_time = datetime.datetime.now()
    
    if delete is True:
        del_data(name)
        return

    if data is None:
        print('Please provide data.')
        return
    
    if isinstance(data, list):
        base_data = get_base_tplot_vars(data)
        #Use first tplot var as the time range
        trange = [np.nanmin(tplot_common.data_quants[base_data[0]].data.index), 
                  np.nanmax(tplot_common.data_quants[base_data[0]].data.index)]
        df = base_data
        spec_bins=None
    else:             
        df = pd.DataFrame(data['y'])
        if 'v' in data:
            spec_bins = data['v']
            df.columns = spec_bins.copy()
            spec_bins.sort()
            df = df.sort_index(axis=1)
        else:
            spec_bins = None
            
        times = data['x']
        if len(times) != len(df.index):
            if len(times[0]) == len(df.index):
                df = df.set_index(data['x'])
            else:
                print("The lengths of x and y do not match!")
                return
        elif isinstance(times, pd.Series):
            df = df.set_index(data['x'])
        else:
            df['Index'] = times
            df = df.set_index('Index', drop=True)
        trange = [np.nanmin(times), np.nanmax(times)]
        
    yaxis_opt = dict(axis_label = name)
    zaxis_opt = {}
    line_opt = {}
    dtype=''
    time_bar = []
    # Dictionary to keep track of extra details needed for plotting
    #     that aren't actual attributes in Bokeh
    extras = dict(panel_size = 1)
    
    temp = tplot_common.TVar(name, tplot_num, df, spec_bins, yaxis_opt, zaxis_opt, line_opt,
                trange, dtype, create_time, time_bar, extras)
    
    tplot_common.data_quants[name] = temp
    tplot_common.data_quants[name].yaxis_opt['y_range'] = get_y_range(df, spec_bins)
    
    return

def get_base_tplot_vars(data):
    base_vars = []
    if not isinstance(data, list):
        data = [data]
    for var in data:
        if isinstance(tplot_common.data_quants[var].data, list):
            base_vars += get_base_tplot_vars(tplot_common.data_quants[var].data)
        else:
            base_vars += [var]
    return base_vars

def get_y_range(data, spec_bins):
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
                datasets.append(tplot_common.data_quants[oplot_name].data)
        else:
            datasets.append(data)
    
        for dataset in datasets:
            dataset_temp = dataset.replace([np.inf, -np.inf], np.nan)
            y_min_list.append(np.nanmin(dataset_temp.min(skipna=True).tolist()))
            y_max_list.append(np.nanmax(dataset_temp.max(skipna=True).tolist()))
        y_min = min(y_min_list)
        y_max = max(y_max_list)
        
        if y_min==y_max:
            y_min = y_min-(.1*np.abs(y_min))
            y_max = y_max+(.1*np.abs(y_max))
            
        return [y_min, y_max]
    
