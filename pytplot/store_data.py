from __future__ import division
import datetime
import pandas as pd
import numpy as np
from . import tplot_common
from .del_data import del_data

def store_data(name, data=None, delete=False):
    global tplot_num
    create_time = datetime.datetime.now()
    
    if delete is True:
        del_data(name)
        return

    if data is None:
        print('Please provide data.')
        return
            
    df = pd.DataFrame(data['y'])
    if 'v' in data:
        spec_bins = data['v']
        df.columns = spec_bins.copy()
        spec_bins.sort()
        df = df.sort_index(axis=1)
    else:
        spec_bins = None
        
    times = data['x']
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
    tag_names = ['name', 'data', 'spec_bins', 'yaxis_opt', 'zaxis_opt', 'line_opt',
                 'trange','dtype','create_time', 'time_bar', 'extras', 'number']
    data_tags = [name, df, spec_bins, yaxis_opt, zaxis_opt, line_opt,
                 trange, dtype, create_time, time_bar, extras, tplot_common.tplot_num]
    # return a dictionary made from tag_names and data_tags
    temp = ( dict( zip( tag_names, data_tags ) ) )
    
    tplot_common.data_quants[name] = temp
    tplot_common.data_quants[tplot_common.tplot_num] = temp
        
    tplot_common.tplot_num += 1
    
    return