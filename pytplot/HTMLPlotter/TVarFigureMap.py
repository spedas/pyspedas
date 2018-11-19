# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import numpy as np
import os
from bokeh.plotting.figure import Figure
from bokeh.models import (LogColorMapper, LogTicker, LinearColorMapper, 
                          BasicTicker, ColumnDataSource, HoverTool, 
                          Range1d, Span, Title)
from bokeh.models.formatters import BasicTickFormatter

import pytplot
from .CustomModels.colorbarsidetitle import ColorBarSideTitle

class TVarFigureMap(object):
    
    def __init__(self, tvar_name, auto_color = False, show_xaxis=False, interactive=False):
        self.tvar_name = tvar_name
        self.show_xaxis=show_xaxis
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
        self.fig = Figure(tools = "pan,crosshair,reset,box_zoom", 
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
        if self.show_xaxis:
            self.fig.plot_height = height + 22
        else:
            self.fig.plot_height = height

    def add_title(self):
        if 'title_text' in pytplot.tplot_opt_glob:
            if pytplot.tplot_opt_glob['title_text'] != '':
                title1 = Title(text = pytplot.tplot_opt_glob['title_text'], 
                               align=pytplot.tplot_opt_glob['title_align'],
                               text_font_size=pytplot.tplot_opt_glob['title_size'])  
                self.fig.title = title1
                self.fig.plot_height += 22
    
    def buildfigure(self):
        self._setminborder()
        self._setxrange()
        self._setxaxis()
        self._setyrange()
        self._setzrange()
        self._setzaxistype()
        self._setbackground()
        self._visdata()
        self._setxaxislabel()
        self._setyaxislabel()
        self._setzaxislabel()
        self._addhoverlines()
        self._addlegend()
        self._addtimebars()

        
    def _format(self):
        #Formatting stuff
        self.fig.grid.grid_line_color = None
        self.fig.axis.major_tick_line_color = None
        self.fig.axis.major_label_standoff = 0
        self.fig.title = None
        self.fig.toolbar.active_drag='auto'
        if not self.show_xaxis:
            self.fig.xaxis.major_label_text_font_size = '0pt'
            self.fig.xaxis.visible = False
        self.fig.lod_factor = 100
        self.fig.lod_interval = 30
        self.fig.lod_threshold = 100
        self.fig.yaxis.axis_label_text_font_size = "10pt"
        
    def _setxrange(self):
        #Check if x range is not set, if not, set good ones
        if 'map_range' not in pytplot.tplot_opt_glob:
            pytplot.tplot_opt_glob['map_range'] = [0, 360]
            tplot_x_range = Range1d(0, 360)
            if self.show_xaxis:
                pytplot.lim_info['xfull'] = tplot_x_range
                pytplot.lim_info['xlast'] = tplot_x_range
        
        #Bokeh uses milliseconds since epoch for some reason
        x_range = Range1d(pytplot.tplot_opt_glob['map_range'][0], 
                          pytplot.tplot_opt_glob['map_range'][1],
                          bounds = (0, 360))
        self.fig.x_range = x_range
    
    def _setyrange(self):
        y_range = Range1d(-90, 90, bounds=(-90, 90))
        self.fig.y_range = y_range
        
    def _setzrange(self):
        #Get Z Range
        if 'z_range' in pytplot.data_quants[self.tvar_name].zaxis_opt:
            self.zmin = pytplot.data_quants[self.tvar_name].zaxis_opt['z_range'][0]
            self.zmax = pytplot.data_quants[self.tvar_name].zaxis_opt['z_range'][1]
        else:
            if isinstance(pytplot.data_quants[self.tvar_name].data, list):
                #Check the first one
                dataset_temp = pytplot.data_quants[pytplot.data_quants[self.tvar_name].data[0]].data.replace([np.inf, -np.inf], np.nan)
            else:
                dataset_temp = pytplot.data_quants[self.tvar_name].data.replace([np.inf, -np.inf], np.nan)
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
        self.fig.min_border_bottom = pytplot.tplot_opt_glob['min_border_bottom']
        self.fig.min_border_top = pytplot.tplot_opt_glob['min_border_top']
        
    def _addtimebars(self):
        for time_bar in pytplot.data_quants[self.tvar_name].time_bar:
            time_bar_line = Span(location = time_bar['location'], 
                                 dimension = time_bar['dimension'], 
                                 line_color = time_bar['line_color'], 
                                 line_width = time_bar['line_width'])
            self.fig.renderers.extend([time_bar_line])
        #initialize dataset variable
        datasets = []
        #grab tbardict
        tbardict = pytplot.data_quants[self.tvar_name].time_bar
        ltbar = len(tbardict)
        #make sure data is in list format
        if isinstance(pytplot.data_quants[self.tvar_name].data, list):
            for oplot_name in pytplot.data_quants[self.tvar_name].data:
                datasets.append(pytplot.data_quants[oplot_name])
        else:
            datasets.append(pytplot.data_quants[self.tvar_name])        
        for dataset in datasets:  
            #for location in tbar dict
            for i in range(ltbar):
                #get times, color, point size
                test_time = pytplot.data_quants[self.tvar_name].time_bar[i]["location"]
                color = pytplot.data_quants[self.tvar_name].time_bar[i]["line_color"]
                pointsize = pytplot.data_quants[self.tvar_name].time_bar[i]["line_width"]
                #correlate given time with corresponding lat/lon points
                time, latitude = pytplot.get_data(dataset.links['lat']) 
                time, longitude = pytplot.get_data(dataset.links['lon'])
                latitude = latitude.transpose()[0]
                longitude = longitude.transpose()[0]
                nearest_time_index = np.abs(time - test_time).argmin()
                lat_point = latitude[nearest_time_index]
                lon_point = longitude[nearest_time_index]
                #color = pytplot.tplot_utilities.rgb_color(color)
                self.fig.circle([lon_point], [lat_point], size = pointsize, color = color)

        return
            
    def _setxaxis(self):
        #Nothing to set for now
        return
        
    def _getyaxistype(self):
        #Not going to have a log planet map
        return 'linear'
        
    def _setzaxistype(self):
        if 'z_axis_type' in pytplot.data_quants[self.tvar_name].zaxis_opt:
            self.zscale = pytplot.data_quants[self.tvar_name].zaxis_opt['z_axis_type']

        
    def _setcolors(self):          
        if 'colormap' in pytplot.data_quants[self.tvar_name].extras:
            for cm in pytplot.data_quants[self.tvar_name].extras['colormap']:
                self.colors.append(pytplot.tplot_utilities.return_bokeh_colormap(cm))
        else:
            self.colors.append(pytplot.tplot_utilities.return_bokeh_colormap('magma'))
        
    def _setxaxislabel(self):
        self.fig.xaxis.axis_label = pytplot.data_quants[self.tvar_name].xaxis_opt['axis_label']
    
    def _setyaxislabel(self):
        self.fig.yaxis.axis_label = pytplot.data_quants[self.tvar_name].yaxis_opt['axis_label']
    
    def _setzaxislabel(self):
        self.fig.yaxis.axis_label = pytplot.data_quants[self.tvar_name].yaxis_opt['axis_label']
        
    def _visdata(self):
        self._setcolors()
        datasets = []
        if isinstance(pytplot.data_quants[self.tvar_name].data, list):
            for oplot_name in pytplot.data_quants[self.tvar_name].data:
                datasets.append(pytplot.data_quants[oplot_name])
        else:
            datasets.append(pytplot.data_quants[self.tvar_name])
        
        cm_index=0
        for dataset in datasets:   
            #TODO: Add a check that lon and lat are only 1D
            t_link_lon, x = pytplot.get_data(dataset.links['lon'])
            t_link_lat, y = pytplot.get_data(dataset.links['lat'])

            for column_name in dataset.data.columns:
                data = dataset.data[column_name].values

                # Need to trim down the data points to fit within the link
                t_tvar = dataset.data.index.values
                while t_tvar[-1] > t_link_lon[-1]:
                    t_tvar = np.delete(t_tvar, -1)
                    data = np.delete(data, -1)
                while t_tvar[0] < t_link_lon[0]:
                    t_tvar = np.delete(t_tvar, 0)
                    data = np.delete(data, 0)
                while t_tvar[-1] > t_link_lat[-1]:
                    t_tvar = np.delete(t_tvar, -1)
                    data = np.delete(data, -1)
                while t_tvar[0] < t_link_lat[0]:
                    t_tvar = np.delete(t_tvar, 0)
                    data = np.delete(data, 0)

                colors=[]
                colors.extend(pytplot.tplot_utilities.get_heatmap_color(color_map=self.colors[cm_index % len(self.colors)], 
                                                                        min_val=self.zmin, 
                                                                        max_val=self.zmax, 
                                                                        values=data.tolist(),
                                                                        zscale=self.zscale))
                circle_source = ColumnDataSource(data=dict(x=x, 
                                                           y=y, 
                                                           value=data.tolist(),
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
    
        
    def _addlegend(self):
        #Add the color bar
        if 'z_axis_type' in pytplot.data_quants[self.tvar_name].zaxis_opt:
            if pytplot.data_quants[self.tvar_name].zaxis_opt['z_axis_type'] == 'log':
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
        
        if 'axis_label' in pytplot.data_quants[self.tvar_name].zaxis_opt:
            color_bar.title = pytplot.data_quants[self.tvar_name].zaxis_opt['axis_label']
            color_bar.title_text_font_size = '8pt'
            color_bar.title_text_font_style = 'bold'
            color_bar.title_standoff = 20
        
        
        self.fig.add_layout(color_bar, 'right')
    
    def _setbackground(self):
        if 'alpha' in pytplot.data_quants[self.tvar_name].extras:
            alpha=pytplot.data_quants[self.tvar_name].extras['alpha']
        else:
            alpha=1
        if 'basemap' in pytplot.data_quants[self.tvar_name].extras:
            if os.path.isfile(pytplot.data_quants[self.tvar_name].extras['basemap']):
                from scipy import misc
                img = misc.imread(pytplot.data_quants[self.tvar_name].extras['basemap'], mode='RGBA') 
                #Need to flip the image upside down...This will probably be fixed in 
                #a future release, so this will need to be deleted at some point
                img = img[::-1]          
                self.fig.image_rgba(image = [img], x = 0, y=-90, dw=360, dh=180, alpha=alpha)