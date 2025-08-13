# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import logging
import datetime
import numpy as np
from dateutil.parser import parse
import pyspedas
import copy



def set_tplot_options(option, value, old_tplot_opt_glob):
    new_tplot_opt_glob = old_tplot_opt_glob
    
    if option in ['title_text', 'title']:
        new_tplot_opt_glob['title_text'] = value
    
    elif option == 'title_size':
        new_tplot_opt_glob['title_size'] = value
        
    elif option == 'var_label':
        new_tplot_opt_glob['var_label'] = value

    elif option == 'x_range':
        new_tplot_opt_glob['x_range'] = value

    elif option == 'data_gap':
        new_tplot_opt_glob['data_gap'] = value

    elif option == 'axis_font_size':
        new_tplot_opt_glob['axis_font_size'] = value

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

    elif option == 'varlabel_style':
        new_tplot_opt_glob['varlabel_style'] = value

    else:
        logging.warning("Unknown option supplied: " + str(option))

    return new_tplot_opt_glob


def str_to_float_fuzzy(time_str):
    """
    Implementation of str_to_int (below) that uses dateutil and .timestamp()
    to convert the date/time string to integer (number of seconds since Jan 1, 1970)

    This function is slower than str_to_int, but more flexible
    """
    dt_object = parse(time_str)
    return dt_object.replace(tzinfo=datetime.timezone.utc).timestamp()

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


def convert_tplotxarray_to_pandas_dataframe(name, no_spec_bins=False):
    import pandas as pd
    # This function is not final, and will presumably change in the future
    # This function sums over all dimensions except for the second non-time one.
    # This collapses many dimensions into just a single "energy bin" dimensions

    matrix = pyspedas.pytplot.data_quants[name].values
    while len(matrix.shape) > 3:
        matrix = np.nansum(matrix, 3)
    if len(matrix.shape) == 3:
        matrix = np.nansum(matrix, 1)
    return_data = pd.DataFrame(matrix)
    return_data = return_data.set_index(pd.Index(pyspedas.pytplot.data_quants[name].coords['time'].values))

    if no_spec_bins:
        return return_data

    if 'spec_bins' in pyspedas.pytplot.data_quants[name].coords:
        spec_bins = pd.DataFrame(pyspedas.pytplot.data_quants[name].coords['spec_bins'].values)
        if len(pyspedas.pytplot.data_quants[name].coords['spec_bins'].shape) == 1:
            spec_bins = spec_bins.transpose()
        else:
            spec_bins = spec_bins.set_index(pd.Index(pyspedas.pytplot.data_quants[name].coords['time'].values))

        return return_data, spec_bins

    return return_data


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
        da = copy.deepcopy(pyspedas.pytplot.data_quants[name])
    else:
        return

    if da.attrs['plot_options']['extras'].get('spec_dim_to_plot', None) is not None:
        coordinate_to_plot = da.attrs['plot_options']['extras']['spec_dim_to_plot']
    else:
        # If not found, default to v2 (to match behavior in options.py when setting "spec" option)
        coordinate_to_plot = "v2"

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

