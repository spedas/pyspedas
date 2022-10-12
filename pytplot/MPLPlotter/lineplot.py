import numpy as np
import pytplot


def lineplot(var_data,
             var_times,
             this_axis,
             line_opts,
             yaxis_options,
             plot_extras,
             pseudo_plot_num=None,
             time_idxs=None,
             style=None,
             var_metadata=None):
    alpha = plot_extras.get('alpha')

    if len(var_data.y.shape) == 1:
        num_lines = 1
    else:
        num_lines = var_data.y.shape[1]

    if yaxis_options.get('legend_names') is not None:
        labels = yaxis_options['legend_names']
        if pseudo_plot_num is not None and pseudo_plot_num < len(labels):
            labels = [yaxis_options['legend_names'][pseudo_plot_num]]

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

    if legend_markersize is None:
        legend_markersize = 4

    if legend_size is None:
        legend_size = pytplot.tplot_opt_glob.get('charsize')

    # set up line colors
    colors = None

    if plot_extras.get('line_color') is not None:
        colors = plot_extras['line_color']
        if pseudo_plot_num is not None and pseudo_plot_num < len(colors):
            colors = [plot_extras['line_color'][pseudo_plot_num]]

        # check the color size vs. the size of the data
        # colors should already be an array at this point
        colors = np.array(colors)
        if len(colors.shape) == 1:
            if len(colors) != num_lines:
                print('Problem with the number of line colors specified')
                return
        else:
            # time varying symbol colors, not supported yet
            if colors.shape[1] != num_lines:
                print('Problem with the number of line colors specified')
                return
    else:
        if style is None:
            if num_lines == 3:
                colors = ['b', 'g', 'r']
            elif num_lines == 4:
                colors = ['b', 'g', 'r', 'k']
            else:
                colors = ['k', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']

            if num_lines >= len(colors):
                colors = colors*num_lines

    # line thickness
    if line_opts.get('line_width') is not None:
        thick = line_opts['line_width']
        if pseudo_plot_num is not None and pseudo_plot_num < len(thick):
            thick = [line_opts['line_width'][pseudo_plot_num]]
    else:
        thick = [0.5]

    if num_lines >= len(thick):
        thick = thick*num_lines

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
        if pseudo_plot_num is not None and pseudo_plot_num < len(line_style):
            line_style = [line_opts['line_style_name'][pseudo_plot_num]]
    else:
        line_style = ['solid']

    if num_lines >= len(line_style):
        line_style = line_style*num_lines

    symbols = False
    if line_opts.get('symbols') is not None:
        if line_opts['symbols']:
            symbols = True

    # create the plot
    line_options = {'alpha': alpha}

    if line_opts.get('marker') is not None:
        line_options['marker'] = line_opts['marker']

    if line_opts.get('markevery') is not None:
        line_options['markevery'] = line_opts['markevery']

    if line_opts.get('marker_size') is not None:
        if symbols:
            line_options['s'] = line_opts['marker_size']
        else:
            line_options['markersize'] = line_opts['marker_size']

    # check for error data first
    if 'dy' in var_data._fields:
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
        if symbols:
            plotter = this_axis.scatter

    for line in range(0, num_lines):
        if colors is not None:
            color = colors[line]
        else:
            color=None
        this_line = plotter(var_times, var_data.y[time_idxs] if num_lines == 1 else var_data.y[time_idxs, line], color=color,
                            linestyle=line_style[line], linewidth=thick[line], **line_options)

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
                         facecolor=legend_facecolor, edgecolor=legend_edgecolor, frameon=legend_frameon,
                         title_fontsize=legend_titlesize, bbox_to_anchor=bbox_to_anchor)
        for legobj in legend.legendHandles:
            legobj.set_linewidth(legend_markersize)

    return True
