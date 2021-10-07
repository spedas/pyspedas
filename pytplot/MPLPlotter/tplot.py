
import numpy as np
import matplotlib as mpl
from datetime import datetime, timezone
from matplotlib import pyplot as plt
import pytplot

def tplot(variables, return_plot_objects=False, xsize=8, ysize=10):
    """
    This function creates tplot windows using matplotlib as a backend.
    """
    if not isinstance(variables, list):
        variables = [variables]
        
    num_panels = len(variables)
    fig, axes = plt.subplots(nrows=num_panels, sharex=True)
        
    fig.set_size_inches(xsize, ysize)
    
    plot_title = pytplot.tplot_opt_glob['title_text']
    
    for idx, variable in enumerate(variables):
        var_data = pytplot.get_data(variable)
        var_metadata = pytplot.get_data(variable, metadata=True)
        
        if var_data is None:
            print('Variable not found: ' + variable)
            continue

        var_times = [datetime.fromtimestamp(time, tz=timezone.utc) for time in var_data.times]
        
        if num_panels == 1:
            this_axis = axes
        else:
            this_axis = axes[idx]
        
        if idx == 0 and plot_title != '':
            this_axis.set_title(plot_title)
        
        if len(var_data) == 2:
            # line plots
            if pytplot.data_quants[variable].attrs['plot_options']['yaxis_opt'].get('legend_names') is not None:
                labels = pytplot.data_quants[variable].attrs['plot_options']['yaxis_opt']['legend_names']
            else:
                labels = None
            
            if len(var_data.y.shape) == 1:
                this_axis.plot(var_times, var_data.y, linewidth=0.5, color='k')
            else:
                num_lines = var_data.y.shape[1]
                if num_lines == 3:
                    colors = ['b', 'g', 'r']
                else:
                    colors = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']

                if num_lines >= len(colors):
                    colors = colors*num_lines
                
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
                cmap = 'turbo'
            
            # kludge because the 'spedas' color bar isn't here yet
            if cmap == 'spedas':
                cmap = 'turbo'
                
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
            fig.colorbar(im, cax=cax, label=ztitle + '\n ' + zsubtitle)
        
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
            
        yrange = pytplot.data_quants[variable].attrs['plot_options']['yaxis_opt']['y_range']
        
        this_axis.set_ylim(yrange)
        this_axis.set_ylabel(ytitle + '\n' + ysubtitle)
    
    if return_plot_objects:
        return fig, axes
    
    plt.show()
    
