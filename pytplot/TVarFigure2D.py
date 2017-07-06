# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import numpy as np
import os
from bokeh.plotting.figure import Figure
from bokeh.models import (CustomJS, LogColorMapper, LogTicker, LinearColorMapper, 
                          BasicTicker, ColumnDataSource, DatetimeAxis, HoverTool, 
                          Range1d, Span, Title)
from bokeh.models.glyphs import Line
from bokeh.models.tools import BoxZoomTool, PanTool
from bokeh.models.formatters import BasicTickFormatter

from . import tplot_common
from .colorbarsidetitle import ColorBarSideTitle
from . import tplot_utilities

class TVarFigure2D(object):
    
    def __init__(self, tvar, last_plot=False, interactive=False):
        self.tvar = tvar
        self.last_plot=last_plot
        self.interactive = interactive

        #Variables needed across functions
        self.fig=None
        self.colors = []
        self.lineglyphs = []
        self.linenum = 0
        self.zscale = 'linear'
        self.zmin = 0
        self.zmax = 1
        self.callback = None
        self.interactive_plot = None
        self.fig = Figure(tools = "pan,wheel_zoom,crosshair,reset,box_zoom", 
                          y_axis_type=self._getyaxistype() )
        self._format()
    def getaxistype(self):
        axis_type = 'map'
        link_y_axis = True
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
        self._setzrange()
        self._setzaxistype()
        self._addtimebars()
        self._visdata()
        self._setyaxislabel()
        self._setzaxislabel()
        self._addhoverlines()
        self._addlegend()
        self._addextras()
        self._setbackground()
        
    def _format(self):
        #Formatting stuff
        self.fig.grid.grid_line_color = None
        self.fig.axis.major_tick_line_color = None
        self.fig.axis.major_label_standoff = 0
        self.fig.title = None
        self.fig.toolbar.active_drag='auto'
        if not self.last_plot:
            self.fig.xaxis.major_label_text_font_size = '0pt'
            self.fig.xaxis.visible = False
        self.fig.lod_factor = 100
        self.fig.lod_interval = 30
        self.fig.lod_threshold = 100
        self.fig.yaxis.axis_label_text_font_size = "10pt"
        
    def _setxrange(self):
        #Check if x range is not set, if not, set good ones
        if 'map_range' not in tplot_common.tplot_opt_glob:
            tplot_common.tplot_opt_glob['map_range'] = [0, 360]
            tplot_x_range = Range1d(0, 360)
            if self.last_plot:
                tplot_common.lim_info['xfull'] = tplot_x_range
                tplot_common.lim_info['xlast'] = tplot_x_range
        
        #Bokeh uses milliseconds since epoch for some reason
        x_range = Range1d(tplot_common.tplot_opt_glob['map_range'][0], 
                          tplot_common.tplot_opt_glob['map_range'][1],
                          bounds = (0, 360))
        self.fig.x_range = x_range
    
    def _setyrange(self):
        y_range = Range1d(-90, 
                          90, 
                          bounds=(-90, 90))
        self.fig.y_range = y_range
        
    def _setzrange(self):
        #Get Z Range
        if 'z_range' in self.tvar.zaxis_opt:
            self.zmin = self.tvar.zaxis_opt['z_range'][0]
            self.zmax = self.tvar.zaxis_opt['z_range'][1]
        else:
            if isinstance(self.tvar.data, list):
                dataset_temp = tplot_common.data_quants[self.tvar.data[0]].data.replace([np.inf, -np.inf], np.nan)
            else:
                dataset_temp = self.tvar.data.replace([np.inf, -np.inf], np.nan)
            self.zmax = dataset_temp.max().max()
            self.zmin = dataset_temp.min().min()
            
            #Cannot have a 0 minimum in a log scale
            if self.zscale=='log':
                zmin_list = []
                for column in dataset_temp.columns:
                    series = dataset_temp[column]
                    zmin_list.append(series.iloc[series.nonzero()[0]].min())
                self.zmin = min(zmin_list)
        
    def _setminborder(self):
        self.fig.min_border_bottom = tplot_common.tplot_opt_glob['min_border_bottom']
        self.fig.min_border_top = tplot_common.tplot_opt_glob['min_border_top']
        
    def _addtimebars(self):
        for time_bar in self.tvar.time_bar:
            time_bar_line = Span(location = time_bar['location'], 
                                 dimension = time_bar['dimension'], 
                                 line_color = time_bar['line_color'], 
                                 line_width = time_bar['line_width'])
            self.fig.renderers.extend([time_bar_line])
            
    def _setxaxis(self):
        #Nothing to set for now
        return
        
    def _getyaxistype(self):
        #Not going to have a log planet map
        return 'linear'
        
    def _setzaxistype(self):
        if 'z_axis_type' in self.tvar.zaxis_opt:
            self.zscale = self.tvar.zaxis_opt['z_axis_type']

        
    def _setcolors(self):          
        if 'colormap' in self.tvar.extras:
            for cm in self.tvar.extras['colormap']:
                self.colors.append(tplot_utilities.return_bokeh_colormap(cm))
        else:
            self.colors.append(tplot_utilities.return_bokeh_colormap('magma'))

    
    def _setyaxislabel(self):
        self.fig.yaxis.axis_label = self.tvar.yaxis_opt['axis_label']
    
    def _setzaxislabel(self):
        self.fig.yaxis.axis_label = self.tvar.yaxis_opt['axis_label']
        
    def _visdata(self):
        self._setcolors()
        
        
        datasets = []
        if isinstance(self.tvar.data, list):
            for oplot_name in self.tvar.data:
                datasets.append(tplot_common.data_quants[oplot_name].data)
        else:
            datasets.append(self.tvar.data)
        
        cm_index=0
        for dataset in datasets:   
            x = dataset.index.tolist()
            x = list(zip(*x))
            
            for column_name in dataset.columns:
                values = dataset[column_name].tolist()
                colors=[]
                colors.extend(tplot_utilities.get_heatmap_color(color_map=self.colors[cm_index], 
                                                                min_val=self.zmin, 
                                                                max_val=self.zmax, 
                                                                values=values, 
                                                                zscale=self.zscale))
                circle_source = ColumnDataSource(data=dict(x=x[0], 
                                                           y=x[1], 
                                                           value=values, 
                                                           colors=colors))
                self.fig.scatter(x='x',y='y', 
                                 radius=1.0, 
                                 fill_color='colors', 
                                 fill_alpha=1, 
                                 line_color=None, 
                                 source=circle_source)
            cm_index+=1
        
        
    def _addhoverlines(self):
        #Add tools
        hover = HoverTool()
        hover.tooltips = [("Longitude","@x"), ("Latitude", "@y"), ("Value","@value")]
        self.fig.add_tools(hover)
    
    def _addextras(self):
        self.fig.renderers.extend(tplot_common.extra_renderers)
        
    def _addlegend(self):
        #Add the color bar
        if 'z_axis_type' in self.tvar.zaxis_opt:
            if self.tvar.zaxis_opt['z_axis_type'] == 'log':
                color_mapper=LogColorMapper(palette=self.colors[0], 
                                            low=self.zmin, 
                                            high=self.zmax)
                color_bar=ColorBarSideTitle(color_mapper=color_mapper, 
                                            border_line_color=None, 
                                            location=(0,0),
                                            ticker=LogTicker())
            else:
                color_mapper=LinearColorMapper(palette=self.colors[0], 
                                               low=self.zmin, 
                                               high=self.zmax)
                color_bar=ColorBarSideTitle(color_mapper=color_mapper, 
                                            border_line_color=None, 
                                            location=(0,0),
                                            ticker=BasicTicker())
        else:
            color_mapper=LinearColorMapper(palette=self.colors[0], 
                                           low=self.zmin, 
                                           high=self.zmax)
            color_bar=ColorBarSideTitle(color_mapper=color_mapper, 
                                        border_line_color=None, 
                                        location=(0,0),
                                        ticker=BasicTicker())
        color_bar.width=10
        color_bar.formatter = BasicTickFormatter(precision=1)
        color_bar.major_label_text_align = 'left'
        color_bar.label_standoff = 5
        color_bar.major_label_text_baseline = 'middle'
        
        if 'axis_label' in self.tvar.zaxis_opt:
            color_bar.title = self.tvar.zaxis_opt['axis_label']
            color_bar.title_text_font_size = '8pt'
            color_bar.title_text_font_style = 'bold'
            color_bar.title_standoff = 20
        
        
        self.fig.add_layout(color_bar, 'right')
    
    def _setbackground(self):
        if 'alpha' in self.tvar.extras:
            alpha=self.tvar.extras['alpha']
        else:
            alpha=1
        if 'basemap' in self.tvar.extras:
            if os.path.isfile(self.tvar.extras['basemap']):
                self.fig.image_url(url=[self.tvar.extras['basemap']], x = 0, y=90, w=360, h=180, global_alpha=alpha)