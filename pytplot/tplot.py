# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import os 
from bokeh.io import output_file, show, output_notebook
from bokeh.models import LinearAxis, Range1d
from .tplot_directory import get_tplot_directory
from . import tplot_common
from .timestamp import TimeStamp
from bokeh.layouts import gridplot
from .TVarFigure1D import TVarFigure1D
from .TVarFigure2D import TVarFigure2D
from .TVarFigureSpec import TVarFigureSpec
from .TVarFigureAlt import TVarFigureAlt

def tplot(name, var_label = None, auto_color=True, interactive=False, nb=False, combine_axes=True):

    # Name for .html file containing plots
    out_name = ""
    
    #Check a bunch of things
    if(not isinstance(name, list)):
        name=[name]
        num_plots = 1
    else:
        num_plots = len(name)
    
    for i in range(num_plots):
        if isinstance(name[i], int):
            name[i] = list(tplot_common.data_quants.keys())[name[i]]
        if name[i] not in tplot_common.data_quants.keys():
            print(str(i) + " is currently not in pytplot")
            return
    
    if isinstance(var_label, int):
        var_label = list(tplot_common.data_quants.keys())[var_label]
    
    # Vertical Box layout to store plots
    all_plots = []
    axis_types=[]
    i = 0
    
    # Configure plot sizes
    total_psize = 1
    j = 0
    while(j < num_plots):
        total_psize += tplot_common.data_quants[name[j]].extras['panel_size']
        j += 1
    p_to_use = tplot_common.tplot_opt_glob['window_size'][1]/total_psize
    
    # Create all plots  
    while(i < num_plots):
        last_plot = (i == num_plots-1)
        temp_data_quant = tplot_common.data_quants[name[i]]
        
        p_height = int(temp_data_quant.extras['panel_size'] * p_to_use)
        p_width = tplot_common.tplot_opt_glob['window_size'][0]
        
        #Check plot type
        has_spec_bins = (temp_data_quant.spec_bins is not None)
        has_spec_keyword = ('spec' in temp_data_quant.extras.keys())
        has_alt_keyword = ('alt' in temp_data_quant.extras.keys())
        has_map_keyword = ('map' in temp_data_quant.extras.keys())
        if has_spec_bins and has_spec_keyword:
            spec_keyword = temp_data_quant.extras['spec']
        else:
            spec_keyword = False
        if has_alt_keyword:
            alt_keyword = temp_data_quant.extras['alt']
        else:
            alt_keyword = False
        if has_map_keyword:
            map_keyword = temp_data_quant.extras['map']
        else:
            map_keyword = False
        
        if spec_keyword:     
            new_fig = TVarFigureSpec(temp_data_quant, interactive=interactive, last_plot=last_plot)
        elif alt_keyword:
            new_fig = TVarFigureAlt(temp_data_quant, auto_color=auto_color, interactive=interactive, last_plot=last_plot)
        elif map_keyword:    
            new_fig = TVarFigure2D(temp_data_quant, interactive=interactive, last_plot=last_plot)
        else:
            new_fig = TVarFigure1D(temp_data_quant, auto_color=auto_color, interactive=interactive, last_plot=last_plot)
            
        axis_types.append(new_fig.getaxistype())
        
        new_fig.setsize(height=p_height, width=p_width) 
        if i == 0:
            new_fig.add_title()
        
        new_fig.buildfigure()
        
            
        # Add name of variable to output file name
        if last_plot:    
            out_name += temp_data_quant.name
        else:
            out_name += temp_data_quant.name + '+'
        # Add plot to GridPlot layout
        all_plots.append(new_fig.getfig())
        i = i+1
    # Add date of data to the bottom left corner and timestamp to lower right
    # if py_timestamp('on') was previously called
    total_string = ""
    if 'time_stamp' in tplot_common.extra_layouts:
        total_string = tplot_common.extra_layouts['time_stamp']
    
    ts = TimeStamp(text = total_string)
    tplot_common.extra_layouts['data_time'] = ts
    all_plots.append([tplot_common.extra_layouts['data_time']])
        
    # Set all plots' x_range and plot_width to that of the bottom plot
    #     so all plots will pan and be resized together.
    first_type = {}
    if combine_axes:
        k=0
        while(k < num_plots):
            if axis_types[k][0] not in first_type:
                first_type[axis_types[k][0]] = k
            else:
                all_plots[k][0].x_range = all_plots[first_type[axis_types[k][0]]][0].x_range
                if axis_types[k][1]:
                    all_plots[k][0].y_range = all_plots[first_type[axis_types[k][0]]][0].y_range
            k+=1
    
    #Add extra x axes if applicable 
    if var_label is not None:
        if not isinstance(var_label, list):
            var_label = [var_label]
        x_axes = []
        x_axes_index = 0
        for new_x_axis in var_label:
            
            axis_data_quant = tplot_common.data_quants[new_x_axis]
            axis_start = min(axis_data_quant.data.min(skipna=True).tolist())
            axis_end = max(axis_data_quant.data.max(skipna=True).tolist())
            x_axes.append(Range1d(start = axis_start, end = axis_end))
            k = 0
            while(k < num_plots ):
                all_plots[k][0].extra_x_ranges['extra_'+str(new_x_axis)] = x_axes[x_axes_index]
                k += 1
            all_plots[k-1][0].add_layout(LinearAxis(x_range_name = 'extra_'+str(new_x_axis)), 'below')
            all_plots[k-1][0].plot_height += 22
            x_axes_index += 1
    
    # Add toolbar and title (if applicable) to top plot.        
    final = gridplot(all_plots)
    
    
    if 'title_text' in tplot_common.tplot_opt_glob:
        if tplot_common.tplot_opt_glob['title_text'] != '':
            out_name = tplot_common.tplot_opt_glob['title_text']+'.html'
        else:
            out_name += '.html'
    else:
        out_name += '.html'
    
    if nb:
        output_notebook()
    else:
        output_file(os.path.join(get_tplot_directory(),out_name))
    
    show(final)    
    return

    
