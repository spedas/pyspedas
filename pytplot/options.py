# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pytplot
import numpy as np
from pytplot import tplot_utilities as utilities
from copy import deepcopy

def options(name, option=None, value=None, opt_dict=None):
    """
    This function allows the user to set a large variety of options for individual plots.

    Parameters:
        name : str
            Name or number of the tplot variable
        option : str
            The name of the option.  See section below.
        value : str/int/float/list
            The value of the option.  See section below.
        dict : dict
            This can be a dictionary of option:value pairs.  Option and value
            will not be needed if this dictionary item is supplied.

    Options:
        =================== ==========   =====
        Options             Value type   Notes
        =================== ==========   =====
        Color               str/list     red, green, blue, etc.  Also takes in RGB tuples, i.e. (0,255,0) for green
        Colormap            str/list     https://matplotlib.org/examples/color/colormaps_reference.html.
        Spec                int          1 sets the Tplot Variable to spectrogram mode, 0 reverts.
        Alt                 int          1 sets the Tplot Variable to altitude plot mode, 0 reverts.
        Map                 int          1 sets the Tplot Variable to latitude/longitude mode, 0 reverts.
        link                list         Allows a user to reference one tplot variable to another.
        ylog                int          1 sets the y axis to log scale, 0 reverts.
        zlog                int          1 sets the z axis to log scale, 0 reverts (spectrograms only).
        legend_names        list         A list of strings that will be used to identify the lines.
        xlog_slice          bool         Sets x axis on slice plot to log scale if True.
        ylog                bool         Set y axis on main plot window to log scale if True.
        ylog_slice          bool         Sets y axis on slice plot to log scale if True.
        zlog                bool         Sets z axis on main plot window to log scale if True.
        line_style          str          scatter (to make scatter plots), or solid_line, dot, dash, dash_dot, dash_dot_dot_dot, long_dash.
        char_size           int          Defines character size for plot labels, etc.
        name                str          The title of the plot.
        panel_size          flt          Number between (0,1], representing the percent size of the plot.
        basemap             str          Full path and name of a background image for "Map" plots.
        alpha               flt          Number between [0,1], gives the transparancy of the plot lines.
        thick               flt          Sets plot line width.
        yrange              flt list     Two numbers that give the y axis range of the plot.
        zrange              flt list     Two numbers that give the z axis range of the plot.
        xrange_slice        flt list     Two numbers that give the x axis range of spectrogram slicing plots.
        yrange_slice        flt list     Two numbers that give the y axis range of spectrogram slicing plots.
        ytitle              str          Title shown on the y axis.  Use backslash for new lines.
        ztitle              str          Title shown on the z axis.  Spec plots only.  Use backslash for new lines.
        ysubtitle           str          Subtitle shown on the y axis.
        zsubtitle           str          Subtitle shown on the z axis.  Spec plots only.
        plotter             str          Allows a user to implement their own plotting script in place of the ones
                                         herein.
        crosshair_x         str          Title for x-axis crosshair.
        crosshair_y         str          Title for y-axis crosshair.
        crosshair_z         str          Title for z-axis crosshair.
        static              str          Datetime string that gives desired time to plot y and z values from a spec
                                         plot.
        static_tavg         str          Datetime string that gives desired time-averaged y and z values to plot
                                         from a spec plot.
        t_average           int          Seconds around which the cursor is averaged when hovering over spectrogram
                                         plots.
        spec_plot_dim       int          If variable two dimensions, this sets which dimension the variable will have on
                                         on the y axis.  All other dimensions are summed into this one.
        border              bool         Turns on or off the top/right axes that would create a box around the plot
        var_label_ticks     int          Sets the number of ticks if this variable is displayed as an alternative x axis
        =================== ==========   =====
    Returns:
        None

    Examples:
        >>> # Change the y range of Variable1
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> pytplot.options('Variable1', 'yrange', [2,4])

        >>> # Change Variable1 to use a log scale
        >>> pytplot.options('Variable1', 'ylog', 1)

    """

    if isinstance(name, int):
        name = list(pytplot.data_quants.keys())[name]

    if opt_dict is None:
        opt_dict = {option: value}
    else:
        if not isinstance(opt_dict,dict):
            print("dict must be a dictionary object.  Returning.")
            return

    if not isinstance(name, list):
        name = [name]

    for i in name:

        for option, value in opt_dict.items():

            # Lower case option for consistency
            option = option.lower()

            if i not in pytplot.data_quants.keys():
                print(str(i) + " is currently not in pytplot.")
                return

            if option == 'color':
                if isinstance(value, list):
                    pytplot.data_quants[i].attrs['plot_options']['extras']['line_color'] = value
                else:
                    pytplot.data_quants[i].attrs['plot_options']['extras']['line_color'] = [value]

            if option == 'link':
                if isinstance(value, list):
                    pytplot.link(i, value[1], value[0])

            if option == 'colormap':
                if isinstance(value, list):
                    pytplot.data_quants[i].attrs['plot_options']['extras']['colormap'] = value
                else:
                    pytplot.data_quants[i].attrs['plot_options']['extras']['colormap'] = [value]

            if option == 'spec':
                _reset_plots(i)
                if value:
                    if 'spec_bins' not in pytplot.data_quants[i].coords:
                        print(f"{i} does not contain coordinates for spectrogram plotting.  Continuing...")
                    else:
                        pytplot.data_quants[i].attrs['plot_options']['extras']['spec'] = value
                        pytplot.data_quants[i].attrs['plot_options']['yaxis_opt']['y_range'] = utilities.get_y_range(pytplot.data_quants[i])

                else:
                    pytplot.data_quants[i].attrs['plot_options']['extras']['spec'] = value
                    pytplot.data_quants[i].attrs['plot_options']['yaxis_opt']['y_range'] = utilities.get_y_range(pytplot.data_quants[i])

            if option == 'alt':
                _reset_plots(i)
                pytplot.data_quants[i].attrs['plot_options']['extras']['alt'] = value

            if option == 'map':
                _reset_plots(i)
                pytplot.data_quants[i].attrs['plot_options']['extras']['map'] = value

            if option == 'legend_names':
                if isinstance(value, list):
                    pytplot.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_names'] = value
                else:
                    pytplot.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_names'] = [value]

            if option == 'xlog_slice':
                if value:
                    pytplot.data_quants[i].attrs['plot_options']['slice_xaxis_opt']['xi_axis_type'] = 'log'
                else:
                    pytplot.data_quants[i].attrs['plot_options']['slice_xaxis_opt']['xi_axis_type'] = 'linear'

            if option == 'ylog':
                negflag = 0 # _ylog_check(data_quants, value, i)
                if negflag == 0 and value:
                    pytplot.data_quants[i].attrs['plot_options']['yaxis_opt']['y_axis_type'] = 'log'
                else:
                    pytplot.data_quants[i].attrs['plot_options']['yaxis_opt']['y_axis_type'] = 'linear'

            if option == 'ylog_slice':
                if value:
                    pytplot.data_quants[i].attrs['plot_options']['slice_yaxis_opt']['yi_axis_type'] = 'log'
                else:
                    pytplot.data_quants[i].attrs['plot_options']['slice_yaxis_opt']['yi_axis_type'] = 'linear'

            if option == 'zlog':
                negflag = _zlog_check(pytplot.data_quants, value, i)
                if negflag == 0:
                    pytplot.data_quants[i].attrs['plot_options']['zaxis_opt']['z_axis_type'] = 'log'
                else:
                    pytplot.data_quants[i].attrs['plot_options']['zaxis_opt']['z_axis_type'] = 'linear'

            if option == 'nodata':
                pytplot.data_quants[i].attrs['plot_options']['line_opt']['visible'] = value

            if option == 'line_style':
                to_be = []
                if value == 0 or value == 'solid_line':
                    to_be = []
                elif value == 1 or value == 'dot':
                    to_be = [2, 4]
                elif value == 2 or value == 'dash':
                    to_be = [6]
                elif value == 3 or value == 'dash_dot':
                    to_be = [6, 4, 2, 4]
                elif value == 4 or value == 'dash_dot_dot_dot':
                    to_be = [6, 4, 2, 4, 2, 4, 2, 4]
                elif value == 5 or value == 'long_dash':
                    to_be = [10]
                else:
                    to_be=value

                pytplot.data_quants[i].attrs['plot_options']['line_opt']['line_style'] = to_be

                if(value == 6 or value == 'none'):
                    pytplot.data_quants[i].attrs['plot_options']['line_opt']['visible'] = False

            if option == 'char_size':
                pytplot.data_quants[i].attrs['plot_options']['extras']['char_size'] = value

            if option == 'name':
                pytplot.data_quants[i].attrs['plot_options']['line_opt']['name'] = value

            if option == "panel_size":
                if value > 1 or value <= 0:
                    print("Invalid value. Should be (0, 1]")
                    return
                pytplot.data_quants[i].attrs['plot_options']['extras']['panel_size'] = value

            if option == 'basemap':
                pytplot.data_quants[i].attrs['plot_options']['extras']['basemap'] = value

            if option == 'alpha':
                if value > 1 or value < 0:
                    print("Invalid value. Should be [0, 1]")
                    return
                pytplot.data_quants[i].attrs['plot_options']['extras']['alpha'] = value

            if option == 'thick':
                pytplot.data_quants[i].attrs['plot_options']['line_opt']['line_width'] = value

            if option == 'yrange' or option == 'y_range':
                pytplot.data_quants[i].attrs['plot_options']['yaxis_opt']['y_range'] = [value[0], value[1]]

            if option == 'zrange' or option == 'z_range':
                pytplot.data_quants[i].attrs['plot_options']['zaxis_opt']['z_range'] = [value[0], value[1]]

            if option == 'xrange_slice':
                pytplot.data_quants[i].attrs['plot_options']['slice_xaxis_opt']['xi_range'] = [value[0], value[1]]

            if option == 'yrange_slice':
                pytplot.data_quants[i].attrs['plot_options']['slice_yaxis_opt']['yi_range'] = [value[0], value[1]]

            if option == 'xtitle':
                pytplot.data_quants[i].attrs['plot_options']['xaxis_opt']['axis_label'] = value

            if option == 'ytitle':
                pytplot.data_quants[i].attrs['plot_options']['yaxis_opt']['axis_label'] = value

            if option == 'ztitle':
                pytplot.data_quants[i].attrs['plot_options']['zaxis_opt']['axis_label'] = value

            if option == 'xsubtitle':
                pytplot.data_quants[i].attrs['plot_options']['xaxis_opt']['axis_subtitle'] = value

            if option == 'ysubtitle':
                pytplot.data_quants[i].attrs['plot_options']['yaxis_opt']['axis_subtitle'] = value

            if option == 'zsubtitle':
                pytplot.data_quants[i].attrs['plot_options']['zaxis_opt']['axis_subtitle'] = value

            if option == 'ybar':
                pytplot.data_quants[i].attrs['plot_options']['extras']['ybar'] = value

            if option == 'ybar_color':
                pytplot.data_quants[i].attrs['plot_options']['extras']['ybar'] = value

            if option == 'ybar_size':
                pytplot.data_quants[i].attrs['plot_options']['extras']['ysize'] = value

            if option == 'plotter':
                _reset_plots(i)
                pytplot.data_quants[i].attrs['plot_options']['extras']['plotter'] = value

            if option == 'crosshair_x':
                pytplot.data_quants[i].attrs['plot_options']['xaxis_opt']['crosshair'] = value

            if option == 'crosshair_y':
                pytplot.data_quants[i].attrs['plot_options']['yaxis_opt']['crosshair'] = value

            if option == 'crosshair_z':
                pytplot.data_quants[i].attrs['plot_options']['zaxis_opt']['crosshair'] = value

            if option == 'static':
                pytplot.data_quants[i].attrs['plot_options']['extras']['static'] = value

            if option == 'static_tavg':
                pytplot.data_quants[i].attrs['plot_options']['extras']['static_tavg'] = [value[0], value[1]]

            if option == 't_average':
                pytplot.data_quants[i].attrs['plot_options']['extras']['t_average'] = value

            if option == 'spec_plot_dim':
                attr_dict = deepcopy(pytplot.data_quants[i].attrs)
                data_dict = {}
                data_dict['x'] = pytplot.data_quants[i].coords['time'].values
                data_values = pytplot.data_quants[i].values
                if len(data_values.shape) <= 2:
                    pass
                else:
                    data_dict['y'] = np.swapaxes(data_values, 2, value)
                    for c in pytplot.data_quants[i].coords:
                        if c=='time' or c=='spec_bins':
                            continue
                        data_dict[c] = pytplot.data_quants[i].coords[c].values
                    v2_values = pytplot.data_quants[i].coords["v2"].values
                    data_dict['v2'] = data_dict['v'+str(value)]
                    data_dict['v' + str(value)] = v2_values
                    pytplot.store_data(i, data=data_dict)
                    pytplot.data_quants[i].attrs = attr_dict
                    pytplot.data_quants[i].attrs['plot_options']['yaxis_opt']['y_range'] = utilities.get_y_range(pytplot.data_quants[i])

            if option == 'border':
                pytplot.data_quants[i].attrs['plot_options']['extras']['border'] = value

            if option == 'var_label_ticks':
                pytplot.data_quants[i].attrs['plot_options']['var_label_ticks'] = value


    return


