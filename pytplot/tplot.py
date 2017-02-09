from __future__ import division
import datetime
import numpy as np
import math
import os 
from bokeh.io import output_file, show, gridplot, output_notebook
from bokeh.plotting.figure import Figure
from bokeh.layouts import gridplot, widgetbox, layout
from bokeh.models import (CustomJS, Label, LogColorMapper, LogTicker, ColorBar, LinearColorMapper, 
                          BasicTicker, ColumnDataSource, DatetimeAxis, HoverTool, LinearAxis, 
                          Range1d, Span, Title, Legend, LogAxis)
from bokeh.models.glyphs import Line
from bokeh.models.tools import BoxZoomTool
from bokeh.models.formatters import BasicTickFormatter

from . import tplot_common
from .timestamp import TimeStamp
from .colorbarsidetitle import ColorBarSideTitle
from . import tplot_utilities
from .tplot_directory import get_tplot_directory
from bokeh.models.formatters import DatetimeTickFormatter

dttf = DatetimeTickFormatter(microseconds=["%H:%M:%S"],                        
            milliseconds=["%H:%M:%S"],
            seconds=["%H:%M:%S"],
            minsec=["%H:%M:%S"],
            minutes=["%H:%M:%S"],
            hourmin=["%H:%M:%S"],
            hours=["%H:%M"],
            days=["%F"],
            months=["%F"],
            years=["%F"])

