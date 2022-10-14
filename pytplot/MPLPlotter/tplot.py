import copy
import numpy as np
import matplotlib as mpl
from datetime import date, datetime, timezone
from matplotlib import pyplot as plt
import pytplot
from fnmatch import filter as tname_filter
from time import sleep

from .lineplot import lineplot
from .specplot import specplot

# the following improves the x-axis ticks labels
import matplotlib.units as munits
import matplotlib.dates as mdates
converter = mdates.ConciseDateConverter()
munits.registry[np.datetime64] = converter
munits.registry[date] = converter
munits.registry[datetime] = converter


def tplot(variables, var_label=None,
                     xsize=None,
                     ysize=None,
                     save_png='', 
                     save_eps='', 
                     save_svg='', 
                     save_pdf='',
                     save_jpeg='',
                     dpi=None,
                     display=True, 
                     fig=None, 
                     axis=None, 
                     pseudo_plot_num=None, 
                     pseudo_right_axis=False,
                     pseudo_yaxis_options=None,
                     pseudo_zaxis_options=None,
                     pseudo_line_options=None,
                     pseudo_extra_options=None,
                     second_axis_size=0.0,
                     slice=False,
                     return_plot_objects=False):
    """
    This function creates tplot windows using matplotlib as a backend.
    """
    tnames = pytplot.tplot_names(quiet=True)
    if isinstance(variables, str):
        # check for wild cards * or ?
        if '*' in variables or '?' in variables:
            variables = tname_filter(tnames, variables)

    if not isinstance(variables, list):
        variables = [variables]

    # support for using the variable # instead of the variable name
    for idx, variable in enumerate(variables):
        if isinstance(variable, int):
            if variable > len(tnames):
                print('Variable not found: ' + str(variable))
            variables[idx] = tnames[variable]

    # support for matplotlib styles
    style = pytplot.tplot_opt_glob.get('style')
    if style is not None:
        plt.style.use(style)

    num_panels = len(variables)
    panel_sizes = [1]*num_panels

    # support for the panel_size option
    for var_idx, variable in enumerate(variables):
        if pytplot.data_quants.get(variable) is None:
            continue
        panel_size = pytplot.data_quants[variable].attrs['plot_options']['extras'].get('panel_size')
        if panel_size is not None:
            panel_sizes[var_idx] = panel_size

    if xsize is None:
        xsize = pytplot.tplot_opt_glob.get('xsize')
        if xsize is None:
            xsize = 8

    if ysize is None:
        ysize = pytplot.tplot_opt_glob.get('ysize')
        if ysize is None:
            ysize = 10

    if fig is None and axis is None:
        fig, axes = plt.subplots(nrows=num_panels, sharex=True, gridspec_kw={'height_ratios': panel_sizes})
        fig.set_size_inches(xsize, ysize)
    else:
        if pseudo_plot_num == 0 or pseudo_right_axis == False:
            # setting up first axis
            axes = axis
        else:
            # using previous axis
            axes = axis.twinx()
    
    plot_title = pytplot.tplot_opt_glob['title_text']
    axis_font_size = pytplot.tplot_opt_glob.get('axis_font_size')
    vertical_spacing = pytplot.tplot_opt_glob.get('vertical_spacing')
    xmargin = pytplot.tplot_opt_glob.get('xmargin')
    ymargin = pytplot.tplot_opt_glob.get('ymargin')
    zrange = [None, None]

    colorbars = {}

    if xmargin is None:
        xmargin = [0.10, 0.05]

    fig.subplots_adjust(left=xmargin[0], right=1-xmargin[1])

    if ymargin is not None:
        fig.subplots_adjust(top=1-ymargin[0], bottom=ymargin[1])

    if vertical_spacing is None:
        vertical_spacing = 0.07
    
    fig.subplots_adjust(hspace=vertical_spacing)
    
    for idx, variable in enumerate(variables):
        var_data_org = pytplot.get_data(variable, dt=True)
        var_metadata = pytplot.get_data(variable, metadata=True)
        
        if var_data_org is None:
            print('Variable not found: ' + variable)
            continue

        var_data = copy.deepcopy(var_data_org)

        # plt.subplots returns a list of axes for multiple panels 
        # but only a single axis for a single panel
        if num_panels == 1:
            this_axis = axes
        else:
            this_axis = axes[idx]

        # we need to track the variable name in the axis object
        # for spectrogram slices
        this_axis.var_name = variable

        pseudo_var = False
        overplots = None
        spec = False

        var_quants = pytplot.data_quants[variable]

        if not isinstance(var_quants, dict):
            if var_quants.attrs['plot_options'].get('overplots_mpl') is not None:
                overplots = var_quants.attrs['plot_options']['overplots_mpl']
                pseudo_var = True

        # deal with pseudo-variables first
        if isinstance(var_data, list) or isinstance(var_data, str) or pseudo_var:
            # this is a pseudo variable
            if isinstance(var_data, str):
                var_data = var_data.split(' ')

            if pseudo_var:
                pseudo_vars = overplots
            else:
                pseudo_vars = var_data

            # pseudo variable metadata should override the metadata
            # for individual variables
            yaxis_options = None
            zaxis_options = None
            line_opts = None
            plot_extras = None
            if pseudo_var:
                plot_extras = var_quants.attrs['plot_options']['extras']
                if plot_extras.get('spec') is not None:
                    spec = True

                if plot_extras.get('right_axis') is not None:
                    if plot_extras.get('right_axis'):
                        pseudo_right_axis = True

                if pseudo_right_axis or spec:
                    plot_extras = None
                else:
                    yaxis_options = var_quants.attrs['plot_options']['yaxis_opt']
                    zaxis_options = var_quants.attrs['plot_options']['zaxis_opt']
                    line_opts = var_quants.attrs['plot_options']['line_opt']

            for pseudo_idx, var in enumerate(pseudo_vars):
                tplot(var, return_plot_objects=return_plot_objects, 
                        xsize=xsize, ysize=ysize, save_png=save_png, 
                        save_eps=save_eps, save_svg=save_svg, save_pdf=save_pdf, 
                        fig=fig, axis=this_axis, display=False, 
                        pseudo_plot_num=pseudo_idx, second_axis_size=0.1,
                        pseudo_yaxis_options=yaxis_options, pseudo_zaxis_options=zaxis_options,
                        pseudo_line_options=line_opts, pseudo_extra_options=plot_extras,
                        pseudo_right_axis=pseudo_right_axis)
            continue

        # set the figure title
        if idx == 0 and plot_title != '':
            this_axis.set_title(plot_title)
        
        # set the x-axis range, if it was set with xlim or tlimit
        if pytplot.tplot_opt_glob.get('x_range') is not None:
            x_range = pytplot.tplot_opt_glob['x_range']

            if isinstance(x_range[0], float):
                if np.isfinite(x_range[0]):
                    x_range[0] = datetime.utcfromtimestamp(x_range[0])
                else:
                    x_range[0] = datetime.utcfromtimestamp(0)

            if isinstance(x_range[1], float):
                if np.isfinite(x_range[1]):
                    x_range[1] = datetime.utcfromtimestamp(x_range[1])
                else:
                    x_range[1] = datetime.utcfromtimestamp(0)

            x_range = np.array(x_range, dtype='datetime64[s]')
            this_axis.set_xlim(x_range)
            time_idxs = np.argwhere((var_data.times >= x_range[0]) & (var_data.times <= x_range[1])).flatten()
            if len(time_idxs) == 0:
                print('No data found in the time range: ' + variable)
                continue
            var_data_times = var_data.times[time_idxs]
        else:
            var_data_times = var_data.times
            time_idxs = np.arange(len(var_data_times))

        # the data are stored as unix times, but matplotlib wants datatime objects
        # var_times = [datetime.fromtimestamp(time, tz=timezone.utc) for time in var_data_times]
        var_times = var_data_times

        # set some more plot options
        yaxis_options = var_quants.attrs['plot_options']['yaxis_opt']
        if pseudo_yaxis_options is not None:
            yaxis_options = pseudo_yaxis_options

        zaxis_options = var_quants.attrs['plot_options']['zaxis_opt']
        if pseudo_zaxis_options is not None:
            zaxis_options = pseudo_zaxis_options

        line_opts = var_quants.attrs['plot_options']['line_opt']
        if pseudo_line_options is not None:
            line_opts = pseudo_line_options

        plot_extras = var_quants.attrs['plot_options']['extras']
        if pseudo_extra_options is not None:
            plot_extras = pseudo_extra_options

        ylog = yaxis_options['y_axis_type']

        if ylog == 'log':
            this_axis.set_yscale('log')
        else:
            this_axis.set_yscale('linear')
            
        ytitle = yaxis_options['axis_label']
        if ytitle == '':
            ytitle = variable
        
        ysubtitle = ''
        if yaxis_options.get('axis_subtitle') is not None:
            ysubtitle = yaxis_options['axis_subtitle']

        # replace some common superscripts
        ysubtitle = replace_common_exp(ysubtitle)

        if axis_font_size is not None:
            this_axis.tick_params(axis='x', labelsize=axis_font_size)
            this_axis.tick_params(axis='y', labelsize=axis_font_size)

        char_size = pytplot.tplot_opt_glob.get('charsize')
        if char_size is None:
            char_size = 12

        if plot_extras.get('char_size') is not None:
            char_size = plot_extras['char_size']

        user_set_yrange = yaxis_options.get('y_range_user')
        if user_set_yrange is not None:
            # the user has set the yrange manually
            yrange = yaxis_options['y_range']
            if not np.isfinite(yrange[0]):
                yrange[0] = None
            if not np.isfinite(yrange[1]):
                yrange[1] = None
            this_axis.set_ylim(yrange)

        if style is None:
            ytitle_color = 'black'
        else:
            ytitle_color = None

        if yaxis_options.get('axis_color') is not None:
            ytitle_color = yaxis_options['axis_color']

        if ytitle_color is not None:
            this_axis.set_ylabel(ytitle + '\n' + ysubtitle, fontsize=char_size, color=ytitle_color)
        else:
            this_axis.set_ylabel(ytitle + '\n' + ysubtitle, fontsize=char_size)

        border = True
        if plot_extras.get('border') is not None:
            border = plot_extras['border']

        if border == False:
            this_axis.axis('off')

        # axis tick options
        if plot_extras.get('xtickcolor') is not None:
            this_axis.tick_params(axis='x', color=plot_extras.get('xtickcolor'))

        if plot_extras.get('ytickcolor') is not None:
            this_axis.tick_params(axis='y', color=plot_extras.get('ytickcolor'))

        if plot_extras.get('xtick_direction') is not None:
            this_axis.tick_params(axis='x', direction=plot_extras.get('xtick_direction'))

        if plot_extras.get('ytick_direction') is not None:
            this_axis.tick_params(axis='y', direction=plot_extras.get('ytick_direction'))

        if plot_extras.get('xtick_length') is not None:
            this_axis.tick_params(axis='x', length=plot_extras.get('xtick_length'))

        if plot_extras.get('ytick_length') is not None:
            this_axis.tick_params(axis='y', length=plot_extras.get('ytick_length'))

        if plot_extras.get('xtick_width') is not None:
            this_axis.tick_params(axis='x', width=plot_extras.get('xtick_width'))

        if plot_extras.get('ytick_width') is not None:
            this_axis.tick_params(axis='y', width=plot_extras.get('ytick_width'))

        if plot_extras.get('xtick_labelcolor') is not None:
            this_axis.tick_params(axis='y', labelcolor=plot_extras.get('xtick_labelcolor'))

        if plot_extras.get('ytick_labelcolor') is not None:
            this_axis.tick_params(axis='y', labelcolor=plot_extras.get('ytick_labelcolor'))

        # determine if this is a line plot or a spectrogram
        spec = False
        if plot_extras.get('spec') is not None:
            spec = plot_extras['spec']

        if spec:
            # create spectrogram plots
            plot_created = specplot(var_data, var_times, this_axis, yaxis_options, zaxis_options, plot_extras, colorbars, axis_font_size, fig, variable, time_idxs=time_idxs, style=style)
            if not plot_created:
                continue
        else:
            # create line plots
            plot_created = lineplot(var_data, var_times, this_axis, line_opts, yaxis_options, plot_extras, pseudo_plot_num=pseudo_plot_num, time_idxs=time_idxs, style=style, var_metadata=var_metadata)
            if not plot_created:
                continue
            
        # apply any vertical bars
        if pytplot.data_quants[variable].attrs['plot_options'].get('time_bar') is not None:
            time_bars = pytplot.data_quants[variable].attrs['plot_options']['time_bar']

            for time_bar in time_bars:
                this_axis.axvline(x=datetime.fromtimestamp(time_bar['location'], tz=timezone.utc), 
                    color=np.array(time_bar.get('line_color'))/256.0, lw=time_bar.get('line_width'))

        # highlight time intervals
        if pytplot.data_quants[variable].attrs['plot_options'].get('highlight_intervals') is not None:
            highlight_intervals = pytplot.data_quants[variable].attrs['plot_options']['highlight_intervals']

            for highlight_interval in highlight_intervals:
                hightlight_opts = copy.deepcopy(highlight_interval)
                del hightlight_opts['location']
                if highlight_interval['edgecolor'] is not None or highlight_interval['facecolor'] is not None:
                    del hightlight_opts['color']

                this_axis.axvspan(mdates.date2num(datetime.utcfromtimestamp(highlight_interval['location'][0])),
                                  mdates.date2num(datetime.utcfromtimestamp(highlight_interval['location'][1])),
                                  **hightlight_opts)

        # add annotations
        if pytplot.tplot_opt_glob.get('annotations') is not None:
            annotations = pytplot.tplot_opt_glob['annotations']
            for annotation in annotations:
                this_axis.annotate(annotation['text'], annotation['position'],
                                   xycoords=annotation['xycoords'],
                                   fontsize=annotation['fontsize'],
                                   alpha=annotation['alpha'],
                                   fontfamily=annotation['fontfamily'],
                                   fontvariant=annotation['fontvariant'],
                                   fontstyle=annotation['fontstyle'],
                                   fontstretch=annotation['fontstretch'],
                                   fontweight=annotation['fontweight'],
                                   rotation=annotation['rotation'],
                                   color=annotation['color'])

    # apply any addition x-axes specified by the var_label keyword
    if var_label is not None:
        if not isinstance(var_label, list):
            var_label = [var_label]

        axis_delta = 0.0

        for label in var_label:
            if isinstance(label, int):
                label = tnames[label]
            label_data = pytplot.get_data(label, xarray=True, dt=True)

            if label_data is None:
                print('Variable not found: ' + label)
                continue

            if len(label_data.values.shape) != 1:
                print(label + ' specified as a vector; var_label only supports scalars. Try splitting the vector into seperate tplot variables.')
                continue

            # set up the new x-axis
            axis_delta = axis_delta - num_panels*0.1
            new_xaxis = this_axis.secondary_xaxis(axis_delta)
            xaxis_ticks = this_axis.get_xticks().tolist()
            xaxis_ticks_dt = [np.datetime64(mpl.dates.num2date(tick_val).isoformat()) for tick_val in xaxis_ticks]
            # xaxis_ticks_unix = [tick_val.timestamp() for tick_val in xaxis_ticks_dt]
            xaxis_labels = get_var_label_ticks(label_data, xaxis_ticks_dt)
            new_xaxis.set_xticks(xaxis_ticks_dt)
            new_xaxis.set_xticklabels(xaxis_labels)
            ytitle = pytplot.data_quants[label].attrs['plot_options']['yaxis_opt']['axis_label']
            new_xaxis.set_xlabel(ytitle)

        fig.subplots_adjust(bottom=0.05+len(var_label)*0.1)

    # add the color bars to any spectra
    for idx, variable in enumerate(variables):
        if pytplot.data_quants.get(variable) is None:
            continue
        plot_extras = pytplot.data_quants[variable].attrs['plot_options']['extras']

        if plot_extras.get('spec') is not None:
            spec = plot_extras['spec']
        else:
            spec = False

        if spec:
            if colorbars.get(variable) is None:
                continue

            # add the color bar
            if pseudo_plot_num == 0:
                # there's going to be a second axis, so we need to make sure there's room for it
                second_axis_size = 0.07

            if num_panels == 1:
                this_axis = axes
            else:
                this_axis = axes[idx]

            fig.subplots_adjust(left=0.14, right=0.87-second_axis_size)
            box = this_axis.get_position()
            pad, width = 0.02, 0.02
            cax = fig.add_axes([box.xmax + pad + second_axis_size, box.ymin, width, box.height])
            if colorbars[variable]['axis_font_size'] is not None:
                cax.tick_params(labelsize=colorbars[variable]['axis_font_size'])
            colorbar = fig.colorbar(colorbars[variable]['im'], cax=cax)

            if style is None:
                ztitle_color = 'black'
            else:
                ztitle_color = None

            if zaxis_options.get('axis_color') is not None:
                ztitle_color = zaxis_options['axis_color']

            ztitle_text = colorbars[variable]['ztitle']
            zsubtitle_text = colorbars[variable]['zsubtitle']

            # replace some common superscripts
            ztitle_text = replace_common_exp(ztitle_text)
            zsubtitle_text = replace_common_exp(zsubtitle_text)

            if ztitle_color is not None:
                colorbar.set_label(ztitle_text + '\n ' + zsubtitle_text,
                                   color=ztitle_color, fontsize=char_size)
            else:
                colorbar.set_label(ztitle_text + '\n ' + zsubtitle_text,
                                   fontsize=char_size)

    if return_plot_objects:
        return fig, axes
    
    if save_png is not None and save_png != '':
        plt.savefig(save_png + '.png', dpi=dpi)

    if save_eps is not None and save_eps != '':
        plt.savefig(save_eps + '.eps', dpi=dpi)

    if save_svg is not None and save_svg != '':
        plt.savefig(save_svg + '.svg', dpi=dpi)

    if save_pdf is not None and save_pdf != '':
        plt.savefig(save_pdf + '.pdf', dpi=dpi)

    if save_jpeg is not None and save_jpeg != '':
        plt.savefig(save_jpeg + '.jpeg', dpi=dpi)

    if slice:
        slice_fig, slice_axes = plt.subplots(nrows=1)
        slice_plot, = slice_axes.plot([0], [0])
        mouse_event_func = lambda event: mouse_move_slice(event, slice_axes, slice_plot)
        cid = fig.canvas.mpl_connect('motion_notify_event', mouse_event_func)

    if display:
        plt.show()


