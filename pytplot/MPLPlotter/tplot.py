
import numpy as np
import matplotlib as mpl
from datetime import datetime, timezone
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pytplot

def tplot(variables, return_plot_objects=False, xsize=8, ysize=10, save_png='', save_eps='', save_svg='', save_pdf=''):
    """
    This function creates tplot windows using matplotlib as a backend.
    """
    if not isinstance(variables, list):
        variables = [variables]
        
    num_panels = len(variables)
    fig, axes = plt.subplots(nrows=num_panels, sharex=True)
        
    fig.set_size_inches(xsize, ysize)
    
    plot_title = pytplot.tplot_opt_glob['title_text']
    axis_font_size = pytplot.tplot_opt_glob.get('axis_font_size')
    
    for idx, variable in enumerate(variables):
        var_data = pytplot.get_data(variable)
        
        if var_data is None:
            print('Variable not found: ' + variable)
            continue

        # the data are stored as unix times, but matplotlib wants datatime objects
        var_times = [datetime.fromtimestamp(time, tz=timezone.utc) for time in var_data.times]
        
        if num_panels == 1:
            this_axis = axes
        else:
            this_axis = axes[idx]
        
        # set the figure title
        if idx == 0 and plot_title != '':
            this_axis.set_title(plot_title)
        
        # determine if this is a line plot or a spectrogram
        if pytplot.data_quants[variable].attrs['plot_options']['extras'].get('spec') is not None:
            spec = pytplot.data_quants[variable].attrs['plot_options']['extras']['spec']
        else:
            spec = False

        if not spec:
            # line plots
            if pytplot.data_quants[variable].attrs['plot_options']['yaxis_opt'].get('legend_names') is not None:
                labels = pytplot.data_quants[variable].attrs['plot_options']['yaxis_opt']['legend_names']
            else:
                labels = None
            
            if len(var_data.y.shape) == 1:
                num_lines = 1
            else:
                num_lines = var_data.y.shape[1]

            # set up line colors
            if pytplot.data_quants[variable].attrs['plot_options']['extras'].get('line_color') is not None:
                colors = pytplot.data_quants[variable].attrs['plot_options']['extras']['line_color']
            else:
                if num_lines == 3:
                    colors = ['b', 'g', 'r']
                else:
                    colors = ['k', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']

                if num_lines >= len(colors):
                    colors = colors*num_lines

            # create the plot
            if num_lines == 1:
                this_line, = this_axis.plot(var_times, var_data.y, linewidth=0.5, color=colors[0])
                if labels is not None:
                    this_line.set_label(labels[line])
            else:
                for line in range(0, num_lines):
                    this_line, = this_axis.plot(var_times, var_data.y[:, line], linewidth=0.5, color=colors[line])
                    if labels is not None:
                        this_line.set_label(labels[line])
            if labels is not None:
                this_axis.legend()
        else:
            # spectrogram plots
            ztitle = pytplot.data_quants[variable].attrs['plot_options']['zaxis_opt']['axis_label']
            zlog = pytplot.data_quants[variable].attrs['plot_options']['zaxis_opt']['z_axis_type']
            if pytplot.data_quants[variable].attrs['plot_options']['zaxis_opt'].get('z_range') is not None:
                zrange = pytplot.data_quants[variable].attrs['plot_options']['zaxis_opt']['z_range']
            else:
                zrange = [None, None]
                
            if pytplot.data_quants[variable].attrs['plot_options']['zaxis_opt'].get('axis_subtitle') is not None:
                zsubtitle = pytplot.data_quants[variable].attrs['plot_options']['zaxis_opt']['axis_subtitle']
            else:
                zsubtitle = ''
                
            if zlog == 'log':
                norm = mpl.colors.LogNorm()
            else:
                norm = None
            
            if pytplot.data_quants[variable].attrs['plot_options']['extras'].get('colormap') is not None:
                cmap = pytplot.data_quants[variable].attrs['plot_options']['extras']['colormap'][0]
            else:
                cmap = 'spedas'
            
            # kludge to add support for the 'spedas' color bar
            if cmap == 'spedas':
                spedas_colors = pytplot.spedas_colorbar
                spd_map = [(np.array([r, g, b])).astype(np.float64)/256 for r, g, b in zip(spedas_colors.r, spedas_colors.g, spedas_colors.b)]
                cmap = LinearSegmentedColormap.from_list('spedas', spd_map)
                
            # create the spectrogram
            var_x, var_v = np.meshgrid(var_data.times, var_data.v)
            im = this_axis.pcolormesh(var_times, var_data.v.T, var_data.y.T, 
                                      cmap=cmap, 
                                      norm=norm, 
                                      shading='auto', 
                                      vmin=zrange[0],
                                      vmax=zrange[1])
            
            # add the color bar
            fig.subplots_adjust(left=0.14, right=0.87)
            box = this_axis.get_position()
            pad, width = 0.02, 0.02
            cax = fig.add_axes([box.xmax + pad, box.ymin, width, box.height])
            if axis_font_size is not None:
                cax.tick_params(labelsize=axis_font_size)
            fig.colorbar(im, cax=cax, label=ztitle + '\n ' + zsubtitle)
        
        # set some more plot options
        ylog = pytplot.data_quants[variable].attrs['plot_options']['yaxis_opt']['y_axis_type']
        if ylog == 'log':
            this_axis.set_yscale('log')
        else:
            this_axis.set_yscale('linear')
            
        ytitle = pytplot.data_quants[variable].attrs['plot_options']['yaxis_opt']['axis_label']
        if ytitle == '':
            ytitle = variable
        
        if pytplot.data_quants[variable].attrs['plot_options']['yaxis_opt'].get('axis_subtitle') is not None:
            ysubtitle = pytplot.data_quants[variable].attrs['plot_options']['yaxis_opt']['axis_subtitle']
        else:
            ysubtitle = ''
            
        if axis_font_size is not None:
            this_axis.tick_params(axis='x', labelsize=axis_font_size)
            this_axis.tick_params(axis='y', labelsize=axis_font_size)

        if pytplot.tplot_opt_glob.get('x_range') is not None:
            x_range = pytplot.tplot_opt_glob['x_range']
            this_axis.set_xlim([datetime.fromtimestamp(x_range[0], tz=timezone.utc), datetime.fromtimestamp(x_range[1], tz=timezone.utc)])

        yrange = pytplot.data_quants[variable].attrs['plot_options']['yaxis_opt']['y_range']
        this_axis.set_ylim(yrange)
        this_axis.set_ylabel(ytitle + '\n' + ysubtitle)

        # apply any vertical bars
        if pytplot.data_quants[variable].attrs['plot_options'].get('time_bar') is not None:
            time_bars = pytplot.data_quants[variable].attrs['plot_options']['time_bar']

            for time_bar in time_bars:
                plt.axvline(x=datetime.fromtimestamp(time_bar['location'], tz=timezone.utc), color=np.array(time_bar.get('line_color'))/256.0, lw=time_bar.get('line_width'))
    
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

    plt.show()
