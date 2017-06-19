# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import numpy as np
from bokeh.plotting.figure import Figure
from bokeh.models import (ColumnDataSource, DatetimeAxis, HoverTool, 
                          Range1d, Span, Title, Legend)
from bokeh.models.glyphs import Line
from bokeh.models.tools import BoxZoomTool

from . import tplot_common
from . import tplot_utilities
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


class TVarFigure1D(object):
    
    def __init__(self, tvar, auto_color, last_plot=False, interactive=False):
        self.tvar = tvar
        self.auto_color=auto_color
        self.last_plot=last_plot
        self.interactive=interactive
       
        #Variables needed across functions
        self.colors = ['black', 'red', 'green', 'navy', 'orange', 'firebrick', 'pink', 'blue', 'olive']
        self.lineglyphs = []
        self.linenum = 0
        self.interactive_plot = None

        self.fig = Figure(output_backend='webgl', 
                          x_axis_type='datetime', 
                          tools = tplot_common.tplot_opt_glob['tools'],
                          y_axis_type=self._getyaxistype())
        self.fig.add_tools(BoxZoomTool(dimensions='width'))
        self._format()
        
    def getaxistype(self):
        axis_type = 'time'
        link_y_axis = False
        return axis_type, link_y_axis

    def getfig(self):
        if self.interactive:
            return [self.fig, self.interactive_plot]
        else:
            return [self.fig]
    
    def setsize(self, width, height):
        self.fig.plot_width = width
        if self.last_plot:
            self.fig.plot_height = height + 22
        else:
            self.fig.plot_height = height

    def add_title(self):
        if 'title_text' in tplot_common.tplot_opt_glob:
            if tplot_common.tplot_opt_glob['title_text'] != '':
                title1 = Title(text = tplot_common.tplot_opt_glob['title_text'], 
                               align=tplot_common.tplot_opt_glob['title_align'],
                               text_font_size=tplot_common.tplot_opt_glob['title_size'])  
                self.fig.title = title1
                self.fig.plot_height += 22

    def buildfigure(self):
        self._setminborder()
        self._setxrange()
        self._setxaxis()
        self._setyrange()
        self._addtimebars()
        self._visdata()
        self._setyaxislabel()
        self._addhoverlines()
        self._addlegend()
        self._addextras()
    
    def _format(self):
        #Formatting stuff
        self.fig.grid.grid_line_color = None
        self.fig.axis.major_tick_line_color = None
        self.fig.axis.major_label_standoff = 0
        self.fig.xaxis.formatter = dttf
        self.fig.title = None
        self.fig.toolbar.active_drag='auto'
        if not self.last_plot:
            self.fig.xaxis.major_label_text_font_size = '0pt'
            
    def _setxrange(self):
        #Check if x range is not set, if not, set good ones
        if 'x_range' not in tplot_common.tplot_opt_glob:
            datasets = []
            x_min_list = []
            x_max_list = []
            if isinstance(self.tvar.data, list):
                for oplot_name in self.tvar.data:
                    datasets.append(tplot_common.data_quants[oplot_name].data)
            else:
                datasets.append(self.tvar.data)
            for dataset in datasets:
                x_min_list.append(np.nanmin(dataset.index.tolist()))
                x_max_list.append(np.nanmax(dataset.index.tolist()))
            tplot_common.tplot_opt_glob['x_range'] = [np.nanmin(x_min_list), np.nanmax(x_max_list)]
            tplot_x_range = [np.nanmin(x_min_list), np.nanmax(x_max_list)]
            if self.last_plot:
                tplot_common.lim_info['xfull'] = tplot_x_range
                tplot_common.lim_info['xlast'] = tplot_x_range
        
        #Bokeh uses milliseconds since epoch for some reason
        x_range = Range1d(tplot_common.tplot_opt_glob['x_range'][0]* 1000, tplot_common.tplot_opt_glob['x_range'][1]* 1000)
        self.fig.x_range = x_range
    
    def _setyrange(self):
        if self._getyaxistype() == 'log':
            if self.tvar.yaxis_opt['y_range'][0] <0 or self.tvar.yaxis_opt['y_range'][1] < 0:
                return
        y_range = Range1d(self.tvar.yaxis_opt['y_range'][0], self.tvar.yaxis_opt['y_range'][1])
        self.fig.y_range = y_range
        
    def _setminborder(self):
        self.fig.min_border_bottom = tplot_common.tplot_opt_glob['min_border_bottom']
        self.fig.min_border_top = tplot_common.tplot_opt_glob['min_border_top']
    
        
    def _addtimebars(self):
        for time_bar in self.tvar.time_bar:
            time_bar_line = Span(location = time_bar['location'], dimension = time_bar['dimension'], line_color = time_bar['line_color'], line_width = time_bar['line_width'])
            self.fig.renderers.extend([time_bar_line])
            
    def _setxaxis(self):
        xaxis1 = DatetimeAxis(major_label_text_font_size = '0pt', formatter=dttf)
        self.fig.add_layout(xaxis1, 'above')
        
    def _getyaxistype(self):
        if 'y_axis_type' in self.tvar.yaxis_opt:
            return self.tvar.yaxis_opt['y_axis_type']
        else:
            return 'linear'
        
    def _setcolors(self):
        if 'line_color' in self.tvar.extras:
            self.colors = self.tvar.extras['line_color']
    
    def _setyaxislabel(self):
        self.fig.yaxis.axis_label = self.tvar.yaxis_opt['axis_label']
        
    def _visdata(self):
        self._setcolors()
        
        datasets = []
        if isinstance(self.tvar.data, list):
            for oplot_name in self.tvar.data:
                datasets.append(tplot_common.data_quants[oplot_name].data)
        else:
            datasets.append(self.tvar.data)
        
        
        for dataset in datasets:                
            #Get Linestyle
            line_style = None
            if 'linestyle' in self.tvar.extras:
                line_style = self.tvar.extras['linestyle']
                
            #Get a list of formatted times  
            corrected_time = [] 
            for x in dataset.index:
                corrected_time.append(tplot_utilities.int_to_str(x))
                
            #Bokeh uses milliseconds since epoch for some reason
            x = dataset.index * 1000
            
            #Create lines from each column in the dataframe    
            for column_name in dataset.columns:
                y = dataset[column_name]
                
                if self._getyaxistype() == 'log':
                    y.loc[y <= 0] = np.NaN                
                
                line_source = ColumnDataSource(data=dict(x=x, y=y, corrected_time=corrected_time))
                if self.auto_color:
                    line = Line(x='x', y='y', line_color = self.colors[self.linenum % len(self.colors)], **self.tvar.line_opt)
                else:
                    line = Line(x='x', y='y', **self.tvar.line_opt)
                if 'line_style' not in self.tvar.line_opt:
                    if line_style is not None:
                        line.line_dash = line_style[self.linenum % len(line_style)]
                else:
                    line.line_dash = self.tvar.line_opt['line_style']
                self.lineglyphs.append(self.fig.add_glyph(line_source, line))
                self.linenum += 1
    
    def _addhoverlines(self):
        #Add tools
        hover = HoverTool()
        hover.tooltips = [("Time","@corrected_time"), ("Value","@y")]
        self.fig.add_tools(hover)
        
    def _addlegend(self):
        #Add the Legend if applicable
        if 'legend_names' in self.tvar.yaxis_opt:
            legend_names = self.tvar.yaxis_opt['legend_names']
            if len(legend_names) != self.linenum:
                print("Number of lines do not match length of legend names")
            legend = Legend()
            legend.location = (0,0)
            legend_items =[]
            j=0
            for legend_name in legend_names:
                legend_items.append((legend_name, [self.lineglyphs[j]]))
                j = j+1
                if j>=len(self.lineglyphs):
                    break
            legend.items = legend_items
            legend.label_text_font_size = "6pt"
            legend.border_line_color = None
            legend.glyph_height = int(self.fig.plot_height / (len(legend_items) + 1))
            self.fig.add_layout(legend, 'right')
            
    def _addextras(self):
        self.fig.renderers.extend(tplot_common.extra_renderers)
                