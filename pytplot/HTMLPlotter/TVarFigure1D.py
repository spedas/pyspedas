# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import numpy as np
from bokeh.plotting.figure import Figure
from bokeh.models import (ColumnDataSource, DatetimeAxis, HoverTool, 
                          Range1d, Span, Title, Legend, BoxAnnotation)
from bokeh.models.glyphs import Line
from bokeh.models.tools import BoxZoomTool

import pytplot
from pytplot import tplot_utilities
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models.markers import X


dttf = DatetimeTickFormatter(microseconds=["%H:%M:%S"],                        
                             milliseconds=["%H:%M:%S"],
                             seconds=["%H: %M:%S"],
                             minsec=["%H:%M:%S"],
                             minutes=["%H:%M:%S"],
                             hourmin=["%H:%M:%S"],
                             hours=["%H:%M"],
                             days=["%F"],
                             months=["%F"],
                             years=["%F"])


class TVarFigure1D(object):
    
    def __init__(self, tvar_name, auto_color, show_xaxis=False, slice=False):
        self.tvar_name = tvar_name
        self.auto_color = auto_color
        self.show_xaxis = show_xaxis
        if 'show_all_axes' in pytplot.tplot_opt_glob:
            if pytplot.tplot_opt_glob['show_all_axes']:
                self.show_xaxis = True
        self.slice = slice
       
        # Variables needed across functions
        self.colors = ['black', 'red', 'green', 'navy', 'orange', 'firebrick', 'pink', 'blue', 'olive']
        self.lineglyphs = []
        self.linenum = 0
        self.interactive_plot = None

        self.fig = Figure(x_axis_type='datetime', 
                          tools=pytplot.tplot_opt_glob['tools'],
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
        axis_type = 'time'
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
        self._addtimebars()
        self._visdata()
        self._setxaxislabel()
        self._setyaxislabel()
        self._addhoverlines()
        self._addlegend()
    
    def _format(self):
        # Formatting stuff
        self.fig.grid.grid_line_color = None
        self.fig.axis.major_tick_line_color = None
        self.fig.axis.major_label_standoff = 0
        self.fig.xaxis.formatter = dttf
        self.fig.title = None
        self.fig.toolbar.active_drag = 'auto'
        if not self.show_xaxis:
            self.fig.xaxis.major_label_text_font_size = '0pt'
            self.fig.xaxis.visible = False
            
    def _setxrange(self):
        # Check if x range is not set, if not, set good ones
        if 'x_range' not in pytplot.tplot_opt_glob:
            datasets = [pytplot.data_quants[self.tvar_name]]
            x_min_list = []
            x_max_list = []
            for oplot_name in pytplot.data_quants[self.tvar_name].attrs['plot_options']['overplots']:
                datasets.append(pytplot.data_quants[oplot_name])
            for dataset in datasets:
                x_min_list.append(np.nanmin(dataset.coords['time']))
                x_max_list.append(np.nanmax(dataset.coords['time']))
            pytplot.tplot_opt_glob['x_range'] = [np.nanmin(x_min_list), np.nanmax(x_max_list)]
            tplot_x_range = [np.nanmin(x_min_list), np.nanmax(x_max_list)]
            if self.show_xaxis:
                pytplot.lim_info['xfull'] = tplot_x_range
                pytplot.lim_info['xlast'] = tplot_x_range
        
        # Bokeh uses milliseconds since epoch for some reason
        x_range = Range1d(int(pytplot.tplot_opt_glob['x_range'][0]) * 1000.0,
                          int(pytplot.tplot_opt_glob['x_range'][1]) * 1000.0)
        self.fig.x_range = x_range
    
    def _setyrange(self):
        if self._getyaxistype() == 'log':
            if pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0] <= 0 or \
                    pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1] <= 0:
                return
        y_range = Range1d(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0],
                          pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1])
        self.fig.y_range = y_range
        
    def _setminborder(self):
        self.fig.min_border_bottom = pytplot.tplot_opt_glob['min_border_bottom']
        self.fig.min_border_top = pytplot.tplot_opt_glob['min_border_top']
        if 'vertical_spacing' in pytplot.tplot_opt_glob:
            self.fig.min_border_bottom = int(pytplot.tplot_opt_glob['vertical_spacing'] / 2.0)
            self.fig.min_border_top = int(pytplot.tplot_opt_glob['vertical_spacing'] / 2.0)

    def _addtimebars(self):
        for time_bar in pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar']:
            time_bar_line = Span(location=time_bar['location']*1000.0, dimension=time_bar['dimension'],
                                 line_color=time_bar['line_color'], line_width=time_bar['line_width'])
            self.fig.renderers.extend([time_bar_line])

    def _set_roi_lines(self, dataset):
        # Locating the two times between which there's a roi
        time = dataset.coords['time'].values
        roi_1 = pytplot.tplot_utilities.str_to_int(pytplot.tplot_opt_glob['roi_lines'][0])
        roi_2 = pytplot.tplot_utilities.str_to_int(pytplot.tplot_opt_glob['roi_lines'][1])
        # find closest time to user-requested time
        x = np.asarray(time)
        x_sub_1 = abs(x - roi_1 * np.ones(len(x)))
        x_sub_2 = abs(x - roi_2 * np.ones(len(x)))
        x_argmin_1 = np.nanargmin(x_sub_1)
        x_argmin_2 = np.nanargmin(x_sub_2)
        x_closest_1 = x[x_argmin_1]
        x_closest_2 = x[x_argmin_2]
        # Create roi box
        roi_box = BoxAnnotation(left=x_closest_1*1000.0, right=x_closest_2*1000.0, fill_alpha=0.2, fill_color='grey',
                                line_color='red', line_width=2.5)
        self.fig.renderers.extend([roi_box])

    def _setxaxis(self):
        xaxis1 = DatetimeAxis(major_label_text_font_size='0pt', formatter=dttf)
        xaxis1.visible = False
        self.fig.add_layout(xaxis1, 'above')
        
    def _getyaxistype(self):
        if 'y_axis_type' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            return pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_axis_type']
        else:
            return 'linear'
        
    def _setcolors(self):
        if 'line_color' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']:
            self.colors = pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['line_color']

    def _setxaxislabel(self):
        self.fig.xaxis.axis_label = pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['axis_label']
        self.fig.xaxis.axis_label_text_font_size = str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])+'pt'
        self.fig.xaxis.axis_label_text_color = self.get_axis_label_color()

    def _setyaxislabel(self):
        self.fig.yaxis.axis_label = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_label']
        self.fig.yaxis.axis_label_text_font_size = str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])+'pt'
        self.fig.yaxis.axis_label_text_color = self.get_axis_label_color()

    def _visdata(self):
        self._setcolors()

        datasets = [pytplot.data_quants[self.tvar_name]]
        for oplot_name in pytplot.data_quants[self.tvar_name].attrs['plot_options']['overplots']:
            datasets.append(pytplot.data_quants[oplot_name])

        for dataset in datasets:
            # Get Linestyle
            line_style = None
            if 'linestyle' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']:
                line_style = pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['linestyle']
                
            # Get a list of formatted times
            corrected_time = [] 
            for x in dataset.coords['time'].values:
                corrected_time.append(tplot_utilities.int_to_str(x))
                
            # Bokeh uses milliseconds since epoch for some reason
            x = dataset.coords['time'].values * 1000.0

            # Add region of interest (roi) lines if applicable
            if 'roi_lines' in pytplot.tplot_opt_glob.keys():
                self._set_roi_lines(dataset)

            plot_options = dataset.attrs['plot_options']
            df = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(dataset.name, no_spec_bins=True)

            # Create lines from each column in the dataframe
            for column_name in df.columns:
                y = df[column_name]

                # Account for log plotting
                if self._getyaxistype() == 'log':
                    y.loc[y <= 0] = np.NaN

                if 'line_style' in plot_options['line_opt']:
                    if plot_options['line_opt']['line_style'] == 'scatter':
                        Glyph = X
                    else:
                        Glyph = Line
                else:
                    Glyph = Line
                # Until what size of a data gap are we removing nan values from the dataset? Set by the user
                # (default is to plot as bokeh would normally plot w/o worrying about data gap handling).
                limit = pytplot.tplot_opt_glob['data_gap']
                if limit != 0:
                    # Grabbing the times associated with nan values (nan_values), and the associated "position" of those
                    # keys in the dataset list (nan_keys)
                    nan_values = y[y.isnull().values].index.tolist()
                    nan_keys = [y.index.tolist().index(j) for j in nan_values]

                    nans = dict(zip(nan_keys, nan_values))

                    count = 0   # Keeping a count of how big of a time gap we have
                    consec_list = list()  # List of consecutive nan values (composed of indices for gaps not bigger than
                    # the user-specified data gap)
                    for val in range(len(nan_keys)):
                        # Avoiding some weird issues with going to the last data point in the nan dictionary keys
                        if val != (len(nan_keys)-1):
                            # Difference between one index and another - if consecutive indices, the diff will be 1
                            diff = abs(nan_keys[val] - nan_keys[val+1])
                            # calculate time accumulated from one index to the next
                            t_now = nan_values[val]
                            t_next = nan_values[val + 1]
                            time_accum = abs(t_now - t_next)
                            # If we haven't reached the allowed data gap, just keep track of how big of a gap we're at,
                            # and the indices in the gap
                            if diff == 1 and count < limit:
                                count += time_accum
                                consec_list.append(nan_keys[val])
                            # This triggers when we initially exceed the allowed data gap
                            elif diff == 1 and count >= limit:
                                pass
                            # When we find that the previous index and the current one are not consecutive, stop adding to
                            # the consec_list/overall_list (if applicable), and start over the count of time accumulated
                            # in a gap, as well as the consecutive list of time values with nans
                            elif diff != 1:
                                # Restart the count and add the current val to the list of nan values to remove
                                count = 0
                                consec_list.append(nan_keys[val])

                    times = x.tolist()
                    for elem in consec_list:
                        # Unless the data gap was big enough, we need to remove nan values from the data,
                        # otherwise bokeh will automatically NOT interpolate (the exact opposite of behavior in
                        # pyqtgraph, which ALWAYS interpolates...).
                        times.remove(nans[elem]*1000.0)
                        del y[nans[elem]]
                        del corrected_time[corrected_time.index(tplot_utilities.int_to_str(nans[elem]))]

                    # Data to be plotted
                    line_source = ColumnDataSource(data=dict(x=times, y=y, corrected_time=corrected_time))
                else:
                    # Data to be plotted
                    line_source = ColumnDataSource(data=dict(x=x, y=y, corrected_time=corrected_time))
                if self.auto_color:
                    line = Glyph(x='x', y='y', line_color=self.colors[self.linenum % len(self.colors)])
                else:
                    line = Glyph(x='x', y='y')
                if Glyph == Line:
                    if 'line_style' not in plot_options['line_opt']:
                        if line_style is not None:
                            line.line_dash = line_style[self.linenum % len(line_style)]
                    else:
                        line.line_dash = plot_options['line_style']
                self.lineglyphs.append(self.fig.add_glyph(line_source, line))
                self.linenum += 1

    def _addhoverlines(self):
        # Add tools
        hover = HoverTool()
        hover.tooltips = [("Time", "@corrected_time"), ("Value", "@y")]
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
