# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import pytplot
from bokeh.models import LinearAxis, Range1d
from .CustomModels.timestamp import TimeStamp
from bokeh.layouts import gridplot
from bokeh.io import doc
import numpy as np


def generate_stack(name, 
                   var_label=None,
                   auto_color=True, 
                   combine_axes=True,
                   slice=True,
                   vert_spacing=25):
    
    doc.curdoc().clear()
    num_plots = len(name)
    
    # Name for .html file containing plots
    out_name = ""
    
    if isinstance(var_label, int):
        var_label = list(pytplot.data_quants.keys())[var_label]
    
    # Vertical Box layout to store plots
    all_plots = []
    axis_types = []
    i = 0
    
    # Configure plot sizes
    total_psize = 0
    j = 0
    while j < num_plots:
        total_psize += pytplot.data_quants[name[j]].attrs['plot_options']['extras']['panel_size']
        j += 1
    
    p_to_use = pytplot.tplot_opt_glob['window_size'][1]/total_psize

    # Create all plots  
    while i < num_plots:
        last_plot = (i == num_plots-1)
        
        p_height = int(pytplot.data_quants[name[i]].attrs['plot_options']['extras']['panel_size'] * p_to_use)
        p_width = pytplot.tplot_opt_glob['window_size'][0]
        
        # Check plot type
        new_fig = _get_figure_class(name[i], auto_color=auto_color, slice=slice, show_xaxis=last_plot)
        
        new_fig.setsize(height=p_height, width=p_width)

        if i == 0:
            new_fig.add_title()
            
        axis_types.append(new_fig.getaxistype())
        
        new_fig.buildfigure()

        # Change background color to black if option for it is set - CHECK ONCE WE'VE UPGRADED OUR BOKEH THAT THIS IS
        # THE RIGHT WAY TO DO THIS
        if pytplot.tplot_opt_glob['black_background']:
            new_fig.background_fill_color = '#000000'
        else:
            new_fig.background_fill_color = '#FFFFFF'
            
        # Add name of variable to output file name
        if last_plot:    
            out_name += name[i]
        else:
            out_name += name[i] + '+'
            
        # Add plot to GridPlot layout
        all_plots.append(new_fig.getfig())
        i = i+1
    
    # Add the time stamp to the stack
    total_string = ""
    if 'time_stamp' in pytplot.extra_layouts:
        total_string = pytplot.extra_layouts['time_stamp']
    
    ts = TimeStamp(text=total_string)
    pytplot.extra_layouts['data_time'] = ts
    all_plots.append([pytplot.extra_layouts['data_time']])
        
    # Add extra x axes if applicable
    if var_label is not None:
        if not isinstance(var_label, list):
            var_label = [var_label]
        x_axes = []
        x_axes_index = 0
        for new_x_axis in var_label:
            # TODO: Bokeh only handles linear plots for now!!! Fix?!
            axis_data_quant = pytplot.data_quants[new_x_axis]
            axis_start = np.float(axis_data_quant.min(skipna=True).values)
            axis_end = np.float(axis_data_quant.max(skipna=True).values)
            x_axes.append(Range1d(start=axis_start, end=axis_end))
            k = 0
            while k < num_plots:
                all_plots[k][0].extra_x_ranges['extra_'+str(new_x_axis)] = x_axes[x_axes_index]
                k += 1
            all_plots[k-1][0].add_layout(LinearAxis(x_range_name='extra_'+str(new_x_axis)), 'below')
            all_plots[k-1][0].plot_height += 22
            x_axes_index += 1
    
    # Set all plots' x_range and plot_width to that of the bottom plot
    #     so all plots will pan and be resized together.
    first_type = {}
    if combine_axes:
        k = 0
        while k < len(axis_types):
            if axis_types[k][0] not in first_type:
                first_type[axis_types[k][0]] = k
            else:
                all_plots[k][0].x_range = all_plots[first_type[axis_types[k][0]]][0].x_range
                if axis_types[k][1]:
                    all_plots[k][0].y_range = all_plots[first_type[axis_types[k][0]]][0].y_range
            k += 1
    
    return gridplot(all_plots)


def _get_figure_class(tvar_name, auto_color=True, slice=False, show_xaxis=True):
    if 'plotter' in pytplot.data_quants[tvar_name].attrs['plot_options']['extras'] \
            and pytplot.data_quants[tvar_name].attrs['plot_options']['extras']['plotter'] in pytplot.bokeh_plotters:
        cls = pytplot.bokeh_plotters[pytplot.data_quants[tvar_name].attrs['plot_options']['extras']['plotter']]
    else:
        spec_keyword = pytplot.data_quants[tvar_name].attrs['plot_options']['extras'].get('spec', False)
        alt_keyword = pytplot.data_quants[tvar_name].attrs['plot_options']['extras'].get('alt', False)
        map_keyword = pytplot.data_quants[tvar_name].attrs['plot_options']['extras'].get('map', False)
        if spec_keyword:
            cls = pytplot.bokeh_plotters['bkTVarFigureSpec']
        elif alt_keyword:
            cls = pytplot.bokeh_plotters['bkTVarFigureAlt']
        elif map_keyword:
            cls = pytplot.bokeh_plotters['bkTVarFigureMap']
        else:
            cls = pytplot.bokeh_plotters['bkTVarFigure1D']
    return cls(tvar_name, auto_color=auto_color, slice=slice, show_xaxis=show_xaxis)