def tplot(name, var_label = None, auto_color=True, interactive=False, nb=False):

    # Name for .html file containing plots
    out_name = ""
    
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
    #all_plots.append([dim_width, dim_height])
    #all_plots.append([dim_height])
    i = 0
    
    # Configure plot sizes
    total_psize = 0
    j = 0
    while(j < num_plots):
        total_psize += tplot_common.data_quants[name[j]]['extras']['panel_size']
        j += 1
    p_to_use = tplot_common.tplot_opt_glob['window_size'][1]/total_psize
    
    # Create all plots  
    while(i < num_plots):
        interactive_plot=None
        
        temp_data_quant = tplot_common.data_quants[name[i]]
        
        #There could be multiple datasets if we are overplotting
        datasets = []
        if isinstance(temp_data_quant['data'], list):
            for oplot_name in temp_data_quant['data']:
                datasets.append(tplot_common.data_quants[oplot_name]['data'])
        else:
            datasets.append(temp_data_quant['data'])
            
        yaxis_opt = temp_data_quant['yaxis_opt']
        line_opt = temp_data_quant['line_opt']
        
        p_height = int(temp_data_quant['extras']['panel_size'] * p_to_use)
        p_width = tplot_common.tplot_opt_glob['window_size'][0]
        
        #Check if we're doing a spec plot
        has_spec_bins = (temp_data_quant['spec_bins'] is not None)
        has_spec_keyword = ('spec' in temp_data_quant['extras'].keys())
        if has_spec_bins and has_spec_keyword:
            spec_keyword = temp_data_quant['extras']['spec']
        else:
            spec_keyword = False
            
        if spec_keyword:
            new_plot, interactive_plot = specplot(name[i], num_plots, last_plot = (i == num_plots-1), height=p_height, width=p_width, var_label=var_label, interactive=interactive)       
            
        else:
            #Check if x and y ranges are set, if not, set good ones
            if 'x_range' not in tplot_common.tplot_opt_glob:
                x_min_list = []
                x_max_list = []
                for dataset in datasets:
                    #Get rid of infinities 
                    x_min_list.append(np.nanmin(dataset.index.tolist()))
                    x_max_list.append(np.nanmax(dataset.index.tolist()))
                tplot_common.tplot_opt_glob['x_range'] = [np.nanmin(x_min_list), np.nanmax(x_max_list)]
                tplot_x_range = [np.nanmin(x_min_list), np.nanmax(x_max_list)]
                if i == num_plots-1:
                    tplot_common.lim_info['xfull'] = tplot_x_range
                    tplot_common.lim_info['xlast'] = tplot_x_range
            if 'y_range' not in yaxis_opt:
                y_min_list = []
                y_max_list = []
                for dataset in datasets:
                    dataset_temp = dataset.replace([np.inf, -np.inf], np.nan)
                    y_min_list.append(np.nanmin(dataset_temp.min(skipna=True).tolist()))
                    y_max_list.append(np.nanmax(dataset_temp.max(skipna=True).tolist()))
                y_min = min(y_min_list)
                y_max = max(y_max_list)
                yaxis_opt['y_range'] = [y_min, y_max]
            
            #Convert all tplot options into variables for bokeh
            all_tplot_opt = {}
            all_tplot_opt['tools'] = tplot_common.tplot_opt_glob['tools']
            all_tplot_opt['min_border_top'] = tplot_common.tplot_opt_glob['min_border_top']
            all_tplot_opt['min_border_bottom'] = tplot_common.tplot_opt_glob['min_border_bottom']
            all_tplot_opt['x_range'] = Range1d(tplot_common.tplot_opt_glob['x_range'][0]* 1000, tplot_common.tplot_opt_glob['x_range'][1]* 1000)
            all_tplot_opt['y_range'] = Range1d(yaxis_opt['y_range'][0], yaxis_opt['y_range'][1])
            if 'y_axis_type' in yaxis_opt:
                all_tplot_opt['y_axis_type'] = yaxis_opt['y_axis_type']
            
            #Make the plot
            new_plot = Figure(x_axis_type='datetime', plot_height = p_height, plot_width = p_width, **all_tplot_opt)
                
            if num_plots > 1 and i == num_plots-1:
                new_plot.plot_height += 22
            
            #Formatting stuff
            new_plot.grid.grid_line_color = None
            new_plot.axis.major_tick_line_color = None
            new_plot.axis.major_label_standoff = 0
            new_plot.xaxis.formatter = dttf
            new_plot.title = None
            
            #Check for time bars
            if temp_data_quant['time_bar']:
                time_bars = temp_data_quant['time_bar']
                for time_bar in time_bars:
                    time_bar_line = Span(location = time_bar['location'], dimension = time_bar['dimension'], line_color = time_bar['line_color'], line_width = time_bar['line_width'])
                    new_plot.renderers.extend([time_bar_line])
            new_plot.renderers.extend(tplot_common.extra_renderers)
            new_plot.toolbar.active_drag='auto'
            
            xaxis1 = DatetimeAxis(major_label_text_font_size = '0pt', formatter=dttf)
            new_plot.add_layout(xaxis1, 'above')
                
            #Turn off the axes for all but last plot    
            if num_plots > 1 and i != num_plots-1:
                new_plot.xaxis.major_label_text_font_size = '0pt'

            # Add lines
            if 'line_color' in temp_data_quant['extras']:
                multi_line_colors = temp_data_quant['extras']['line_color']
            else:
                multi_line_colors = ['black', 'red', 'green', 'navy', 'orange', 'firebrick', 'pink', 'blue', 'olive']
            
            line_glyphs = []
            line_num = 0
            for dataset in datasets:
                yother = dataset
                line_style = None
                if 'linestyle' in temp_data_quant['extras']:
                    line_style = temp_data_quant['extras']['linestyle']
                for column_name in yother.columns:
                    corrected_time = []
                    for x in dataset.index:
                        corrected_time.append(tplot_utilities.int_to_str(x))
                    x = dataset.index * 1000
                    y = yother[column_name]
                    line_opt = temp_data_quant['line_opt']
                    line_source = ColumnDataSource(data=dict(x=x, y=y, corrected_time=corrected_time))
                    if auto_color:
                        line = Line(x='x', y='y', line_color = multi_line_colors[line_num % len(multi_line_colors)], **line_opt)
                    else:
                        line = Line(x='x', y='y', **line_opt)
                    if 'line_style' not in line_opt:
                        if line_style is not None:
                            line.line_dash = line_style[line_num % len(line_style)]
                    else:
                        line.line_dash = line_opt['line_style']
                    line_glyphs.append(new_plot.add_glyph(line_source, line))
                    line_num += 1
            
            #Set y/z labels
            new_plot.yaxis.axis_label = yaxis_opt['axis_label']
            #Add tools
            hover = HoverTool()
            hover.tooltips = [("Time","@corrected_time"), ("Value","@y")]
            new_plot.add_tools(hover)
            new_plot.add_tools(BoxZoomTool(dimensions='width'))
            
            #Add the Legend is applicable
            if line_num>1 and ('legend_names' in yaxis_opt):
                if len(yaxis_opt['legend_names']) != line_num:
                    print("Number of lines do not match length of legend names")
                legend = Legend()
                legend.location = (0,0)
                legend_items =[]
                j=0
                for legend_name in yaxis_opt['legend_names']:
                    legend_items.append((legend_name, [line_glyphs[j]]))
                    j = j+1
                legend.items = legend_items
                legend.label_text_font_size = "6pt"
                legend.border_line_color = None
                legend.glyph_height = int(p_height / (len(legend_items) + 1))
                new_plot.add_layout(legend, 'right')
            
        # Add name of variable to output file name
        if i == num_plots-1:    
            out_name += temp_data_quant['name']
        else:
            out_name += temp_data_quant['name'] + '+'
            
        # Add plot to GridPlot layout
        if interactive_plot is None:
            all_plots.append([new_plot])
        else:
            all_plots.append([new_plot, interactive_plot])
        i += 1 
    
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
    k = 0
    while(k < num_plots - 1):
        all_plots[k][0].x_range = all_plots[num_plots - 1][0].x_range
        k += 1
    
    #Add extra x axes if applicable 
    if var_label is not None:
        if not isinstance(var_label, list):
            var_label = [var_label]
        
        x_axes = []
        x_axes_index = 0
        for new_x_axis in var_label:
            
            axis_data_quant = tplot_common.data_quants[new_x_axis]
            axis_start = min(axis_data_quant['data'].min(skipna=True).tolist())
            axis_end = max(axis_data_quant['data'].max(skipna=True).tolist())
            x_axes.append(Range1d(start = axis_start, end = axis_end))
            
            k = 0
            while(k < num_plots ):
                all_plots[k][0].extra_x_ranges['extra_'+str(new_x_axis)] = x_axes[x_axes_index]
                k += 1
            
            all_plots[k-1][0].add_layout(LinearAxis(x_range_name = 'extra_'+str(new_x_axis)), 'below')
            all_plots[k-1][0].plot_height += 22
            x_axes_index += 1
    
    # Add toolbar and title (if applicable) to top plot.
    if 'title_text' in tplot_common.tplot_opt_glob:
        if tplot_common.tplot_opt_glob['title_text'] != '':
            title1 = Title(text = tplot_common.tplot_opt_glob['title_text'], 
                           align=tplot_common.tplot_opt_glob['title_align'],
                           text_font_size=tplot_common.tplot_opt_glob['title_size'])  
            all_plots[0][0].title = title1
            all_plots[0][0].plot_height += 22
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

