# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import os
import datetime
import pickle
import math
import pandas as pd
import numpy as np
import pytz
from _collections import OrderedDict
from . import data_quants
import pytplot

def compare_versions():
    #import libraries
    import requests

    #access complete list of revision numbers on PyPI 
    pytplot_url = "https://pypi.python.org/pypi/pytplot/json"
    try:
        pt_pypi_vn = sorted(requests.get(pytplot_url).json()['releases'])
    except:
        return
    
    #find PyPI version number
    pt_pypi_vn = pt_pypi_vn[-1]
    pr1 = pt_pypi_vn
    pt_pypi_vn = pt_pypi_vn.split(".")
    #convert to integer array for comparison
    pt_pypi_vn = [int(i) for i in pt_pypi_vn]
    
    #find current directory out of which code is executing
    dir_path = os.path.dirname(os.path.realpath(__file__))
    version_path = dir_path + '/version.txt'
    #open version.txt in current directory and read
    with open(version_path) as f:
        cur_vn = f.readline()
    cur_vn = "".join(cur_vn)
    pr2 = cur_vn
    cur_vn = cur_vn.split(".")
    #convert to integer array for comparison
    cur_vn = [int(i) for i in cur_vn]

    #for each item in version number array [X.Y.Z]
    for i in range(len(cur_vn)):
        #if current item > PyPI item (hypothetical), break, latest version is running
        if cur_vn[i] > pt_pypi_vn[i]:
            old_flag = 0
            break
        #if current item = PyPI item, continue to check next item
        elif cur_vn[i] == pt_pypi_vn[i]:
            old_flag = 0
            continue
        #if current item < PyPI item, indicative of old version, throw flag to initiate warning
        else:
            old_flag = 1
            break

    #if not running latest version, throw warning
    if old_flag == 1:
        print("PyPI PyTplot Version")
        print(pr1)
        print("Your PyTplot Version in " + dir_path)
        print(pr2)
        print("")
        print('****************************** WARNING! ******************************')
        print('*                                                                    *')
        print('*          You are running an outdated version of PyTplot.           *')
        print('*              Sync your module for the latest updates.              *')
        print('*                                                                    *')
        print('****************************** WARNING! ******************************')
    return 
        
def option_usage():
    print("options 'tplot variable name' 'plot option' value[s]")
    return

def set_tplot_options(option, value, old_tplot_opt_glob):
    new_tplot_opt_glob = old_tplot_opt_glob
    
    if option == 'title':
        new_tplot_opt_glob['title_text'] = value
    
    elif option == 'title_size':
        str_size = str(value) + 'pt'
        new_tplot_opt_glob['title_size'] = str_size
        
    elif option == 'wsize':
        new_tplot_opt_glob['window_size'] = value
        
    elif option == 'title_align':
        new_tplot_opt_glob['title_align'] = value
        
    elif option == 'var_label':
        new_tplot_opt_glob['var_label'] = value
        
    elif option == 'alt_range':
        new_tplot_opt_glob['alt_range'] = value
    
    return (new_tplot_opt_glob)

def str_to_int(time_str):
    epoch_t = "1970-1-1 00:00:00"
    pattern = "%Y-%m-%d %H:%M:%S"
    epoch_t1 = datetime.datetime.strptime(epoch_t, pattern)
    time_str1 = datetime.datetime.strptime(time_str, pattern)
    time_int = int((time_str1-epoch_t1).total_seconds())
    return time_int