def mouse_move_slice(event, slice_axes, slice_plot):
    """
    This function is called when the mouse moves over an axis
    and the slice keyword is set to True; for spectra figures, it
    updates the slice plot based on the mouse location
    """
    if event.inaxes is None:
        return

    # check for a spectrogram
    try:
        data = pytplot.get_data(event.inaxes.var_name)
    except AttributeError:
        return

    if data is None:
        return

    if len(data) != 3:
        return

    slice_time = mdates.num2date(event.xdata).timestamp()
    idx = np.abs(data.times-slice_time).argmin()

    if len(data.v.shape) > 1:
        # time varying y-axis
        vdata = data.v[idx, :]
    else:
        vdata = data.v

    yaxis_options = pytplot.data_quants[event.inaxes.var_name].attrs['plot_options']['yaxis_opt']
    zaxis_options = pytplot.data_quants[event.inaxes.var_name].attrs['plot_options']['zaxis_opt']

    yrange = yaxis_options.get('y_range')
    if yrange is None:
        yrange = [np.nanmin(vdata), np.nanmax(vdata)]

    zrange = zaxis_options.get('z_range')
    if zrange is None:
        zrange = [np.nanmin(data.y), np.nanmax(data.y)]

    y_label = zaxis_options.get('axis_label')
    if y_label is not None:
        slice_axes.set_ylabel(y_label)

    title = datetime.utcfromtimestamp(data.times[idx]).strftime('%Y-%m-%d %H:%M:%S.%f')

    x_label = yaxis_options.get('axis_label')
    if x_label is not None:
        title = x_label + ' (' + title + ')'

    slice_axes.set_title(title)

    x_subtitle = yaxis_options.get('axis_subtitle')
    if x_subtitle is not None:
        slice_axes.set_xlabel(x_subtitle)

    slice_yaxis_opt = pytplot.data_quants[event.inaxes.var_name].attrs['plot_options'].get('slice_yaxis_opt')

    xscale = None
    yscale = None

    if slice_yaxis_opt is not None:
        xscale = slice_yaxis_opt.get('xi_axis_type')
        yscale = slice_yaxis_opt.get('yi_axis_type')

    if yscale is None:
        # if the user didn't explicitly set the ylog_slice option,
        # use the option from the plot
        yscale = zaxis_options.get('z_axis_type')
        if yscale is None:
            yscale = 'linear'

    if xscale is None:
        # if the user didn't explicitly set the xlog_slice option,
        # use the option from the plot
        xscale = yaxis_options.get('y_axis_type')
        if xscale is None:
            xscale = 'linear'

    if yscale == 'log' and zrange[0] == 0.0:
        zrange[0] = np.nanmin(data.y[idx, :])

    slice_plot.set_data(vdata, data.y[idx, :])
    slice_axes.set_ylim(zrange)
    slice_axes.set_xlim(yrange)
    slice_axes.set_xscale(xscale)
    slice_axes.set_yscale(yscale)

    try:
        plt.draw()
    except ValueError:
        return
    sleep(0.01)


def get_var_label_ticks(var_xr, times):
    out_ticks = []
    for time in times:
        out_ticks.append('{:.2f}'.format(var_xr.interp(coords={'time': time}, kwargs={'fill_value': 'extrapolate', 'bounds_error': False}).values))
    return out_ticks


def replace_common_exp(title):
    if '$' in title:
        return title
    if '^' not in title:
        return title
    exp = False
    title_out = ''
    for char in title:
        if char == '^':
            exp = True
            title_out += '$^{'
            continue
        else:
            if exp:
                if not char.isalnum():
                    title_out += '}$' + char
                    exp = False
                    continue
        title_out += char
    if exp:
        title_out += '}$'
    return title_out


