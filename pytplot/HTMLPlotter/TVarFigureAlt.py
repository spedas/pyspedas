# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import numpy as np
from bokeh.plotting.figure import Figure
from bokeh.models import (ColumnDataSource, HoverTool, 
                          Range1d, Span, Title, Legend)
from bokeh.models.glyphs import Line
from bokeh.models.markers import Circle, X
from bokeh.models.tools import BoxZoomTool

import pytplot


class TVarFigureAlt(object):
    
    def __init__(self, tvar_name, auto_color, show_xaxis=False, slice=False):
        self.tvar_name = tvar_name
        self.auto_color = auto_color
        self.show_xaxis = show_xaxis
        self.slice = slice
       
        # Variables needed across functions
        self.colors = ['black', 'red', 'green', 'navy', 'orange', 'firebrick', 'pink', 'blue', 'olive']
        self.lineglyphs = []
        self.linenum = 0
        self.interactive_plot = None
        self.fig = Figure(tools=pytplot.tplot_opt_glob['tools'],
                          y_axis_type=self._getyaxistype())
        self.fig.add_tools(BoxZoomTool(dimensions='width'))
        self._format()

    @staticmethod
    def get_axis_label_color():
        if pytplot.tplot_opt_glob['black_background']:
            text_color = '#000000'
        else:
            text_color = '#FFFFFF'
        return text_color

    @staticmethod
    def getaxistype():
        axis_type = 'altitude'
        link_y_axis = False
        return axis_type, link_y_axis
    
    def getfig(self):
        if self.slice:
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
                title1 = Title(text=pytplot.tplot_opt_glob['title_text'],
                               align=pytplot.tplot_opt_glob['title_align'],
                               text_font_size=pytplot.tplot_opt_glob['title_size'],
                               text_color=self.get_axis_label_color())
                self.fig.title = title1
                self.fig.plot_height += 22

    def buildfigure(self):
        self._setminborder()
        self._setxrange()
        self._setxaxis()
        self._setyrange()
        self._visdata()
        self._setxaxislabel()
        self._setyaxislabel()
        self._addhoverlines()
        self._addlegend()
        self._addtimebars()

    def _format(self):
        # Formatting stuff
        self.fig.grid.grid_line_color = None
        self.fig.axis.major_tick_line_color = None
        self.fig.axis.major_label_standoff = 0
        self.fig.title = None
        self.fig.toolbar.active_drag = 'auto'
        if not self.show_xaxis:
            self.fig.xaxis.major_label_text_font_size = '0pt'
            self.fig.xaxis.visible = False

    def _setxrange(self):
        # Check if x range is not set, if not, set good ones
        if 'alt_range' not in pytplot.tplot_opt_glob:
            datasets = [pytplot.data_quants[self.tvar_name]]
            x_min_list = []
            x_max_list = []
            for oplot_name in pytplot.data_quants[self.tvar_name].attrs['plot_options']['overplots']:
                datasets.append(pytplot.data_quants[oplot_name])
            for dataset in datasets:
                coords = pytplot.tplot_utilities.return_interpolated_link_dict(dataset, ['alt'])
                alt = coords['alt'].values
                x_min_list.append(np.nanmin(alt.tolist()))
                x_max_list.append(np.nanmax(alt.tolist()))
            pytplot.tplot_opt_glob['alt_range'] = [np.nanmin(x_min_list), np.nanmax(x_max_list)]
            tplot_x_range = [np.nanmin(x_min_list), np.nanmax(x_max_list)]
            if self.show_xaxis:
                pytplot.lim_info['xfull'] = tplot_x_range
                pytplot.lim_info['xlast'] = tplot_x_range
        
        x_range = Range1d(pytplot.tplot_opt_glob['alt_range'][0], pytplot.tplot_opt_glob['alt_range'][1])
        
        self.fig.x_range = x_range
    
    def _setyrange(self):
        if self._getyaxistype() == 'log':
            if pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0] <= 0 \
                    or pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1] <= 0:
                return
        y_range = Range1d(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0],
                          pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1])
        self.fig.y_range = y_range
        
    def _setminborder(self):
        self.fig.min_border_bottom = pytplot.tplot_opt_glob['min_border_bottom']
        self.fig.min_border_top = pytplot.tplot_opt_glob['min_border_top']

    def _addtimebars(self):
        for time_bar in pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar']:
            time_bar_line = Span(location=time_bar['location'],
                                 dimension=time_bar['dimension'],
                                 line_color=time_bar['line_color'],
                                 line_width=time_bar['line_width'])
            self.fig.renderers.extend([time_bar_line])
        # grab tbardict
        tbardict = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar']
        ltbar = len(tbardict)
        # make sure data is in list format
        datasets = [pytplot.data_quants[self.tvar_name]]
        for oplot_name in pytplot.data_quants[self.tvar_name].attrs['plot_options']['overplots']:
            datasets.append(pytplot.data_quants[oplot_name])
        for dataset in datasets:
            # TODO: The below function is essentially a hack for now, because this code was written assuming the data was a dataframe object.
            # This needs to be rewritten to use xarray
            dataset = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(dataset.name, no_spec_bins=True)
            # for location in tbar dict
            for i in range(ltbar):
                # get times, color, point size
                test_time = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]["location"]
                color = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]["line_color"]
                pointsize = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]["line_width"]
                # correlate given time with corresponding data/alt points
                time = pytplot.data_quants[pytplot.data_quants[self.tvar_name].attrs['plot_options']['links']['alt']].coords['time'].values
                altitude = pytplot.data_quants[pytplot.data_quants[self.tvar_name].attrs['plot_options']['links']['alt']].values
                nearest_time_index = np.abs(time - test_time).argmin()
                data_point = dataset.iloc[nearest_time_index][0]
                alt_point = altitude[nearest_time_index]
                self.fig.circle([alt_point], [data_point], size=pointsize, color=color)
        return
            
    def _setxaxis(self):
        # Nothing to set for now
        return
        
    def _getyaxistype(self):
        if 'y_axis_type' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            return pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_axis_type']
        else:
            return 'linear'
        
    def _setcolors(self):
        if 'line_color' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']:
            self.colors = pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['line_color']

    def _setxaxislabel(self):
        if 'axis_label' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']:
            self.fig.xaxis.axis_label = pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['axis_label']
        self.fig.xaxis.axis_label = 'Altitude'
        self.fig.xaxis.axis_label_text_font_size = str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])+'pt'
        self.fig.xaxis.axis_label_text_color = self.get_axis_label_color()

    def _setyaxislabel(self):
        self.fig.yaxis.axis_label = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_label']
        self.fig.yaxis.axis_label_text_font_size = str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])+'pt'
        self.fig.yaxis.axis_label_text_color = self.get_axis_label_color()

    def _visdata(self):
        self._setcolors()

        # make sure data is in list format
        datasets = [pytplot.data_quants[self.tvar_name]]
        for oplot_name in pytplot.data_quants[self.tvar_name].attrs['plot_options']['overplots']:
            datasets.append(pytplot.data_quants[oplot_name])
        
        for dataset in datasets:                
            # Get Linestyle
            line_style = None
            if 'line_style' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['line_opt']:
                line_style = pytplot.data_quants[self.tvar_name].attrs['plot_options']['line_opt']['line_style']

            coords = pytplot.tplot_utilities.return_interpolated_link_dict(dataset, ['alt'])
            t_link = coords['alt'].coords['time'].values
            x = coords['alt'].values
            df = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(dataset.name, no_spec_bins=True)
            # Create lines from each column in the dataframe
            for column_name in df.columns:
                y = df[column_name]

                t_tvar = df.index.values
                y = df.values
                while t_tvar[-1] > t_link[-1]:
                    t_tvar = np.delete(t_tvar, -1)
                    y = np.delete(y, -1)
                while t_tvar[0] < t_link[0]:
                    t_tvar = np.delete(t_tvar, 0)
                    y = np.delete(y, 0)
                
                if self._getyaxistype() == 'log':
                    y[y <= 0] = np.NaN

                line_source = ColumnDataSource(data=dict(x=x, y=y))
                if self.auto_color:
                    line = Circle(x='x', y='y', line_color=self.colors[self.linenum % len(self.colors)])
                else:
                    line = Circle(x='x', y='y')
                if 'line_style' not in pytplot.data_quants[self.tvar_name].attrs['plot_options']['line_opt']:
                    if line_style is not None:
                        line.line_dash = line_style[self.linenum % len(line_style)]
                else:
                    line.line_dash = pytplot.data_quants[self.tvar_name].attrs['plot_options']['line_opt']['line_style']
                self.lineglyphs.append(self.fig.add_glyph(line_source, line))
                self.linenum += 1
    
    def _addhoverlines(self):
        # Add tools
        hover = HoverTool()
        hover.tooltips = [("Value", "@y")]
        self.fig.add_tools(hover)
        
    def _addlegend(self):
        # Add the Legend if applicable
        if 'legend_names' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            legend_names = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['legend_names']
            if len(legend_names) != self.linenum:
                print("Number of lines do not match length of legend names")
            legend = Legend()
            legend.location = (0, 0)
            legend_items = []
            j = 0
            for legend_name in legend_names:
                legend_items.append((legend_name, [self.lineglyphs[j]]))
                j = j+1
                if j >= len(self.lineglyphs):
                    break
            legend.items = legend_items
            legend.label_text_font_size = str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])+'pt'
            legend.border_line_color = None
            legend.glyph_height = int(self.fig.plot_height / (len(legend_items) + 1))
            self.fig.add_layout(legend, 'right')
