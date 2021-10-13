
import numpy as np
from scipy.interpolate import interp1d
import matplotlib as mpl
from datetime import date, datetime, timezone
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import warnings
import pytplot

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
                     second_axis_size=0.0,
                     return_plot_objects=False):
    """
    This function creates tplot windows using matplotlib as a backend.
    """
    if not isinstance(variables, list):
        variables = [variables]
        
    num_panels = len(variables)

    if fig is None and axis is None:
        fig, axes = plt.subplots(nrows=num_panels, sharex=True)
        fig.set_size_inches(xsize, ysize)
    else:
        if pseudo_plot_num == 0:
            # setting up first axis
            axes = axis
        else:
            # using previous axis
            axes = axis.twinx()
    
    plot_title = pytplot.tplot_opt_glob['title_text']
    axis_font_size = pytplot.tplot_opt_glob.get('axis_font_size')
    zrange = [None, None]
    
    for idx, variable in enumerate(variables):
        var_data = pytplot.get_data(variable)
        
        if var_data is None:
            print('Variable not found: ' + variable)
            continue

        # plt.subplots returns a list of axes for multiple panels 
        # but only a single axis for a single panel
        if num_panels == 1:
            this_axis = axes
        else:
            this_axis = axes[idx]

        # deal with pseudo-variables first
        if isinstance(var_data, list) or isinstance(var_data, str):
            # this is a pseudo variable
            if not isinstance(var_data, list):
                var_data = var_data.split(' ')

            for pseudo_idx, var in enumerate(var_data):
                tplot(var, return_plot_objects=return_plot_objects, 
                    xsize=xsize, ysize=ysize, save_png=save_png, 
                    save_eps=save_eps, save_svg=save_svg, save_pdf=save_pdf, 
                    fig=fig, axis=this_axis, display=False, 
                    pseudo_plot_num=pseudo_idx, second_axis_size=0.1)
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
        yaxis_options = pytplot.data_quants[variable].attrs['plot_options']['yaxis_opt']
        zaxis_options = pytplot.data_quants[variable].attrs['plot_options']['zaxis_opt']
        line_opts = pytplot.data_quants[variable].attrs['plot_options']['line_opt']
        plot_extras = pytplot.data_quants[variable].attrs['plot_options']['extras']

        ylog = yaxis_options['y_axis_type']
        if ylog == 'log':
            this_axis.set_yscale('log')
        else:
            this_axis.set_yscale('linear')
            
        ytitle = yaxis_options['axis_label']
        if ytitle == '':
            ytitle = variable
        
        if yaxis_options.get('axis_subtitle') is not None:
            ysubtitle = yaxis_options['axis_subtitle']
        else:
            ysubtitle = ''
            
        if axis_font_size is not None:
            this_axis.tick_params(axis='x', labelsize=axis_font_size)
            this_axis.tick_params(axis='y', labelsize=axis_font_size)

        yrange = yaxis_options['y_range']
        this_axis.set_ylim(yrange)
        this_axis.set_ylabel(ytitle + '\n' + ysubtitle)

        if plot_extras.get('alpha') is not None:
            alpha = plot_extras['alpha']
        else:
            alpha = None

        # determine if this is a line plot or a spectrogram
        if plot_extras.get('spec') is not None:
            spec = plot_extras['spec']
        else:
            spec = False

        if not spec:
            # create line plots
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
                else:
                    colors = ['k', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']

                if num_lines >= len(colors):
                    colors = colors*num_lines

            # line thickness
            if line_opts.get('line_width') is not None:
                thick = line_opts['line_width']
            else:
                thick = 1

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

            # create the plot
            line_options = {'linewidth': thick, 'linestyle': line_style, 'alpha': alpha}

            # check for error data first
            if 'dy' in var_data._fields:
                # error data provided
                line_options['yerr'] = var_data.dy
                plotter = this_axis.errorbar
            else:
                # no error data provided
                plotter = this_axis.plot

            for line in range(0, num_lines):
                this_line = plotter(var_times, var_data.y if num_lines == 1 else var_data.y[:, line], color=colors[line], **line_options)

                if labels is not None:
                    if isinstance(this_line, list):
                        this_line[0].set_label(labels[line])
                    else:
                        this_line.set_label(labels[line])

            if labels is not None:
                this_axis.legend()
        else:
            # create spectrogram plots
            spec_options = {'shading': 'auto', 'alpha': alpha}
            ztitle = zaxis_options['axis_label']
            zlog = zaxis_options['z_axis_type']

            if zaxis_options.get('z_range') is not None:
                zrange = zaxis_options['z_range']
                
            if zaxis_options.get('axis_subtitle') is not None:
                zsubtitle = zaxis_options['axis_subtitle']
            else:
                zsubtitle = ''
            
            if zlog == 'log':
                spec_options['norm'] = mpl.colors.LogNorm(vmin=zrange[0], vmax=zrange[1])
            else:
                spec_options['norm'] = None
                spec_options['vmin'] = zrange[0]
                spec_options['vmax'] = zrange[1]
            
            if plot_extras.get('colormap') is not None:
                cmap = plot_extras['colormap'][0]
            else:
                cmap = 'spedas'
            
            # kludge to add support for the 'spedas' color bar
            if cmap == 'spedas':
                _colors = pytplot.spedas_colorbar
                spd_map = [(np.array([r, g, b])).astype(np.float64)/256 for r, g, b in zip(_colors.r, _colors.g, _colors.b)]
                cmap = LinearSegmentedColormap.from_list('spedas', spd_map)
                
            spec_options['cmap'] = cmap

            out_values = var_data.y
            out_vdata = var_data.v

            # automatic interpolation options
            if yaxis_options.get('x_interp') is not None:
                x_interp = yaxis_options['x_interp']

                # interpolate along the x-axis
                if x_interp:
                    if yaxis_options.get('x_interp_points') is not None:
                        nx = yaxis_options['x_interp_points']
                    else:
                        fig_size = fig.get_size_inches()*fig.dpi
                        nx = fig_size[0]

                    if zlog:
                        zdata = np.log10(out_values)
                    else:
                        zdata = out_values

                    zdata[zdata < 0.0] = 0.0
                    zdata[zdata == np.nan] = 0.0

                    interp_func = interp1d(var_data.times, zdata, axis=0, fill_value=np.nan, bounds_error=False)
                    out_times = np.arange(0, nx, dtype=np.float64)*(var_data.times[-1]-var_data.times[0])/(nx-1) + var_data.times[0]

                    out_values = interp_func(out_times)

                    if zlog:
                        out_values = 10**out_values

                    var_times = [datetime.fromtimestamp(time, tz=timezone.utc) for time in out_times]

            if yaxis_options.get('y_interp') is not None:
                y_interp = yaxis_options['y_interp']

                # interpolate along the y-axis
                if y_interp:
                    if yaxis_options.get('y_interp_points') is not None:
                        ny = yaxis_options['y_interp_points']
                    else:
                        fig_size = fig.get_size_inches()*fig.dpi
                        ny = fig_size[1]

                    if zlog:
                        zdata = np.log10(out_values)
                    else:
                        zdata = out_values

                    if ylog:
                        vdata = np.log10(var_data.v)
                        ycrange = np.log10(yrange)
                    else:
                        vdata = var_data.v
                        ycrange = yrange

                    if not np.isfinite(ycrange[0]):
                        ycrange = [np.min(vdata), yrange[1]]

                    zdata[zdata < 0.0] = 0.0
                    zdata[zdata == np.nan] = 0.0

                    interp_func = interp1d(vdata, zdata, axis=1, fill_value=np.nan, bounds_error=False)
                    out_vdata = np.arange(0, ny, dtype=np.float64)*(ycrange[1]-ycrange[0])/(ny-1) + ycrange[0]

                    out_values = interp_func(out_vdata)

                    if zlog:
                        out_values = 10**out_values

                    if ylog:
                        out_vdata = 10**out_vdata

            # create the spectrogram (ignoring warnings)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                im = this_axis.pcolormesh(var_times, out_vdata.T, out_values.T, **spec_options)
            
            # add the color bar
            if pseudo_plot_num == 0:
                # there's going to be a second axis, so we need to make sure there's room for it
                second_axis_size = 0.07

            fig.subplots_adjust(left=0.14, right=0.87-second_axis_size)
            box = this_axis.get_position()
            pad, width = 0.02, 0.02
            cax = fig.add_axes([box.xmax + pad + second_axis_size, box.ymin, width, box.height])
            if axis_font_size is not None:
                cax.tick_params(labelsize=axis_font_size)
            fig.colorbar(im, cax=cax, label=ztitle + '\n ' + zsubtitle)

        # apply any vertical bars
        if pytplot.data_quants[variable].attrs['plot_options'].get('time_bar') is not None:
            time_bars = pytplot.data_quants[variable].attrs['plot_options']['time_bar']

            for time_bar in time_bars:
                this_axis.axvline(x=datetime.fromtimestamp(time_bar['location'], tz=timezone.utc), 
                    color=np.array(time_bar.get('line_color'))/256.0, lw=time_bar.get('line_width'))
    
    # apply any addition x-axes specified by the var_label keyword
    if var_label is not None:
        if not isinstance(var_label, list):
            var_label = [var_label]

        axis_delta = 0.0

        for label in var_label:
            label_data = pytplot.get_data(label, xarray=True)

            if label_data is None:
                print('Variable not found: ' + label)
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

    if return_plot_objects:
        return fig, axes
    
    if save_png != '':
        plt.savefig(save_png + '.png')

    if save_eps != '':
        plt.savefig(save_eps + '.eps')

    if save_svg != '':
        plt.savefig(save_svg + '.svg')

    if save_pdf != '':
        plt.savefig(save_pdf + '.pdf')

    if display:
        plt.show()

def get_var_label_ticks(var_xr, times):
    out_ticks = []
    for time in times:
        out_ticks.append('{:.2f}'.format(var_xr.interp({'time': time}).values))
    return out_ticks
