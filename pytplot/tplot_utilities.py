# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import os
import datetime
import math
import numpy as np
import pytz
from dateutil.parser import parse
import pytplot
from platform import system
import copy
from . import spedas_colorbar

def compare_versions():
    # import libraries
    import requests

    # access complete list of revision numbers on PyPI
    pytplot_url = "https://pypi.python.org/pypi/pytplot/json"
    try:
        pt_pypi_vn = sorted(requests.get(pytplot_url).json()['releases'])
    except:
        return
    
    # find PyPI version number
    pt_pypi_vn = pt_pypi_vn[-1]
    pr1 = pt_pypi_vn
    pt_pypi_vn = pt_pypi_vn.split(".")
    # convert to integer array for comparison
    pt_pypi_vn = [int(i) for i in pt_pypi_vn]
    
    # find current directory out of which code is executing
    dir_path = os.path.dirname(os.path.realpath(__file__))
    version_path = dir_path + '/version.txt'
    # open version.txt in current directory and read
    with open(version_path) as f:
        cur_vn = f.readline()
    cur_vn = "".join(cur_vn)
    pr2 = cur_vn
    cur_vn = cur_vn.split(".")
    # convert to integer array for comparison
    cur_vn = [int(i) for i in cur_vn]

    # for each item in version number array [X.Y.Z]
    for i in range(len(cur_vn)):
        # if current item > PyPI item (hypothetical), break, latest version is running
        if cur_vn[i] > pt_pypi_vn[i]:
            old_flag = 0
            break
        # if current item = PyPI item, continue to check next item
        elif cur_vn[i] == pt_pypi_vn[i]:
            old_flag = 0
            continue
        # if current item < PyPI item, indicative of old version, throw flag to initiate warning
        else:
            old_flag = 1
            break

    # if not running latest version, throw warning
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

    elif option == 'map_x_range':
        new_tplot_opt_glob['map_x_range'] = value

    elif option == 'map_y_range':
        new_tplot_opt_glob['map_y_range'] = value

    elif option == 'x_range':
        new_tplot_opt_glob['x_range'] = value

    elif option == 'crosshair':
        new_tplot_opt_glob['crosshair'] = value

    elif option == 'data_gap':
        new_tplot_opt_glob['data_gap'] = value
    
    elif option == 'roi':
        new_tplot_opt_glob['roi_lines'] = value

    elif option == 'vertical_spacing':
        new_tplot_opt_glob['vertical_spacing'] = value

    elif option == 'show_all_axes':
        new_tplot_opt_glob['show_all_axes'] = value

    elif option == 'min_border_top':
        new_tplot_opt_glob['min_border_top'] = value

    elif option == 'min_border_bottom':
        new_tplot_opt_glob['min_border_bottom'] = value

    elif option == 'black_background':
        new_tplot_opt_glob['black_background'] = value

    elif option == 'axis_font_size':
        new_tplot_opt_glob['axis_font_size'] = value

    elif option == 'axis_tick_num':
        new_tplot_opt_glob['axis_tick_num'] = value

    elif option == 'yaxis_width':
        new_tplot_opt_glob['yaxis_width'] = value

    elif option == 'y_axis_zoom':
        new_tplot_opt_glob['y_axis_zoom'] = value

    elif option == 'xmargin':
        new_tplot_opt_glob['xmargin'] = value

    elif option == 'ymargin':
        new_tplot_opt_glob['ymargin'] = value

    elif option == 'style':
        new_tplot_opt_glob['style'] = value

    elif option == 'charsize':
        new_tplot_opt_glob['charsize'] = value

    elif option == 'xsize':
        new_tplot_opt_glob['xsize'] = value

    elif option == 'ysize':
        new_tplot_opt_glob['ysize'] = value

    else:
        print("Unknown option supplied: " + str(option))

    return new_tplot_opt_glob


def str_to_int_fuzzy(time_str):
    """
    Implementation of str_to_int (below) that uses dateutil and .timestamp()
    to convert the date/time string to integer (number of seconds since Jan 1, 1970)

    This function is slower than str_to_int, but more flexible
    """
    dt_object = parse(time_str)
    return int(int(dt_object.replace(tzinfo=datetime.timezone.utc).timestamp()))