def int_to_str(time_int):
    if math.isnan(time_int):
        return "NaN"
    else:
        return datetime.datetime.fromtimestamp(int(round(time_int)), tz=pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")

def return_bokeh_colormap(name):
    import matplotlib as mpl
    #mpl.use('tkagg')
    from matplotlib import cm
    
    if name=='yellow':
        map = [rgb_to_hex(tuple((np.array([1,1,0,1])*255).astype(np.int))) for x in range(0,256)]
        return map
    elif name=='red':
        map = [rgb_to_hex(tuple((np.array([1,0,0,1])*255).astype(np.int))) for x in range(0,256)]
        return map
    elif name=='blue':
        map = [rgb_to_hex(tuple((np.array([0,0,1,1])*255).astype(np.int))) for x in range(0,256)]
        return map
    elif name=='green':
        map = [rgb_to_hex(tuple((np.array([0,1,0,1])*255).astype(np.int))) for x in range(0,256)]
        return map
    elif name=='purple':
        map = [rgb_to_hex(tuple((np.array([1,0,1,1])*255).astype(np.int))) for x in range(0,256)]
        return map
    elif name=='teal':
        map = [rgb_to_hex(tuple((np.array([0,1,1,1])*255).astype(np.int))) for x in range(0,256)]
        return map
    else:
        cm = mpl.cm.get_cmap(name)
        map = [rgb_to_hex(tuple((np.array(cm(x))*255).astype(np.int))) for x in range(0,cm.N)]
        return map

def rgb_to_hex(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    return '#%02x%02x%02x' % (red, green, blue)

def get_heatmap_color(color_map, min_val, max_val, values, zscale = 'log'):
    colors = []
    if not isinstance(values, list):
        values = [values]
    for value in values:
        if np.isfinite(value):
            if value > max_val:
                value = max_val
            if value < min_val:
                colors.append("#%02x%02x%02x" % (255, 255, 255))
                continue
            if zscale=='log':
                log_min=np.log10(min_val)
                log_max=np.log10(max_val)
                log_val=np.log10(value)
                if np.isfinite(np.log10(value)):
                    cm_index = int((((log_val-log_min) / (log_max-log_min)) * (len(color_map)-1)))
                    colors.append(color_map[cm_index])
                else:
                    colors.append(("#%02x%02x%02x" % (255, 255, 255)))
            else:
                cm_index = int((((value-min_val) / (max_val-min_val)) * (len(color_map)-1)))
                colors.append(color_map[cm_index])
        else:
            colors.append("#%02x%02x%02x" % (255, 255, 255))
    return colors
    
def timebar_delete(t, varname=None, dim='height'):
    if varname is None:
        for name in pytplot.data_quants:
            list_timebars = pytplot.data_quants[name].time_bar
            elem_to_delete = []
            for elem in list_timebars:
                for num in t:
                    if (elem.location == num) and (elem.dimension == dim):
                        elem_to_delete.append(elem)
            for i in elem_to_delete:
                list_timebars.remove(i)
            pytplot.data_quants[name].time_bar = list_timebars
    else:
        if not isinstance(varname, list):
            varname = [varname]
        for i in varname:
            if i not in pytplot.data_quants.keys():
                print(str(i) + " is currently not in pytplot.")
                return
            list_timebars = pytplot.data_quants[i].time_bar
            elem_to_delete = []
            for elem in list_timebars:
                for num in t:
                    if (elem.location == num) and (elem.dimension == dim):
                        elem_to_delete.append(elem)
            for j in elem_to_delete:
                list_timebars.remove(j)
            pytplot.data_quants[i].time_bar = list_timebars
    return    

def return_lut(name):
    import matplotlib as mpl
    mpl.use('tkagg')
    from matplotlib import cm
    
    if name=='yellow':
        map = [(np.array([1,1,0,1])*255).astype(np.int) for x in range(0,256)]
        return map
    elif name=='red':
        map = [(np.array([1,0,0,1])*255).astype(np.int) for x in range(0,256)]
        return map
    elif name=='blue':
        map = [(np.array([0,0,1,1])*255).astype(np.int) for x in range(0,256)]
        return map
    elif name=='green':
        map = [(np.array([0,1,0,1])*255).astype(np.int) for x in range(0,256)]
        return map
    elif name=='purple':
        map = [(np.array([1,0,1,1])*255).astype(np.int) for x in range(0,256)]
        return map
    elif name=='teal':
        map = [(np.array([0,1,1,1])*255).astype(np.int) for x in range(0,256)]
        return map
    else:
        cm = mpl.cm.get_cmap(name)
        map = [(np.array(cm(x))*255).astype(np.int) for x in range(0,cm.N)]
        return map
    
def get_available_qt_window():
    #Delete old windows
    for w in pytplot.pytplotWindows:
        if not w.isVisible():
            del w
            
    #Add a new one to the list
    pytplot.pytplotWindows.append(pytplot.PlotWindow())
    
    #Return the latest window
    return pytplot.pytplotWindows[-1]