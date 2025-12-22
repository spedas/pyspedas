import logging
import pyspedas
import numpy as np
from pyspedas.tplot_tools import get_y_range
from pyspedas.tplot_tools import tplot_wildcard_expand


def options(name, option=None, value=None, opt_dict=None, quiet=False):
    """ Set a large variety of options for individual plots.

    Parameters
    ----------
        name : str or list[str]
            Names of tplot variables to be updated (wildcards accepted).
        option : str, optional
            The name of the option. See the options section below.
        value : str, int, float, list, optional
            The value of the option. See the options section below.
        opt_dict : dict, optional
            This can be a dictionary of option-value pairs. 'option' and 'value'
            will not be needed if this dictionary item is supplied.
        quiet: bool, optional
            If True, do not complain about unrecognized options.

    Options
    -------

    Many of the options are passed directly to matplotlib calls.  For more extensive documentation about how to use these
    obtions, see the matplotlib documentation: https://matplotlib.org/stable/users/index.html

    Note that many X-axis options are controlled at the level of the entire plot, rather than per-variable (since plots with multiple panels will
    share many X axis properties).  See the tplot_options() routine for available per-plot options,


        ======================  ===========  ===========================================================================================================================
        Panel Options           Value type   Notes
        ======================  ===========  ===========================================================================================================================
        title                   str          The title of the plot.
        panel_size              flt          Number between (0,1], representing the percent size of the plot.
        alpha                   flt          Number between [0,1], gives the transparency of the plot lines.
        line_width              flt          Sets plot line width.
        line_style              str          scatter (to make scatter plots), or solid_line, dot, dash, dash_dot, dash_dot_dot_dot, long_dash.
        border                  bool         Turns on or off the top/right axes that would create a box around the plot.
        var_label_format        str          The format of the tick labels if this variable is displayed as an alternative x axis. Default: {:.2f}
        char_size               int          Defines character size for x/y/z titles and subtitles
        right_axis              bool         If true,display a second Y axis on the right side of the plot.
        second_axis_size        numeric      The size of the second axis to display
        data_gap                numeric      If there is a gap in the data larger than this number in seconds, then insert
        (cont)                  (cont)       NaNs. This is similar to using the degap procedure on the variable, but is
        (cont)                  (cont)       applied at plot-time, and does not persist in the variable data.
        annotations             dict         A dictionary or list of dictionaries of matplotlib text annotation parameters (see annotate() routine)
        visible                 bool         If False, do not display lines for this variable.
        nodata                  bool         If True, do not display lines for this variable.
        ======================  ===========  ===========================================================================================================================

        ======================  ===========  ===========================================================================================================================
        Legend Options          Value type   Notes
        ======================  ===========  ===========================================================================================================================
        legend_names            list         A list of strings that will be used to identify the legends.
        legend_location         str          A string giving the location of the legend box.
        legend_size             numeric      The font size of the legend names
        legend_shadow           bool         Turns on or off drop shadows on the legend box
        legend_title            str          The title to display on the legend
        legend_titlesize        numeric      The font size of the legend title
        legend_color            [str]        The color of the legend names
        legend_edgecolor        str          The border color of the legend box
        legend_facecolor        str          The background color of the legend box
        legend_markerfirst      boolean      Put the marker and line to the left of the label in the legend
        legend_markerscale      numeric      The scale size of markers displayed in the legend
        legend_linewidth        numeric      The width of the lines displayed in the legend
        ======================  ===========  ===========================================================================================================================

        ======================  ===========  ===========================================================================================================================
        X Axis Options          Value type   Notes
        ======================  ===========  ===========================================================================================================================
        xtitle                  str          The title to be placed under the x axis.
        xsubtitle               str          The subtitle to be placed under the x axis
        xtitle_color            str          The color of the x axis title.
        xtick_length            numeric      The length of the x tick marks
        xtick_width             numeric      The width of the x tick marks
        xtick_color             str          The color of the x tick marks
        xtick_labelcolor        str          The color of the x tick marks
        xtick_direction         str          The direction of the x tick marks (in, out, inout)
        ======================  ===========  ===========================================================================================================================


        ======================  ===========  ===========================================================================================================================
        Y Axis Options          Value type   Notes
        ======================  ===========  ===========================================================================================================================
        y_range                 flt/list     Two numbers that give the y axis range of the plot. If a third argument is present, set linear or log scaling accordingly.
        ylog                    bool         True sets the y axis to log scale, False reverts.
        ytitle                  str          Title shown on the y axis. Use backslash for new lines.
        ysubtitle               str          Subtitle shown on the y axis.
        ytitle_color            str          The color of the y axis title.
        ytick_length            numeric      The length of the Y tick marks
        ytick_width             numeric      The width of the Y tick marks
        ytick_color             str          The color of the Y tick marks
        ytick_labelcolor        str          The color of the Y tick marks
        ytick_direction         str          The direction of the Y tick marks (in, out, inout)
        y_major_ticks           [numeric]    A list of values that will be used to set the major ticks on the Y axis.
        y_minor_tick_interval   numeric      The interval between minor ticks on the Y axis.
        ======================  ===========  ===========================================================================================================================

        ======================  ===========  ===========================================================================================================================
        Error Bar Options       Value type   Notes
        ======================  ===========  ===========================================================================================================================
        errorevery              numeric      Interval at which to show error bars
        capsize                 numeric      The size of error bar caps
        ecolor                  str          The color of the error bar lines
        elinewidth              numeric      The width of the error bar lines
        ======================  ===========  ===========================================================================================================================

        ======================  ===========  ===========================================================================================================================
        Marker/Symbol  Options  Value type   Notes
        ======================  ===========  ===========================================================================================================================
        marker_size             numeric      The size of the markers displayed in the plot
        markevery               numeric      Interval at which to show markers
        symbols                 bool         If True, display as a scatter plot (no lines)
        ======================  ===========  ===========================================================================================================================


        ======================  ===========  ===========================================================================================================================
        Z  / Specplot Options   Value type   Notes
        ======================  ===========  ===========================================================================================================================
        spec                    bool         Display this variable as a spectrogram.
        colormap                str/list     Color map to use for specplots https://matplotlib.org/examples/color/colormaps_reference.html.
        z_range                 flt/list     Two numbers that give the z axis range of the plot. If a third argument is present, set linear or log scaling accordingly.
        zlog                    int          True sets the z axis to log scale, False reverts (spectrograms only).
        ztitle                  str          Title shown on the z axis. Spec plots only. Use backslash for new lines.
        zsubtitle               str          Subtitle shown on the z axis. Spec plots only.
        ztitle_color            str          The color of the z axis title.
        x_interp                bool         If true, perform smoothing of spectrograms in the X direction
        x_interp_points         numeric      Number of interpolation points to use in the X direction
        y_interp                bool         If true, perform smoothing of spectrograms in the Y direction
        y_interp_points         numeric      Number of interpolation points to use in the Y direction
        xrange_slice            flt/list     Two numbers that give the x axis range of spectrogram slicing plots.
        yrange_slice            flt/list     Two numbers that give the y axis range of spectrogram slicing plots.
        xlog_slice              bool         Sets x axis on slice plot to log scale if True.
        ylog_slice              bool         Sets y axis on slice plot to log scale if True.
        spec_dim_to_plot        int/str      If variable has more than two dimensions, this sets which dimension the "v"
        (cont)                  (cont)       variable will display on the y axis in spectrogram plots.
        (cont)                  (cont)       All other dimensions are summed into this one, unless "spec_slices_to_use"
        (cont)                  (cont)       is also set for this variable.
        spec_slices_to_use      str          Must be a dictionary of coordinate:values. If a variable has more than two
        (cont)                  (cont)       dimensions, spectrogram plots will plot values at that particular slice of
        (cont)                  (cont)       that dimension. See examples for how it works.
        ======================  ===========  ===========================================================================================================================

        Many options have synonyms or variant spellings that are commonly used.  The first column gives the name that is used
        throughout the plotting code.  The second column gives the synonyms that are accepted.

        ======================  ======================================================================================================================================
        Canonical name          Accepted synonyms
        ======================  ======================================================================================================================================
        title                   name
        line_color              color, colors, col, cols, line_colors
        legend_names            labels, legend_name, legend_label, legend_labels
        legend_location         labels_location, legends_location, label_location, labels_location
        legend_size             labels_size, label_size
        legend_shadow           labels_shadow. label_shadow
        legend_title            label_title, labels_title
        legend_titlesize        lable_titlesize, labels_titlesize
        legend_color            legends_color, label_color, labels_color
        legend_edgecolor        label_edgecolor, labels_edgecolor
        legend_facecolor        label_facecolor, labels_facecolor
        legend_markerfirst      label_markerfirst, labels_markerfirst
        legend_markerscale      label_markerscale, labels_markerscale
        legend_linewidth        label_linewidth, labels_linewidth
        legend_frameon          label_frameon, labels_frameon
        legend_ncols            label_ncols, labels_ncols
        line_style_name         line_style, linestyle
        char_size               charsize
        marker                  markers
        marker_size             markersize
        markevery               markerevery mark_every marker_every
        symbol                  symbols
        line_width              thick
        y_range                 yrange
        z_range                 zrange
        data_gap                datagap
        spec_dim_to_plot        spec_plot_dim
        var_label_format        varlabel_format
        annotations             annotation
        ======================  ======================================================================================================================================



    Returns
    -------
        None

    Examples
    --------
        >>> # Change the y range of Variable1
        >>> import pyspedas
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pyspedas.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> pyspedas.options('Variable1', 'yrange', [2,4])

        >>> # Change Variable1 to use a log scale
        >>> pyspedas.options('Variable1', 'ylog', 1)
        >>> pyspedas.tplot('Variable1')

        >>> # Multi-dimensional variable
        >>> y_data = np.random.rand(5, 4, 3)
        >>> v1_data = [0, 1, 3, 4]
        >>> v2_data = [1, 2, 3]
        >>> pyspedas.store_data("Variable2", data={'x': x_data, 'y': y_data, 'v1': v1_data, 'v2': v2_data})
        >>> # Set the spectrogram plots to show dimension 'v2' at slice 'v1' = 0
        >>> pyspedas.options('Variable2', 'spec', 1)
        >>> pyspedas.options("Variable2", "spec_dim_to_plot", 'v2')
        >>> pyspedas.options("Variable2", "spec_slices_to_use", {'v1': 0})
        >>> pyspedas.tplot('Variable2')

    """

    if isinstance(name, int):
        name = list(pyspedas.tplot_tools.data_quants.keys())[name]

    if opt_dict is None:
        opt_dict = {option: value}
    else:
        if not isinstance(opt_dict,dict):
            logging.error("dict must be a dictionary object.  Returning.")
            return

    if not isinstance(name, list):
        name = [name]

    names = tplot_wildcard_expand(name)
    for i in names:

        for option, value in opt_dict.items():

            # Lower case option for consistency
            option = option.lower()

            if i not in pyspedas.tplot_tools.data_quants.keys():
                logging.info(str(i) + " is currently not in pyspedas.")
                return

            elif option in ['color', 'colors', 'col', 'cols', 'line_color', 'line_colors']:
                if isinstance(value, list):
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['line_color'] = value
                else:
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['line_color'] = [value]

            elif option == 'link':
                if isinstance(value, list):
                    pyspedas.link(i, value[1], value[0])

            elif option in ['annotation', 'annotations']:
                # It is probably more convenient to use the annotations() wrapper function
                # to manage annotations
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['annotations'] = value

            elif option == 'colormap':
                if isinstance(value, list):
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['colormap'] = value
                else:
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['colormap'] = [value]

            elif option == 'second_axis_size':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['second_axis_size'] = value

            elif option == 'spec':
                _reset_plots(i)
                if value:
                    if 'spec_bins' not in pyspedas.tplot_tools.data_quants[i].coords:
                        logging.warning(f"{i} does not contain coordinates for spectrogram plotting.  Continuing...")
                        continue
                    else:
                        pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['spec'] = value
                        pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['y_range'] = get_y_range(pyspedas.tplot_tools.data_quants[i])

                else:
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['spec'] = value
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['y_range'] = get_y_range(pyspedas.tplot_tools.data_quants[i])

                # Set the default dimension to plot by.  All others will be summed over.
                if 'spec_dim_to_plot' not in pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']:
                    if 'v' in pyspedas.tplot_tools.data_quants[i].coords:
                        pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['spec_dim_to_plot'] = 'v'
                    elif 'v2' in pyspedas.tplot_tools.data_quants[i].coords:
                        pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['spec_dim_to_plot'] = 'v2'
                    else:
                        pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['spec_dim_to_plot'] = 'v1'

            elif option in ['legend_names', 'labels', 'legend_name', 'legend_label', 'legend_labels']:
                if isinstance(value, list):
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_names'] = value
                else:
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_names'] = [value]

            elif option in ['legend_location', 'labels_location', 'legends_location', 'label_location', 'labels_location']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_location'] = value

            elif option in ['legend_size', 'labels_size', 'label_size']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_size'] = value

            elif option in ['legend_shadow', 'labels_shadow', 'label_shadow']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_shadow'] = value

            elif option in ['legend_title', 'label_title', 'labels_title']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_title'] = value

            elif option in ['legend_titlesize', 'label_titlesize', 'labels_titlesize']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_titlesize'] = value

            elif option in ['legend_color', 'legends_color','label_color','labels_color']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_color'] = value

            elif option in ['legend_edgecolor', 'label_edgecolor', 'labels_edgecolor']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_edgecolor'] = value

            elif option in ['legend_facecolor', 'label_facecolor', 'labels_facecolor']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_facecolor'] = value

            elif option in ['legend_markerfirst', 'label_markerfirst', 'labels_markerfirst']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_markerfirst'] = value

            elif option in ['legend_markerscale', 'label_markerscale', 'labels_markerscale']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_markerscale'] = value

            elif option in ['legend_linewidth', 'label_linewidth', 'labels_linewidth']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_linewidth'] = value

            elif option in ['legend_frameon', 'label_frameon', 'labels_frameon']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_frameon'] = value

            elif option in ['legend_ncols', 'labels_ncols', 'label_ncols']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_ncols'] = value

            elif option == 'xlog_slice':
                if value:
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['slice_xaxis_opt']['xi_axis_type'] = 'log'
                else:
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['slice_xaxis_opt']['xi_axis_type'] = 'linear'

            elif option == 'ylog':
                negflag = 0 # _ylog_check(data_quants, value, i)
                if negflag == 0 and value:
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['y_axis_type'] = 'log'
                else:
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['y_axis_type'] = 'linear'

            elif option == 'ylog_slice':
                if value:
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['slice_yaxis_opt']['yi_axis_type'] = 'log'
                else:
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['slice_yaxis_opt']['yi_axis_type'] = 'linear'

            elif option == 'zlog':
                # check for negative values and warn the user that they will be ignored
                negflag = _zlog_check(pyspedas.tplot_tools.data_quants, value, i)
                if negflag != 0 and value:
                    logging.warning(str(i) + ' contains negative values; setting the z-axis to log scale will cause the negative values to be ignored on figures.')

                if value:
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['zaxis_opt']['z_axis_type'] = 'log'
                else:
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['zaxis_opt']['z_axis_type'] = 'linear'

            elif option =='visible':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['visible'] = bool(value)

            elif option =='nodata':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['visible'] = not bool(value)

            # Obsolete? (except for value='none'?) JWL 2024-03-21
            # These don't seem to be the correct format for matplotlib parameterized line styles.
            elif option in ['line_style', 'linestyle', 'line_style_name']:
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

                # This does not appear to be used by tplot. JWL 2024-03-21
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['line_style'] = to_be

                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['line_style_name'] = _convert_to_matplotlib_linestyle(value)

                # unused?
                if(value == 6 or value == 'none'):
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['visible'] = False

            elif option in ['char_size', 'charsize']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['char_size'] = value

            elif option in ['var_label_format', 'varlabel_format']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['var_label_format'] = value

            elif option in ['name', 'title']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['title'] = value

            elif option == "panel_size":
                if value > 1 or value <= 0:
                    logging.info("Invalid panel_size value (%f). Should be in (0, 1]",value)
                    return
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['panel_size'] = value

            elif option == 'alpha':
                if value > 1 or value < 0:
                    logging.info("Invalid alpha value (%f). Should be [0, 1]",value)
                    return
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['alpha'] = value

            elif option in ['marker', 'markers']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['marker'] = value

            elif option == 'errorevery':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['errorevery'] = value

            elif option == 'capsize':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['capsize'] = value

            elif option == 'ecolor':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['ecolor'] = value

            elif option == 'elinewidth':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['elinewidth'] = value

            elif option in ['marker_size', 'markersize']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['marker_size'] = value

            elif option in ['markevery', 'markerevery', 'mark_every', 'marker_every']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['markevery'] = value

            elif option in ['symbols', 'symbol']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['symbols'] = value

            elif option == 'xtick_length':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['xtick_length'] = value

            elif option == 'ytick_length':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['ytick_length'] = value

            elif option == 'xtick_width':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['xtick_width'] = value

            elif option == 'ytick_width':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['ytick_width'] = value

            elif option == 'xtick_color':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['xtickcolor'] = value

            elif option == 'ytick_color':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['ytickcolor'] = value

            elif option == 'xtick_labelcolor':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['xtick_labelcolor'] = value

            elif option == 'ytick_labelcolor':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['ytick_labelcolor'] = value

            elif option == 'xtick_direction':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['xtick_direction'] = value

            elif option == 'ytick_direction':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['ytick_direction'] = value

            elif option == 'right_axis':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['right_axis'] = value

            elif option in ['thick', 'line_width']:
                if isinstance(value, list):
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['line_width'] = value
                else:
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['line_opt']['line_width'] = [value]

            elif option in ['yrange', 'y_range']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['y_range'] = [value[0], value[1]]
                # track whether the yrange option was set by the user
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['y_range_user'] = True
                # IDL SPEDAS supports a 3-argument form of yrange, where the third argument selects
                # log or linear scaling
                if len(value) == 3:
                    if value[2]:
                        pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['y_axis_type'] = 'log'
                    else:
                        pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['y_axis_type'] = 'linear'

            elif option == 'y_major_ticks':
                # check whether the value is 1D array-like
                if isinstance(value, (list, np.ndarray)):
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['y_major_ticks'] = value
                else:
                    logging.warning('y_major_ticks must be a 1D array-like object')

            elif option == 'y_minor_tick_interval':
                # check whether the value is a number
                if isinstance(value, (int, float)):
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['y_minor_tick_interval'] = value
                else:
                    logging.warning('y_minor_tick_interval must be a number')

            elif option in ['zrange', 'z_range']:
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['zaxis_opt']['z_range'] = [value[0], value[1]]
                if len(value) == 3:
                    # IDL SPEDAS supports a 3-argument form of zrange, where the third element specifies linear vs. log scaling.
                    negflag = _zlog_check(pyspedas.tplot_tools.data_quants, value[2], i)
                    if negflag != 0 and value:
                        logging.warning(str(i) + ' contains negative values; setting the z-axis to log scale will cause the negative values to be ignored on figures.')

                    if value[2]:
                        pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['zaxis_opt']['z_axis_type'] = 'log'
                    else:
                        pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['zaxis_opt']['z_axis_type'] = 'linear'

            elif option == 'xrange_slice':
                plt_opts = pyspedas.tplot_tools.data_quants[i].attrs['plot_options']
                if plt_opts.get('slice_xaxis_opt') is not None:
                    plt_opts['slice_xaxis_opt']['xi_range'] = [value[0], value[1]]

            elif option == 'yrange_slice':
                plt_opts = pyspedas.tplot_tools.data_quants[i].attrs['plot_options']
                if plt_opts.get('slice_yaxis_opt') is not None:
                    plt_opts['slice_yaxis_opt']['yi_range'] = [value[0], value[1]]

            elif option == 'xtitle':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['xaxis_opt']['axis_label'] = value

            elif option == 'ytitle':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['axis_label'] = value

            elif option == 'ztitle':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['zaxis_opt']['axis_label'] = value

            elif option == 'xsubtitle':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['xaxis_opt']['axis_subtitle'] = value

            elif option == 'ysubtitle':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['axis_subtitle'] = value

            elif option == 'zsubtitle':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['zaxis_opt']['axis_subtitle'] = value

            elif option == 'xtitle_color':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['xaxis_opt']['axis_color'] = value

            elif option == 'ytitle_color':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['axis_color'] = value

            elif option == 'ztitle_color':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['zaxis_opt']['axis_color'] = value

            elif option in ['data_gap', 'datagap']: #jmm, 2023-06-20
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['data_gap'] = value

            elif option in ['spec_dim_to_plot', 'spec_plot_dim']:
                if len(pyspedas.tplot_tools.data_quants[i].values.shape) <= 2:
                    logging.warning(f"Must have more than 2 coordinate dimensions to set spec_coord_to_plot for {pyspedas.tplot_tools.data_quants[i].name}")
                    continue

                # Set the 'spec_dim_to_plot' value to either 'v' or 'v1', 'v2', 'v3', etc.
                if isinstance(value, int):
                    coord_to_plot = "v" + str(value)
                    if coord_to_plot not in pyspedas.tplot_tools.data_quants[i].coords:
                        if value == 1:
                            coord_to_plot = "v"
                            if coord_to_plot not in pyspedas.tplot_tools.data_quants[i].coords:
                                logging.warning(f"Dimension {value} not found in {pyspedas.tplot_tools.data_quants[i].name}")
                                continue
                        else:
                            logging.warning(f"Dimension {value} not found in {pyspedas.tplot_tools.data_quants[i].name}")
                            continue
                    pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['spec_dim_to_plot'] = coord_to_plot
                elif isinstance(value, str):
                    coord_to_plot = value
                    if coord_to_plot not in pyspedas.tplot_tools.data_quants[i].coords:
                        logging.warning(f"Dimension {value} not found in {pyspedas.tplot_tools.data_quants[i].name}")
                        continue
                    else:
                        pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['spec_dim_to_plot'] = value

                # If we're plotting against different coordinates, we need to change what we consider the "spec_bins"
                pyspedas.tplot_tools.data_quants[i].coords['spec_bins'] = pyspedas.tplot_tools.data_quants[i].coords[coord_to_plot]
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['y_range'] = get_y_range(pyspedas.tplot_tools.data_quants[i])

            elif option == 'spec_slices_to_use':
                if not isinstance(value, dict):
                    logging.error("Must be a dictionary object in the format {'v2':15, 'v3':7}")
                    return
                else:
                    for coord in value:
                        if coord not in pyspedas.tplot_tools.data_quants[i].coords:
                            logging.warning(f"Dimension {coord} not found in {pyspedas.tplot_tools.data_quants[i].name}")
                            continue

                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['spec_slices_to_use'] = value

            elif option == 'border':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['extras']['border'] = value

            elif option == 'y_interp':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['y_interp'] = value

            elif option == 'y_interp_points':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['y_interp_points'] = value

            elif option == 'x_interp':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['x_interp'] = value

            elif option == 'x_interp_points':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['x_interp_points'] = value
            elif option == 'y_no_resample':
                pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['yaxis_opt']['y_no_resample'] = value

            else:
                # Apparently cdf_to_tplot is treating all variable attributes as potential plot
                # options.  Adding this warning will end up spamming the logs unless cdf_to_tplot is changed.
                if not quiet:
                    logging.warning(f"Unrecognized option {option}")
                #pass
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
                    logging.warning('Negative data is incompatible with log plotting.')
                    negflag = 1
                    break
            else:
                if dataset.attrs['plot_options']['extras']['spec'] == 1:
                    if dataset.coords['spec_bins'].min(skipna=True) < 0:
                        logging.warning('Negative data is incompatible with log plotting.')
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
                        negflag = 1
                        break
        elif value != 1:
            # Using the 'negflag' as a way to not log something if the user doesn't want it to be logged
            negflag = 1
    return negflag


def _reset_plots(name):
    if isinstance(pyspedas.tplot_tools.data_quants[name], dict):  # non-record varying variable
        return
    pyspedas.tplot_tools.data_quants[name].attrs['plot_options']['extras']['spec'] = 0
    pyspedas.tplot_tools.data_quants[name].attrs['plot_options']['extras']['alt'] = 0
    pyspedas.tplot_tools.data_quants[name].attrs['plot_options']['extras']['map'] = 0
    pyspedas.tplot_tools.data_quants[name].attrs['plot_options']['extras']['plotter'] = None

def _convert_to_matplotlib_linestyle(linestyle):
    if not isinstance(linestyle,list):
        linestyle = [linestyle]
    converted_linestyles = []
    for ls in linestyle:
        if ls == 'solid_line':
            converted_linestyles.append('solid')
        elif ls == 'dot':
            converted_linestyles.append('dotted')
        elif ls == 'dash':
            converted_linestyles.append('dashed')
        elif ls == 'dash_dot':
            converted_linestyles.append('dashdot')
        else:
            converted_linestyles.append(ls)
    return converted_linestyles


