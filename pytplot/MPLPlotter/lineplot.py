def lineplot(var_data, var_times, this_axis, line_opts, yaxis_options, plot_extras):
    alpha = plot_extras.get('alpha')

    if yaxis_options.get('legend_names') is not None:
        labels = yaxis_options['legend_names']
        if labels[0] is None:
            labels = None
    else:
        labels = None
    
    if len(var_data.y.shape) == 1:
        num_lines = 1
    else:
        num_lines = var_data.y.shape[1]

    # set up line colors
    if plot_extras.get('line_color') is not None:
        colors = plot_extras['line_color']
    else:
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
    else:
        thick = 0.5

    # line style
    if line_opts.get('line_style_name') is not None:
        line_style_user = line_opts['line_style_name']
        # legacy values
        if line_style_user == 'solid_line':
            line_style = 'solid'
        elif line_style_user == 'dot':
            line_style = 'dotted'
        elif line_style_user == 'dash':
            line_style = 'dashed'
        elif line_style_user == 'dash_dot':
            line_style = 'dashdot'
        else:
            line_style = line_style_user
    else:
        line_style = 'solid'

    symbols = False
    if line_opts.get('symbols') is not None:
        if line_opts['symbols']:
            symbols = True

    # create the plot
    line_options = {'linewidth': thick, 'linestyle': line_style, 'alpha': alpha}

    if line_opts.get('marker') is not None:
        line_options['marker'] = line_opts['marker']

    if line_opts.get('marker_size') is not None:
        if symbols:
            line_options['s'] = line_opts['marker_size']
        else:
            line_options['markersize'] = line_opts['marker_size']

    # check for error data first
    if 'dy' in var_data._fields:
        # error data provided
        line_options['yerr'] = var_data.dy
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
        this_line = plotter(var_times, var_data.y if num_lines == 1 else var_data.y[:, line], color=colors[line], **line_options)

        if labels is not None:
            if isinstance(this_line, list):
                this_line[0].set_label(labels[line])
            else:
                this_line.set_label(labels[line])

    if labels is not None:
        this_axis.legend()

    return True