def specplot(name, num_plots, last_plot=False, height=200, width=800, var_label=None, interactive=False):

    temp_data_quant = tplot_common.data_quants[name]

    if 'colormap' in temp_data_quant['extras']:
        rainbow_colormap = tplot_utilities.return_bokeh_colormap(temp_data_quant['extras']['colormap'])
    else:
        rainbow_colormap = tplot_utilities.return_bokeh_colormap('magma')
    
    yaxis_opt = temp_data_quant['yaxis_opt']
    zaxis_opt = temp_data_quant['zaxis_opt']
    
    if 'x_range' not in tplot_common.tplot_opt_glob:
        tplot_common.tplot_opt_glob['x_range'] = [np.nanmin(temp_data_quant['data'].index.tolist()), np.nanmax(temp_data_quant['data'].index.tolist())]
        tplot_x_range = Range1d(np.nanmin(temp_data_quant['data'].index.tolist()), np.nanmax(temp_data_quant['data'].index.tolist()))
        if last_plot:
            tplot_common.lim_info['xfull'] = tplot_x_range
            tplot_common.lim_info['xlast'] = tplot_x_range
    if 'y_range' not in yaxis_opt:
        ymin = np.nanmin(temp_data_quant['spec_bins'])
        ymax = np.nanmax(temp_data_quant['spec_bins'])
        yaxis_opt['y_range'] = [ymin, ymax]
            
    all_tplot_opt = {}
    all_tplot_opt['tools'] = tplot_common.tplot_opt_glob['tools']
    all_tplot_opt['min_border_top'] = tplot_common.tplot_opt_glob['min_border_top']
    all_tplot_opt['min_border_bottom'] = tplot_common.tplot_opt_glob['min_border_bottom']
    all_tplot_opt['x_range'] = Range1d(tplot_common.tplot_opt_glob['x_range'][0]* 1000, tplot_common.tplot_opt_glob['x_range'][1]* 1000)
    all_tplot_opt['y_range'] = Range1d(yaxis_opt['y_range'][0], yaxis_opt['y_range'][1])
    if 'y_axis_type' in yaxis_opt:
        all_tplot_opt['y_axis_type'] = yaxis_opt['y_axis_type']
    #Retrieve y and z logs
    if 'z_axis_type' in zaxis_opt:
        zscale = zaxis_opt['z_axis_type']
    else:
        zscale = 'log'
    
            
    #Get Z Range
    if 'z_range' in temp_data_quant['zaxis_opt']:
        zmin = temp_data_quant['zaxis_opt']['z_range'][0]
        zmax = temp_data_quant['zaxis_opt']['z_range'][1]
    else:
        zmax = temp_data_quant['data'].max().max()
        zmin = temp_data_quant['data'].min().min()
        if zscale=='log':
            zmin_list = []
            for column in temp_data_quant['data'].columns:
                series = temp_data_quant['data'][column]
                zmin_list.append(series.iloc[series.nonzero()[0]].min())
            zmin = min(zmin_list)
    
    
    new_plot=Figure(x_axis_type='datetime', plot_height = height, plot_width = width, **all_tplot_opt)
    new_plot.lod_factor = 100
    new_plot.lod_interval = 30
    new_plot.lod_threshold = 100
    new_plot.yaxis.axis_label_text_font_size = "10pt"
    
    #APPARENTLY NEEDED
    if num_plots > 1 and last_plot==True:
        new_plot.plot_height += 22
    #if num_plots > 1:
    #    p.toolbar_location = None
    
    #GET CORRECT X DATA
    x = temp_data_quant['data'].index.tolist()
    temp = [a for a in x if (a <= (tplot_common.tplot_opt_glob['x_range'][1]) and a >= (tplot_common.tplot_opt_glob['x_range'][0]))]
    x= temp

    #Sometimes X will be huge, we'll need to cut down so that each x will stay about 1 pixel in size
    step_size=1
    num_rect_displayed = len(x)
    if (width*2) < num_rect_displayed:
        step_size=int(math.floor(num_rect_displayed/(width*2)))
        x[:] = x[0::step_size]

    #Get length of arrays
    size_x = len(x)
    size_y = len(temp_data_quant['spec_bins'])
    
    #These arrays will be populated with data for the rectangle glyphs
    color = []
    bottom = []
    top = []
    left=[]
    right=[]
    value=[]
    corrected_time=[]
    
    #left, right, and time do not depend on the values in spec_bins
    for j in range(size_x-1):
        left.append(x[j]*1000)
        right.append(x[j+1]*1000)
        corrected_time.append(tplot_utilities.int_to_str(x[j]))
        
    left = left * (size_y-1)
    right = right * (size_y-1)
    corrected_time = corrected_time * (size_y-1)
    
    for i in range(size_y-1):
        temp = temp_data_quant['data'][temp_data_quant['spec_bins'][i]][x[0:size_x-1]].tolist()
        value.extend(temp)
        color.extend(tplot_utilities.get_heatmap_color(color_map=rainbow_colormap, min_val=zmin, max_val=zmax, values=temp, zscale=zscale))
        bottom.extend([temp_data_quant['spec_bins'][i]]*(size_x-1))
        top.extend([temp_data_quant['spec_bins'][i+1]]*(size_x-1))
        
    #Here is where we add all of the rectangles to the plot
    cds = ColumnDataSource(data=dict(x=left,y=bottom,right=right, top = top, z=color,value=value, corrected_time=corrected_time))
    new_plot.quad(bottom = 'y', left='x', right='right', top='top', color='z', source=cds)
        
    if interactive:
        if 'y_axis_type' in yaxis_opt:
            y_interactive_log = 'log'
        else:
            y_interactive_log = 'linear'
        interactive_plot = Figure(plot_height = height, plot_width = width, y_range = (zmin, zmax), y_axis_type=y_interactive_log)
        interactive_plot.min_border_left = 100
        spec_bins = temp_data_quant['spec_bins']
        flux = [0]*len(spec_bins)
        interactive_line_source = ColumnDataSource(data=dict(x=spec_bins, y=flux))
        interactive_line = Line(x='x', y='y')
        interactive_plot.add_glyph(interactive_line_source, interactive_line)
        callback = CustomJS(args=dict(cds=cds, interactive_line_source=interactive_line_source), code="""
                var geometry = cb_data['geometry'];
                var x_data = geometry.x; // current mouse x position in plot coordinates
                var y_data = geometry.y; // current mouse y position in plot coordinates
                var d2 = interactive_line_source.get('data');
                var asdf = cds.get('data');
                var j = 0;
                x=d2['x']
                y=d2['y']
                time=asdf['x']
                energies=asdf['y']
                flux=asdf['value']
                for (i = 0; i < time.length-1; i++) {
                    if(x_data >= time[i] && x_data <= time[i+1] ) {
                        x[j] = energies[i]
                        y[j] = flux[i]
                        j=j+1
                    }
                }
                j=0
                interactive_line_source.trigger('change');
            """)
    else:
        interactive_plot = None
        callback=None
    
    #Formatting stuff
    new_plot.grid.grid_line_color = None
    new_plot.axis.major_tick_line_color = None
    new_plot.axis.major_label_standoff = 0
    new_plot.xaxis.formatter = dttf
    new_plot.title = None
    #Check for time bars
    if temp_data_quant['time_bar']:
        time_bars = temp_data_quant['time_bar']
        for time_bar in time_bars:
            time_bar_line = Span(location = time_bar['location'], dimension = time_bar['dimension'], line_color = time_bar['line_color'], line_width = time_bar['line_width'])
            new_plot.renderers.extend([time_bar_line])
            
    new_plot.renderers.extend(tplot_common.extra_renderers)
    new_plot.toolbar.active_drag='auto'
    
    #Add axes
    xaxis1 = DatetimeAxis(major_label_text_font_size = '0pt', formatter=dttf)
    new_plot.add_layout(xaxis1, 'above')
    if num_plots > 1 and not last_plot:
        new_plot.xaxis.major_label_text_font_size = '0pt'
    
    #Add the color bar
    if 'z_axis_type' in zaxis_opt:
        if zaxis_opt['z_axis_type'] == 'log':
            color_mapper=LogColorMapper(palette=rainbow_colormap, low=zmin, high=zmax)
            color_bar=ColorBarSideTitle(color_mapper=color_mapper, ticker=LogTicker(), border_line_color=None, location=(0,0))
        else:
            color_mapper=LinearColorMapper(palette=rainbow_colormap, low=zmin, high=zmax)
            color_bar=ColorBarSideTitle(color_mapper=color_mapper, ticker=BasicTicker(), border_line_color=None, location=(0,0))
    else:
        color_mapper=LogColorMapper(palette=rainbow_colormap, low=zmin, high=zmax)
        color_bar=ColorBarSideTitle(color_mapper=color_mapper, ticker=LogTicker(), border_line_color=None, location=(0,0))
    color_bar.width=10
    color_bar.formatter = BasicTickFormatter(precision=1)
    color_bar.major_label_text_align = 'left'
    color_bar.label_standoff = 5
    color_bar.major_label_text_baseline = 'middle'
    #color_bar.title='hello'
    #color_bar.title_text_align = 'left'
    
    
    #Set y/z labels
    new_plot.yaxis.axis_label = yaxis_opt['axis_label']
    if 'axis_label' in zaxis_opt:
        color_bar.title = zaxis_opt['axis_label']
        color_bar.title_text_font_size = '8pt'
        color_bar.title_text_font_style = 'bold'
        color_bar.title_standoff = 20
    
    new_plot.add_layout(color_bar, 'right')
    
    #Create a custom hover tool
    hover = HoverTool(callback=callback)
    hover.tooltips = [("Time","@corrected_time"), ("Energy", "@y"), ("Value","@value")]
    new_plot.add_tools(hover)
    new_plot.add_tools(BoxZoomTool(dimensions='width'))
    
    return new_plot, interactive_plot