def str_to_int(time_str):
    epoch_t = "1970-1-1 00:00:00"
    if 'T' in time_str:
        pattern = "%Y-%m-%dT%H:%M:%S"
        epoch_t = "1970-1-1T00:00:00"
    else:
        pattern = "%Y-%m-%d %H:%M:%S"
        epoch_t = "1970-1-1 00:00:00"
    epoch_t1 = datetime.datetime.strptime(epoch_t, pattern)
    time_str1 = datetime.datetime.strptime(time_str, pattern)
    time_int = int((time_str1-epoch_t1).total_seconds())
    return time_int


def int_to_str(time_int):
    if math.isnan(time_int):
        return "NaN"
    else:
        try:
            return datetime.datetime.fromtimestamp(int(round(time_int)), tz=pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
        except:
            return "NaN"


def return_bokeh_colormap(name):
    import matplotlib as mpl
    from matplotlib import cm
   
    # This currently gives mac users a headache, so not bothering with it if on a mac 
    if system() != 'Darwin':
        try:
            mpl.use('tkagg')
        except:
            pass
    
    if name == 'yellow':
        map = [rgb_to_hex(tuple((np.array([1, 1, 0, 1])*255).astype(np.int))) for x in range(0, 256)]
        return map
    elif name == 'red':
        map = [rgb_to_hex(tuple((np.array([1, 0, 0, 1])*255).astype(np.int))) for x in range(0, 256)]
        return map
    elif name == 'blue':
        map = [rgb_to_hex(tuple((np.array([0, 0, 1, 1])*255).astype(np.int))) for x in range(0, 256)]
        return map
    elif name == 'green':
        map = [rgb_to_hex(tuple((np.array([0, 1, 0, 1])*255).astype(np.int))) for x in range(0, 256)]
        return map
    elif name == 'purple':
        map = [rgb_to_hex(tuple((np.array([1, 0, 1, 1])*255).astype(np.int))) for x in range(0, 256)]
        return map
    elif name == 'teal':
        map = [rgb_to_hex(tuple((np.array([0, 1, 1, 1])*255).astype(np.int))) for x in range(0, 256)]
        return map
    else:
        cm = mpl.cm.get_cmap(name)
        map = [rgb_to_hex(tuple((np.array(cm(x))*255).astype(np.int))) for x in range(0, cm.N)]
        return map


def rgb_to_hex(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    return '#%02x%02x%02x' % (red, green, blue)


def get_heatmap_color(color_map, min_val, max_val, values, zscale='log'):
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
            if zscale == 'log':
                log_min = np.log10(min_val)
                log_max = np.log10(max_val)
                log_val = np.log10(value)
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
            if isinstance(pytplot.data_quants[name], dict):
                # non-record varying variable
                continue
            try:
                list_timebars = pytplot.data_quants[name].attrs['plot_options']['time_bar']
            except KeyError:
                continue
            elem_to_delete = []
            for elem in list_timebars:
                for num in t:
                    if (elem['location'] == num) and (elem['dimension'] == dim):
                        elem_to_delete.append(elem)
            for i in elem_to_delete:
                list_timebars.remove(i)
            pytplot.data_quants[name].attrs['plot_options']['time_bar'] = list_timebars
    else:
        if not isinstance(varname, list):
            varname = [varname]
        for i in varname:
            if i not in pytplot.data_quants.keys():
                print(str(i) + " is currently not in pytplot.")
                return
            if isinstance(pytplot.data_quants[i], dict):
                # non-record varying variable
                continue
            try:
                list_timebars = pytplot.data_quants[i].attrs['plot_options']['time_bar']
            except KeyError:
                continue
            elem_to_delete = []
            for elem in list_timebars:
                for num in t:
                    if (elem['location'] == num) and (elem['dimension'] == dim):
                        elem_to_delete.append(elem)
            for j in elem_to_delete:
                list_timebars.remove(j)
            # pytplot.data_quants[i].attrs['plot_options']['time_bar']
    return


def return_lut(name):
    import matplotlib as mpl
    from matplotlib import cm	    
    
    # This currently gives mac users a headache, so not bothering with it if on a mac
    if system() != 'Darwin':
        try:
            mpl.use('tkagg')
        except:
            pass

    if name == 'yellow':
        map = [(np.array([1, 1, 0, 1])*255).astype(np.int) for x in range(0, 256)]
        return map
    elif name == 'red':
        map = [(np.array([1, 0, 0, 1])*255).astype(np.int) for x in range(0, 256)]
        return map
    elif name == 'blue':
        map = [(np.array([0, 0, 1, 1])*255).astype(np.int) for x in range(0, 256)]
        return map
    elif name == 'green':
        map = [(np.array([0, 1, 0, 1])*255).astype(np.int) for x in range(0, 256)]
        return map
    elif name == 'purple':
        map = [(np.array([1, 0, 1, 1])*255).astype(np.int) for x in range(0, 256)]
        return map
    elif name == 'teal':
        map = [(np.array([0, 1, 1, 1])*255).astype(np.int) for x in range(0, 256)]
        return map
    elif name == 'spedas':
        map = [(np.array([r, g, b, 255])).astype(np.int) for r, g, b in zip(spedas_colorbar.r, spedas_colorbar.g, spedas_colorbar.b)]
        return map
    else:
        cm = mpl.cm.get_cmap(name)
        map = [(np.array(cm(x))*255).astype(np.int) for x in range(0, cm.N)]
        return map


def get_available_qt_window(name='Plot'):
    # Delete old windows
    for n, w in zip(pytplot.pytplotWindow_names, pytplot.pytplotWindows):
        if not w.isVisible():
            del w
            del n

    # Add a new one to the list
    pytplot.pytplotWindows.append(pytplot.PlotWindow())
    pytplot.pytplotWindow_names.append(name)

    # Return the latest window
    return pytplot.pytplotWindows[-1]


def rgb_color(color):

    color_opt = {
                'indianred': (205, 92, 92),
                'lightcoral': (240, 128, 128),
                'salmon': (250, 128, 114),
                'darksalmon': (233, 150, 122),
                'lightsalmon': (255, 160, 122),
                'crimson': (220, 20, 60),
                'red': (255, 0, 0),
                'firebrick': (178, 34, 34),
                'darkred': (139, 0, 0),
                
                'pink': (255, 192, 203),
                'lightpink': (255, 182, 193),
                'hotpink': (255, 105, 180),
                'deeppink': (255, 20, 147),
                'mediumvioletred': (199, 21, 133),
                'palevioletred': (219, 112, 147),
                
                'tomato': (255, 99, 71),
                'orangered': (255, 69, 0),
                'darkorange': (255, 140, 0),
                'orange': (255, 165, 0),
                
                'gold': (155, 215, 0),
                'yellow': (255, 255, 0),
                'lightyellow': (255, 255, 224),
                'lemonchiffon': (255, 250, 205),
                'lightgoldenrodyellow': (250, 250, 210),
                'papayawhip': (255, 239, 213),
                'moccasin': (255, 228, 181),
                'peachpuff': (255, 218, 185),
                'palegoldenrod': (238, 232, 170),
                'khaki': (240, 230, 130),
                'darkkhaki': (189, 183, 107),
                
                'lavender': (230, 230, 250),
                'thistle': (216, 191, 216),
                'plum': (221, 160, 221),
                'violet': (238, 130, 238),
                'orchid': (218, 112, 214),
                'fuchsia': (255, 0, 255),
                'magenta': (255, 0, 255),
                'mediumorchid': (186, 85, 211),
                'mediumpurple': (147, 112, 219),
                'rebeccapurple': (102, 51, 153),
                'blueviolet': (138, 43, 226),
                'darkviolet': (148, 0, 211),
                'darkorchid': (153, 50, 204),
                'darkmagenta': (139, 0, 139),
                'purple': (128, 0, 128),
                'indigo': (75, 0, 130),
                'slateblue': (106, 90, 205),
                'darkslateblue': (72, 61, 139),
                'mediumslateblue': (123, 104, 238),
                
                'greenyellow': (173, 255, 47),
                'chartreuse': (127, 255, 0),
                'lawngreen': (124, 252, 0),
                'lime': (0, 255, 0),
                'limegreen': (50, 205, 50),
                'palegreen': (152, 251, 152),
                'lightgreen': (144, 238, 144),
                'mediumspringgreen': (0, 250, 154),
                'springgreen': (0, 255, 127),
                'mediumseagreen': (60, 179, 113),
                'seagreen': (46, 139, 87),
                'forestgreen': (34, 139, 34),
                'green': (0, 128, 0),
                'darkgreen': (0, 100, 0),
                'yellowgreen': (154, 205, 50),
                'olivedrab': (107, 142, 35),
                'olive': (128, 128, 0),
                'darkolivegreen': (85, 107, 47),
                'mediumaquamarine': (102, 205, 170),
                'darkseagreen': (143, 188, 139),
                'lightseagreen': (32, 178, 170),
                'darkcyan': (0, 139, 139),
                'teal': (0, 128, 128),
                
                'aqua': (0, 255, 255),
                'cyan': (0, 255, 255),
                'lightcyan': (224, 255, 255),
                'paleturquoise': (175, 238, 238),
                'aquamarine': (127, 255, 212),
                'turquoise': (64, 224, 208),
                'mediumturquoise': (72, 209, 204),
                'darkturquoise': (0, 206, 209),
                'cadetblue': (95, 158, 160),
                'steelblue': (70, 130, 180),
                'lightsteelblue': (176, 196, 222),
                'powderblue': (176, 224, 230),
                'lightblue': (173, 216, 23),
                'skyblue': (135, 206, 235),
                'lightskyblue': (135, 206, 250),
                'deepskyblue': (0, 191, 255),
                'dodgerblue': (30, 144, 255),
                'cornflowerblue': (100, 149, 237),
                'royalblue': (65, 105, 225),
                'blue': (0, 0, 255),
                'mediumblue': (0, 0, 205),
                'darkblue': (0, 0, 139),
                'navy': (0, 0, 128),
                'midnightblue': (25, 25, 112),
                
                'cornsilk': (255, 248, 220),
                'blanchedalmond': (255, 235, 205),
                'bisque': (255, 228, 196),
                'navajowhite': (155, 222, 173),
                'wheat': (245, 222, 179),
                'burlywood': (222, 184, 135),
                'tan': (210, 208, 214),
                'rosybrown': (188, 143, 143),
                'sandybrown': (244, 164, 96),
                'goldenrod': (218, 165, 32),
                'darkgoldenrod': (184, 134, 11),
                'peru': (205, 133, 63),
                'chocolate': (210, 105, 30),
                'saddlebrown': (139, 69, 19),
                'sienna': (160, 82, 45),
                'brown': (165, 42, 42),
                'maroon': (128, 0, 0),
                'white': (255, 255, 255),
                'snow': (255, 250, 250),
                'honeydew': (240, 255, 240),
                'mintcream': (245, 255, 250),
                'azure': (240, 255, 255),
                'aliceblue': (240, 248, 255),
                'ghostwhite': (248, 248, 255),
                'whitesmoke': (245, 245, 245),
                'seashell': (255, 245, 238),
                'beige': (245, 245, 220),
                'oldlace': (253, 245, 230),
                'floralwhite': (255, 250, 240),
                'ivory': (255, 255, 240),
                'antiquewhite': (250, 235, 215),
                'linen': (250, 240, 230),
                'lavenderblush': (255, 240, 245),
                'mistyrose': (255, 228, 255),
                
                'gainsboro': (220, 220, 220),
                'lightgray': (211, 211, 211),
                'silver': (192, 192, 192),
                'darkgray': (169, 169, 169),
                'gray': (128, 128, 128),
                'dimgray': (105, 105, 105),
                'lightslategray': (119, 136, 153),
                'slategray': (112, 128, 144),
                'darkslategray': (47, 79, 79),
                'black': (0, 0, 0),
                
                'r': (255, 0, 0),
                'g': (0, 128, 0),
                'b': (0, 0, 255),
                'c': (0, 255, 255),
                'y': (255, 255, 0),
                'm': (255, 0, 255),
                'w': (255, 255, 255),
                'k': (0, 0, 0)
                 }

    if type(color) is not list:
        if type(color) is tuple:
            return [color]
        rgbcolor = [color_opt.get(color, (0,0,0))]
    else:
        if type(color[0]) is tuple:
            return color
        rgbcolor = len(color)*[0]
        for i, val in enumerate(color):
            rgbcolor[i] = color_opt.get(val, (0,0,0))
    return rgbcolor


# The following functions are needed for a spectrogram's interactive, static, or time-averaged (w/ or w/o cursor)
# supplementary plot(s).

def get_spec_data(names):
    # Just grab variables that are spectrograms.
    valid_vars = list()
    for n in names:
        if 'spec_bins' in pytplot.data_quants[n].coords:
            valid_vars.append(n)
    return valid_vars


def get_spec_slicer_axis_types(names):
    # Get labels and axis types for plots.
    plot_labels = {}
    for n in names:
        if 'spec_bins' in pytplot.data_quants[n].coords:
            zlabel = pytplot.data_quants[n].attrs['plot_options']['zaxis_opt']['axis_label']
            ylabel = pytplot.data_quants[n].attrs['plot_options']['yaxis_opt']['axis_label']

            if 'xi_axis_type' in pytplot.data_quants[n].attrs['plot_options']['interactive_xaxis_opt'].keys():
                xtype_interactive = pytplot.data_quants[n].attrs['plot_options']['interactive_xaxis_opt']['xi_axis_type']
            elif 'y_axis_type' in pytplot.data_quants[n].attrs['plot_options']['yaxis_opt']:
                xtype_interactive = pytplot.data_quants[n].attrs['plot_options']['yaxis_opt']['y_axis_type']
            else:
                xtype_interactive = 'log'

            if 'yi_axis_type' in pytplot.data_quants[n].attrs['plot_options']['interactive_yaxis_opt'].keys():
                ytype_interactive = pytplot.data_quants[n].attrs['plot_options']['interactive_yaxis_opt']['yi_axis_type']
            elif 'z_axis_type' in pytplot.data_quants[n].attrs['plot_options']['zaxis_opt']:
                ytype_interactive = pytplot.data_quants[n].attrs['plot_options']['zaxis_opt']['z_axis_type']
            else:
                ytype_interactive = 'log'

            plot_labels[n] = [ylabel, zlabel, xtype_interactive, ytype_interactive]
    return plot_labels


def set_spec_slice_x_range(var, x_axis_log, plot):
    # Check if plot's x range has been set by user. If not, range is automatically set.
    if 'xi_range' in pytplot.data_quants[var].attrs['plot_options']['interactive_xaxis_opt']:
        if x_axis_log:
            plot.setXRange(np.log10(pytplot.data_quants[var].attrs['plot_options']['interactive_xaxis_opt']['xi_range'][0]),
                           np.log10(pytplot.data_quants[var].attrs['plot_options']['interactive_xaxis_opt']['xi_range'][1]),
                           padding=0)
        elif not x_axis_log:
            plot.setXRange(pytplot.data_quants[var].attrs['plot_options']['interactive_xaxis_opt']['xi_range'][0],
                           pytplot.data_quants[var].attrs['plot_options']['interactive_xaxis_opt']['xi_range'][1], padding=0)

def set_spec_slice_y_range(var, y_axis_log, plot):
    # Check if plot's y range has been set by user. If not, range is automatically set.
    if 'yi_range' in pytplot.data_quants[var].attrs['plot_options']['interactive_yaxis_opt']:
        if y_axis_log:
            plot.setYRange(np.log10(pytplot.data_quants[var].attrs['plot_options']['interactive_yaxis_opt']['yi_range'][0]),
                           np.log10(pytplot.data_quants[var].attrs['plot_options']['interactive_yaxis_opt']['yi_range'][1]),
                           padding=0)
        elif not y_axis_log:
            plot.setYRange(pytplot.data_quants[var].attrs['plot_options']['interactive_yaxis_opt']['yi_range'][0],
                           pytplot.data_quants[var].attrs['plot_options']['interactive_yaxis_opt']['yi_range'][1], padding=0)


def convert_tplotxarray_to_pandas_dataframe(name, no_spec_bins=False):
    import pandas as pd
    # This function is not final, and will presumably change in the future
    # This function sums over all dimensions except for the second non-time one.
    # This collapses many dimensions into just a single "energy bin" dimensions

    matrix = pytplot.data_quants[name].values
    while len(matrix.shape) > 3:
        matrix = np.nansum(matrix, 3)
    if len(matrix.shape) == 3:
        matrix = np.nansum(matrix, 1)
    return_data = pd.DataFrame(matrix)
    return_data = return_data.set_index(pd.Index(pytplot.data_quants[name].coords['time'].values))

    if no_spec_bins:
        return return_data

    if 'spec_bins' in pytplot.data_quants[name].coords:
        spec_bins = pd.DataFrame(pytplot.data_quants[name].coords['spec_bins'].values)
        if len(pytplot.data_quants[name].coords['spec_bins'].shape) == 1:
            spec_bins = spec_bins.transpose()
        else:
            spec_bins = spec_bins.set_index(pd.Index(pytplot.data_quants[name].coords['time'].values))

        return return_data, spec_bins

    return return_data


def return_interpolated_link_dict(dataset, types):
    ret_dict = {}
    for t in types:
        if t not in dataset.attrs['plot_options']['links']:
            print(f"ERROR: {t} is not linked to {dataset.name}")
            raise Exception("Not a valid link")

        link = pytplot.data_quants[dataset.attrs['plot_options']['links'][t]]
        new_link = link.interp_like(dataset)
        ret_dict[t] = new_link

    return ret_dict


def get_y_range(dataset):
    # This is for the numpy RuntimeWarning: All-NaN axis encountered
    # with np.nanmin below

    # This takes the data and sets the minimum and maximum range of the data values.
    # If the data type later gets set to 'spec', then we'll change the ymin and ymax
    import warnings
    warnings.filterwarnings("ignore")

    # Special rule if 'spec' is True
    if 'spec' in dataset.attrs['plot_options']['extras']:
        if dataset.attrs['plot_options']['extras']['spec']:
            try:
                ymin = np.nanmin(dataset.coords['spec_bins'].values)
                ymax = np.nanmax(dataset.coords['spec_bins'].values)
                return [ymin, ymax]
            except Exception as e:
                #continue on to the code below
                pass

    dataset_temp = dataset.where(dataset != np.inf)
    dataset_temp = dataset_temp.where(dataset != -np.inf)
    try:
        y_min = np.nanmin(dataset_temp.values)
        y_max = np.nanmax(dataset_temp.values)
    except RuntimeWarning:
        y_min = np.nan
        y_max = np.nan

    # CDF files may have array of strings (e.g., RBSP EMFISIS)
    if isinstance(y_min, str):
        y_min = np.nan
        y_max = np.nan
        
    if y_min == y_max:
        # Show 10% and 10% below the straight line
        y_min = y_min - (.1 * np.abs(y_min))
        y_max = y_max + (.1 * np.abs(y_max))
    warnings.resetwarnings()
    return [y_min, y_max]


def reduce_spec_dataset(tplot_dataset=None, name=None):
    # This function will reduce the data in a 3+ dimensional DataSet object into something that can be plotted with a
    # spectrogram, either by taking slices of the data or by summing the dimensions into this one.
    if tplot_dataset is not None:
        da = copy.deepcopy(tplot_dataset)
    elif name is not None:
        da = copy.deepcopy(pytplot.data_quants[name])
    else:
        return

    coordinate_to_plot = da.attrs['plot_options']['extras']['spec_dim_to_plot']

    dim_to_plot = coordinate_to_plot + '_dim'

    for d in da.dims:
        if d == dim_to_plot:
            pass
        elif d == 'time':
            pass
        else:
            if 'spec_slices_to_use' in da.attrs['plot_options']['extras']:
                for key, value in da.attrs['plot_options']['extras']['spec_slices_to_use'].items():
                    dim = key+"_dim"
                    if dim == d:
                        da=da.isel({dim:value})
                        break
                else:
                    da = da.sum(dim=d, skipna=True, keep_attrs=True)
            else:
                da = da.sum(dim=d, skipna=True, keep_attrs=True)
    return da


def highlight(variables=None, range=None, color='gray', alpha=0.2, fill=True, edgecolor=None, facecolor=None, hatch=None, delete=False):
    """
    This function highlights a time interval on tplot variables
    """
    if not isinstance(variables, list):
        variables = [variables]

    for variable in variables:
        if delete:
            pytplot.data_quants[variable].attrs['plot_options']['highlight_intervals'] = None
            continue
        if range is None:
            pytplot.data_quants[variable].attrs['plot_options']['highlight_intervals'] = None
            continue
        interval = {'location': range,
                    'color': color,
                    'alpha': alpha,
                    'fill': fill,
                    'edgecolor': edgecolor,
                    'facecolor': facecolor,
                    'hatch': hatch}
        if pytplot.data_quants[variable].attrs['plot_options'].get('highlight_intervals') is None:
            pytplot.data_quants[variable].attrs['plot_options']['highlight_intervals'] = [interval]
        else:
            pytplot.data_quants[variable].attrs['plot_options']['highlight_intervals'].append(interval)


def annotate(text=None, position=None,
             xycoords='figure fraction',
             color='black',
             fontfamily=None,
             fontsize='x-large',
             alpha=1,
             fontvariant='normal',
             fontstyle='normal',
             fontstretch='normal',
             fontweight='normal',
             rotation='horizontal',
             delete=False):
    """
    This function adds annotations to tplot figures
    """
    if delete:
        pytplot.tplot_opt_glob['annotations'] = None
        return

    annotations = {'text': text,
                   'position': position,
                   'xycoords': xycoords,
                   'fontfamily': fontfamily,
                   'fontsize': fontsize,
                   'fontvariant': fontvariant,
                   'fontstyle': fontstyle,
                   'fontstretch': fontstretch,
                   'fontweight': fontweight,
                   'rotation': rotation,
                   'color': color,
                   'alpha': alpha}

    if pytplot.tplot_opt_glob.get('annotations') is None:
        pytplot.tplot_opt_glob['annotations'] = [annotations]
    else:
        pytplot.tplot_opt_glob['annotations'].append(annotations)