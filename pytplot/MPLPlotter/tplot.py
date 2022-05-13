import copy
import numpy as np
import matplotlib as mpl
from datetime import date, datetime, timezone
from matplotlib import pyplot as plt
import pytplot
from fnmatch import filter as tname_filter

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
                     xsize=8, 
                     ysize=10, 
                     save_png='', 
                     save_eps='', 
                     save_svg='', 
                     save_pdf='', 
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
        
    num_panels = len(variables)
    panel_sizes = [1]*num_panels

    # support for the panel_size option
    for var_idx, variable in enumerate(variables):
        if pytplot.data_quants.get(variable) is None:
            continue
        panel_size = pytplot.data_quants[variable].attrs['plot_options']['extras'].get('panel_size')
        if panel_size is not None:
            panel_sizes[var_idx] = panel_size

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
        var_data_org = pytplot.get_data(variable)
        
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

        # the data are stored as unix times, but matplotlib wants datatime objects
        var_times = [datetime.fromtimestamp(time, tz=timezone.utc) for time in var_data.times]
        
        # set the figure title
        if idx == 0 and plot_title != '':
            this_axis.set_title(plot_title)
        
        # set the x-axis range, if it was set with xlim or tlimit
        if pytplot.tplot_opt_glob.get('x_range') is not None:
            x_range = pytplot.tplot_opt_glob['x_range']
            this_axis.set_xlim([datetime.fromtimestamp(x_range[0], tz=timezone.utc), datetime.fromtimestamp(x_range[1], tz=timezone.utc)])

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
            
        if axis_font_size is not None:
            this_axis.tick_params(axis='x', labelsize=axis_font_size)
            this_axis.tick_params(axis='y', labelsize=axis_font_size)

        char_size = 14
        if plot_extras.get('char_size') is not None:
            char_size = plot_extras['char_size']

        yrange = yaxis_options['y_range']
        if not np.isfinite(yrange[0]):
            yrange[0] = None
        if not np.isfinite(yrange[1]):
            yrange[1] = None

        this_axis.set_ylim(yrange)

        ytitle_color = 'black'
        if yaxis_options.get('axis_color') is not None:
            ytitle_color = yaxis_options['axis_color']

        this_axis.set_ylabel(ytitle + '\n' + ysubtitle, fontsize=char_size, color=ytitle_color)

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
            plot_created = specplot(var_data, var_times, this_axis, yaxis_options, zaxis_options, plot_extras, colorbars, axis_font_size, fig, variable)
            if not plot_created:
                continue
        else:
            # create line plots
            plot_created = lineplot(var_data, var_times, this_axis, line_opts, yaxis_options, plot_extras, pseudo_plot_num=pseudo_plot_num)
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
            label_data = pytplot.get_data(label, xarray=True)

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
            xaxis_ticks_dt = [mpl.dates.num2date(tick_val) for tick_val in xaxis_ticks]
            xaxis_ticks_unix = [tick_val.timestamp() for tick_val in xaxis_ticks_dt]
            xaxis_labels = get_var_label_ticks(label_data, xaxis_ticks_unix)
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

            ztitle_color = 'black'
            if zaxis_options.get('axis_color') is not None:
                ztitle_color = zaxis_options['axis_color']

            colorbar.set_label(colorbars[variable]['ztitle'] + '\n ' + colorbars[variable]['zsubtitle'], color=ztitle_color, fontsize=char_size)

    if return_plot_objects:
        return fig, axes
    
    if save_png is not None and save_png != '':
        plt.savefig(save_png + '.png')

    if save_eps is not None and save_eps != '':
        plt.savefig(save_eps + '.eps')

    if save_svg is not None and save_svg != '':
        plt.savefig(save_svg + '.svg')

    if save_pdf is not None and save_pdf != '':
        plt.savefig(save_pdf + '.pdf')

    if display:
        plt.show()

def get_var_label_ticks(var_xr, times):
    out_ticks = []
    for time in times:
        out_ticks.append('{:.2f}'.format(var_xr.interp(coords={'time': time}, kwargs={'fill_value': 'extrapolate', 'bounds_error': False}).values))
    return out_ticks