def _ylog_check(data_quants, value, i):
    negflag = 0
    namedata = data_quants[i]
    # check variable data
    # if negative numbers, don't allow log setting
    datasets = [namedata]
    for oplot_name in namedata.attrs['plot_options']['overplots']:
        datasets.append(data_quants[oplot_name])

    if value == 1:
        for dataset in datasets:
            if 'spec' not in dataset.attrs['plot_options']['extras']:
                if dataset.min(skipna=True) < 0:
                    print('Negative data is incompatible with log plotting.')
                    negflag = 1
                    break
            else:
                if dataset.attrs['plot_options']['extras']['spec'] == 1:
                    if dataset.coords['spec_bins'].min(skipna=True) < 0:
                        print('Negative data is incompatible with log plotting.')
                        negflag = 1
                        break
    elif value != 1:
        # Using the 'negflag' as a way to not log something if the user doesn't want it to be logged
        negflag = 1
    return negflag


def _zlog_check(data_quants, value, i):
    negflag = 0
    namedata = data_quants[i]
    # check variable data
    # if negative numbers, don't allow log setting
    datasets = [namedata]
    for oplot_name in namedata.attrs['plot_options']['overplots']:
        datasets.append(data_quants[oplot_name])

    for dataset in datasets:
        if value == 1:
            if 'spec' in dataset.attrs['plot_options']['extras']:
                if dataset.attrs['plot_options']['extras']['spec'] == 1:
                    if dataset.min(skipna=True) < 0:
                        print('Negative data is incompatible with log plotting.')
                        negflag = 1
                        break
        elif value != 1:
            # Using the 'negflag' as a way to not log something if the user doesn't want it to be logged
            negflag = 1
    return negflag


def _reset_plots(name):
    pytplot.data_quants[name].attrs['plot_options']['extras']['spec'] = 0
    pytplot.data_quants[name].attrs['plot_options']['extras']['alt'] = 0
    pytplot.data_quants[name].attrs['plot_options']['extras']['map'] = 0
    pytplot.data_quants[name].attrs['plot_options']['extras']['plotter'] = None
