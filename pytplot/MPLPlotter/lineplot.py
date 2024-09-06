import numpy as np
import pytplot
import logging


def lineplot(var_data,
             var_times,
             this_axis,
             line_opts,
             yaxis_options,
             plot_extras,
             running_trace_count=None,
             time_idxs=None,
             style=None,
             var_metadata=None):
    """
    Generate a matplotlib line plot from a tplot variable

    Parameters
    ----------
        var_data: dict
            The data to be plotted (may have multiple traces)
        var_times:
            Array of datetime objects to use for x axis
        this_axis:
            The current axis (plot panel) we're working with
        line_opts: dict
            A dictionary of line options
        yaxis_options: dict
            A dictionary of y axis options
        plot_extras: dict
            A dictionary of 'extra' options (colors, etc)
        running_trace_count:
            If not Null, an integer representing the number of traces already processed in this pseudovariable. Defaults to None.
        time_idxs: np.ndarray
            If provided, an integer array specifying the subset of time indices to be plotted. Defaults to None.
        style:
            A matplotlib style to be used in the plot. Defaults to None.
        var_metadata: dict
            The metadata dictionary associated with this tplot variable (used as a fallback for trace labels). Defaults to None.

    Returns
    -------
        True

    """
    alpha = plot_extras.get('alpha')

    if len(var_data.y.shape) == 1:
        num_lines = 1
    else:
        num_lines = var_data.y.shape[1]

    is_errorbar_plot = False
    if 'dy' in var_data._fields:
        is_errorbar_plot = True

    if yaxis_options.get('legend_names') is not None:
        labels = yaxis_options['legend_names']
        labels = get_trace_options(labels, running_trace_count, num_lines)

        if labels[0] is None:
            labels = None
    else:
        labels = None
        if var_metadata.get('CDF') is not None:
            labels = var_metadata['CDF'].get('LABELS')

    legend_location = yaxis_options.get('legend_location')

    bbox_to_anchor = None
    if legend_location is not None:
        if legend_location == 'spedas':
            # the spedas legend puts the legend on the outside of the panel
            # to the right of the panel (just like in IDL)
            legend_location = 'center left'
            bbox_to_anchor = (1.04, 0.5)
    else:
        legend_location = 'upper right'

    legend_size = yaxis_options.get('legend_size')
    legend_shadow = yaxis_options.get('legend_shadow')
    legend_title = yaxis_options.get('legend_title')
    legend_titlesize = yaxis_options.get('legend_titlesize')
    legend_color = yaxis_options.get('legend_color')
    legend_markerfirst = yaxis_options.get('legend_markerfirst')
    legend_markerscale = yaxis_options.get('legend_markerscale')
    legend_markersize = yaxis_options.get('legend_markersize')
    legend_edgecolor = yaxis_options.get('legend_edgecolor')
    legend_facecolor = yaxis_options.get('legend_facecolor')
    legend_frameon = yaxis_options.get('legend_frameon')
    legend_ncols = yaxis_options.get('legend_ncols')
    if legend_ncols is None:
        legend_ncols = 1

    if legend_markersize is None:
        legend_markersize = 4

    if legend_size is None:
        legend_size = pytplot.tplot_opt_glob.get('charsize')

    markers = None
    if line_opts.get('marker') is not None:
        markers = line_opts['marker']
        markers = get_trace_options(markers, running_trace_count, num_lines, repeat=True)

    colors = None
    if plot_extras.get('line_color') is not None:
        colors = plot_extras['line_color']
    else:
        if style is None:
            if num_lines == 1:
                colors = ['k']
            elif num_lines == 2:
                colors = ['r', 'g']
            elif num_lines == 3:
                colors = ['b', 'g', 'r']
            elif num_lines == 4:
                colors = ['b', 'g', 'r', 'k']
            else:
                colors = ['k', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
    colors = get_trace_options(colors, running_trace_count, num_lines, repeat=True)

    # line thickness
    if line_opts.get('line_width') is not None:
        thick = line_opts['line_width']
    else:
        thick = [0.5]
    thick = get_trace_options(thick, running_trace_count, num_lines, repeat=True)

    # line style
    if line_opts.get('line_style_name') is not None:
        line_style_user = line_opts['line_style_name']

        # line_style_user should already be a list
        # handle legacy values
        line_style = []
        for linestyle in line_style_user:
            if linestyle == 'solid_line':
                line_style.append('solid')
            elif linestyle == 'dot':
                line_style.append('dotted')
            elif linestyle == 'dash':
                line_style.append('dashed')
            elif linestyle == 'dash_dot':
                line_style.append('dashdot')
            else:
                line_style.append(linestyle)
    else:
        line_style = ['solid']
    line_style = get_trace_options(line_style, running_trace_count, num_lines, repeat=True)

    symbols = False
    if line_opts.get('symbols') is not None:
        if line_opts['symbols']:
            symbols = True

    # create the plot
    line_options = {'alpha': alpha}

    marker_every = None
    if line_opts.get('markevery') is not None:
        marker_every = line_opts['markevery']
        marker_every = get_trace_options(marker_every, running_trace_count, num_lines, repeat=True)

    marker_sizes = None
    if line_opts.get('marker_size') is not None:
        marker_sizes = line_opts['marker_size']
        marker_sizes = get_trace_options(marker_sizes, running_trace_count, num_lines, repeat=True)

    # check for error data first
    if is_errorbar_plot:
        # error data provided
        line_options['yerr'] = var_data.dy[time_idxs]
        plotter = this_axis.errorbar
        if line_opts.get('ecolor') is not None:
            line_options['ecolor'] = line_opts['ecolor']
        if line_opts.get('elinewidth') is not None:
            line_options['elinewidth'] = line_opts['elinewidth']
        if line_opts.get('errorevery') is not None:
            line_options['errorevery'] = line_opts['errorevery']
        if line_opts.get('capsize') is not None:
            line_options['capsize'] = line_opts['capsize']
    else:
        # no error data provided
        plotter = this_axis.plot
        # Note: to turn off connecting lines in an error bar plot, do not use the
        # 'symbols' option.  Instead, set the line_options metadata to 'None' (as a string).
        if symbols:
            plotter = this_axis.scatter

    for line in range(0, num_lines):
        if colors is not None:
            color = colors[line]
        else:
            color = None

        if markers is not None:
            marker = markers[line]
        else:
            marker = None

        if marker_sizes is not None:
            # Note: scaling of marker sizes in scatter plots and line plots is different!
            # For line plot and scatter plot marker sizes to match, the line plot
            # marker size should be the square root of the scatter plot marker size.
            # Maybe that should be enforced here....???

            if symbols:
                line_options['s'] = marker_sizes[line]
            else:
                line_options['markersize'] = marker_sizes[line]

        if symbols:
            this_line_style='None'
        else:
            this_line_style=line_style[line]

        if marker_every is not None:
            line_options['markevery'] = marker_every[line]

        this_line = plotter(var_times, var_data.y[time_idxs] if num_lines == 1 else var_data.y[time_idxs, line], color=color,
                            linestyle=this_line_style, linewidth=thick[line], marker=marker, **line_options)

        if labels is not None:
            try:
                if isinstance(this_line, list):
                    this_line[0].set_label(labels[line])
                else:
                    this_line.set_label(labels[line])
            except IndexError:
                continue

    if labels is not None:
        legend = this_axis.legend(loc=legend_location, fontsize=legend_size, shadow=legend_shadow, title=legend_title,
                         labelcolor=legend_color, markerfirst=legend_markerfirst, markerscale=legend_markerscale,
                         facecolor=legend_facecolor, edgecolor=legend_edgecolor, frameon=legend_frameon, ncols=legend_ncols,
                         title_fontsize=legend_titlesize, bbox_to_anchor=bbox_to_anchor)
        try:
            handles = legend.legend_handles
        except AttributeError:
            handles = legend.legendHandles
        for legobj in handles:
            legobj.set_linewidth(legend_markersize)

    return True

def get_trace_options(parent_array, start_trace=None, num_traces=1, repeat=False, fill=False, fillval=None):
    """ Get options for a set of traces from a parent array, extending or slicing as necessary to handle pseudovariable options

    Parameters
    -----------
        parent_array: str or list of str
            An array of option values to select from
        start_trace: int
            If set, we are processing a pseuodovariable, and this is the count of line traces processed so far for
            previous sub-variables in the current pseuodovariable.

            If parent_array is long enough (e.g. if set on the pseudovariable and intended to cover the complete
            set of traces), we take a slice from start_trace with num_traces entries.  If it matches
            the number of traces requested (e.g. parent array comes from this subvariable), we take it as-is.
            If there are fewer entries than num_traces (e.g. a single value intended to apply to all traces),
            we repeat parent_array or add fill until there are enough values to take a slice from start_trace.

            If None, we're just processing a regular variable, so we take values starting at zero (extending or filling
            as necessary)
            Default: None
        num_traces: int
            The number of traces in the current (sub-)variable.
        repeat: bool
            If True, extend the parent array by repetition if necessary. Defaults to False.
        fill: bool
            If True, extend the parent array by adding fill values. Defaults to False.
        fillval: Any
            If fill=True, values to append to parent_array to make enough entries. Defaults to None.

    Returns:
    --------
        list of option values with num_traces entries

    """
    if not isinstance(parent_array,list):
        parent_array=[parent_array]
    parent_length = len(parent_array)
    output_array = parent_array
    if start_trace is not None:
        end_trace = start_trace + num_traces
        if parent_length >= start_trace+num_traces:
            output_array = parent_array[start_trace:end_trace]
        elif parent_length == num_traces:
            output_array = parent_array
        else:
            if repeat:
                expansion_factor = int((end_trace/parent_length + 1))
                expanded_array = np.tile(parent_array,expansion_factor)
                output_array = expanded_array[start_trace:end_trace]
            elif fill:
                output_array = parent_array
                missing=num_traces-parent_length
                output_array.extend(np.tile([fillval],missing))
            else:
                logging.warning("Length of trace options (%d) smaller than number of traces (%d)",parent_length, num_traces)
    else:
        if len(parent_array) >= num_traces:
            output_array = parent_array[0:num_traces]
        else:
            if repeat:
                expansion_factor = int(num_traces/parent_length + 1)
                expanded_array = np.tile(parent_array,expansion_factor)
                output_array = expanded_array[0:num_traces]
            elif fill:
                output_array = parent_array
                missing = num_traces - parent_length
                output_array.extend(np.tile([fillval], missing))
            else:
                logging.warning("Length of trace options (%d) smaller than number of traces (%d)",parent_length, num_traces)
    return output_array