# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pyqtgraph as pg
import numpy as np
import pytplot
from pyqtgraph.Qt import QtGui
from .CustomAxis.DateAxis import DateAxis
from .CustomLegend.CustomLegend import CustomLegendItem
from .CustomAxis.AxisItem import AxisItem
from .CustomViewBox.NoPaddingPlot import NoPaddingPlot
from .CustomLinearRegionItem.CustomLinearRegionItem import CustomLinearRegionItem
from math import log10, floor

class TVarFigure1D(pg.GraphicsLayout):
    def __init__(self, tvar_name, show_xaxis=False):

        self.tvar_name = tvar_name
        self.show_xaxis = show_xaxis
        if 'show_all_axes' in pytplot.tplot_opt_glob:
            if pytplot.tplot_opt_glob['show_all_axes']:
                self.show_xaxis = True
        self.crosshair = pytplot.tplot_opt_glob['crosshair']

        # Sets up the layout of the Tplot Object
        pg.GraphicsLayout.__init__(self)
        self.layout.setHorizontalSpacing(10)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Set up the x axis
        if self.show_xaxis:
            self.xaxis = DateAxis(orientation='bottom')
            self.xaxis.setHeight(35)
        else:
            self.xaxis = DateAxis(orientation='bottom', showValues=False)
            self.xaxis.setHeight(0)
        self.xaxis.enableAutoSIPrefix(enable=False)

        # Set up the y axis
        self.yaxis = AxisItem("left")

        # Creating axes to bound the plots with lines
        self.xaxis2 = DateAxis(orientation='top', showValues=False)
        self.xaxis2.setHeight(0)
        self.yaxis2 = AxisItem("right", showValues=False)
        self.yaxis2.setWidth(0)

        vb = NoPaddingPlot()

        # Generate our plot in the graphics layout
        self.plotwindow = self.addPlot(row=0, col=0, axisItems={'bottom': self.xaxis,
                                                                'left': self.yaxis,
                                                                'right': self.yaxis2,
                                                                'top': self.xaxis2}, viewBox=vb)

        #Turn off zooming in on the y-axis, time resolution is much more important
        self.plotwindow.setMouseEnabled(y=pytplot.tplot_opt_glob['y_axis_zoom'])

        if pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['border']:
            self.plotwindow.showAxis("top")
            self.plotwindow.showAxis("right")

        # Set up the view box needed for the legends

        self.legendvb = pg.ViewBox(enableMouse=False)
        self.legendvb.setMaximumWidth(100)
        self.legendvb.setXRange(0, 1, padding=0)
        self.legendvb.setYRange(0, 1, padding=0)
        self.addItem(self.legendvb, 0, 1)

        self.curves = []
        self.colors = self._setcolors()
        self.colormap = self._setcolormap()

        if pytplot.tplot_opt_glob['black_background']:
            self.labelStyle = {'font-size':
                               str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])
                               + 'pt', 'color': '#FFF',
                               'white-space': 'pre-wrap'}
        else:
            self.labelStyle = {'font-size':
                               str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])
                               + 'pt', 'color': '#000',
                               'white-space': 'pre-wrap'}

        # Set the font size of the axes
        font = QtGui.QFont()
        font.setPixelSize(pytplot.tplot_opt_glob['axis_font_size'])
        self.xaxis.tickFont = font
        self.yaxis.tickFont = font
        self.yaxis.setStyle(textFillLimits=pytplot.tplot_opt_glob["axis_tick_num"]) # Set an absurdly high number for the first 3, ensuring that at least 3 axis labels are always present


        # Set legend options
        self.hoverlegend = CustomLegendItem(offset=(0, 0))
        self.hoverlegend.setItem("Date:", "0")
        # Allow the user to set x-axis(time) and y-axis names in crosshairs
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['crosshair']
                                 + ':', "0")
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['crosshair']
                                 + ':', "0")
        self.hoverlegend.setVisible(False)
        self.hoverlegend.setParentItem(self.plotwindow.vb)

    def _set_crosshairs(self):
        if pytplot.tplot_opt_glob["black_background"]:
            self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('w'))
            self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('w'))
        else:
            self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('k'))
            self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('k'))

        self.plotwindow.addItem(self.vLine, ignoreBounds=True)
        self.plotwindow.addItem(self.hLine, ignoreBounds=True)
        self.vLine.setVisible(False)
        self.hLine.setVisible(False)

    def _set_roi_lines(self):
        if 'roi_lines' in pytplot.tplot_opt_glob.keys():
            # Locating the two times between which there's a roi
            roi_1 = pytplot.tplot_utilities.str_to_int(pytplot.tplot_opt_glob['roi_lines'][0])
            roi_2 = pytplot.tplot_utilities.str_to_int(pytplot.tplot_opt_glob['roi_lines'][1])
            # find closest time to user-requested time
            x = pytplot.data_quants[self.tvar_name].coords['time']
            x_sub_1 = abs(x - roi_1 * np.ones(len(x)))
            x_sub_2 = abs(x - roi_2 * np.ones(len(x)))
            x_argmin_1 = np.nanargmin(x_sub_1)
            x_argmin_2 = np.nanargmin(x_sub_2)
            x_closest_1 = x[x_argmin_1]
            x_closest_2 = x[x_argmin_2]
            # Create roi box
            roi = CustomLinearRegionItem(orientation=pg.LinearRegionItem.Vertical, values=[x_closest_1, x_closest_2])
            roi.setBrush([211, 211, 211, 130])
            roi.lines[0].setPen('r', width=2.5)
            roi.lines[1].setPen('r', width=2.5)
            self.plotwindow.addItem(roi)

    def buildfigure(self):
        self._setxrange()
        self._setyrange()
        self._setyaxistype()
        self._setzaxistype()
        self._setzrange()
        self._visdata()
        self._setxaxislabel()
        self._setyaxislabel()
        self._addlegend()
        self._addtimebars()
        if self.crosshair:
            self._set_crosshairs()
            self._addmouseevents()
        self._set_roi_lines()

    def _setxaxislabel(self):
        if self.show_xaxis:
            self.xaxis.setLabel(pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['axis_label'], **self.labelStyle)

    def _setyaxislabel(self):
        ylabel = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_label'].replace(" \ ", " <br> ")
        if "axis_subtitle" in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            ysublabel = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_subtitle'].replace(" \ ", " <br> ")
            self.yaxis.setLabel(f"{ylabel} <br> {ysublabel}", **self.labelStyle)
        else:
            self.yaxis.setLabel(ylabel, **self.labelStyle)

    def getfig(self):
        return self

    def _visdata(self):
        datasets = [pytplot.data_quants[self.tvar_name]]
        for oplot_name in pytplot.data_quants[self.tvar_name].attrs['plot_options']['overplots']:
            datasets.append(pytplot.data_quants[oplot_name])
        line_num = 0

        for dataset in datasets:
            # TODO: The below function is essentially a hack for now, because this code was written assuming the data was a dataframe object.
            # This needs to be rewritten to use xarray
            plot_options = dataset.attrs['plot_options']
            dataset = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(dataset.name, no_spec_bins=True)

            for i in range(len(dataset.columns)):
                if 'line_style' in plot_options['line_opt']:
                    if plot_options['line_opt']['line_style'] == 'scatter':
                        self.curves.append(self.plotwindow.scatterPlot(x=dataset.index.tolist(),
                                                                       y=dataset[i].tolist(),
                                                                       pen=self.colors[line_num % len(self.colors)],
                                                                       symbol='+'))
                        line_num += 1
                        continue
                limit = pytplot.tplot_opt_glob['data_gap']  # How big a data gap is allowed before those nans (default
                # is to plot as pyqtgraph would normally plot w / o worrying about data gap handling).
                if limit != 0:
                    # Grabbing the times associated with nan values (nan_values), and the associated "position" of those
                    # keys in the dataset list (nan_keys)
                    nan_values = dataset[i][dataset[i].isnull().values].index.tolist()
                    nan_keys = [dataset[i].index.tolist().index(j) for j in nan_values]

                    count = 0   # Keeping a count of how big of a time gap we have
                    flag = False    # This flag changes to true when we accumulate a big enough period of time that we
                    #  exceed the user-specified data gap
                    consec_list = list()  # List of consecutive nan values (composed of indices for gaps not bigger than
                    # the user-specified data gap)
                    overall_list = list()  # List of consecutive nan values (composed of indices for gaps bigger than
                    # the user-specified data gap)
                    for val, actual_value in enumerate(nan_keys):
                        # Avoiding some weird issues with going to the last data point in the nan dictionary keys
                        if actual_value != nan_keys[-1]:
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
                            elif diff == 1 and count >= limit and not flag:
                                count += time_accum
                                # For some reason if you don't grab the point before the big data gap happened, when you
                                # plot this, the data gap isn't actually removed...
                                if consec_list[0] != 0:
                                    consec_list.insert(0, consec_list[0]-1)
                                # Put the current datagap into the list (overall_list) whose indices will actually be
                                # removed from the final plot
                                overall_list.append(consec_list)
                                overall_list.append([nan_keys[val]])
                                flag = True
                            # If we already exceeded the data gap, and the current index is still part of a gap,
                            # throw that index into the overall_list
                            elif diff == 1 and count > limit and flag:
                                count += time_accum
                                overall_list.append([nan_keys[val]])
                            # When we find that the previous index and the current one are not consecutive, stop adding
                            # to the consec_list/overall_list (if applicable), and start over the count of time
                            # accumulated in a gap, as well as the consecutive list of time values with nans
                            elif diff != 1:
                                count = 0
                                consec_list = []
                                flag = False
                                # For some reason if you don't grab the point after the last point where big data gap
                                # happened, when you plot, the data gap isn't actually removed...
                                if nan_keys[val-1] in [y for x in overall_list for y in x]:
                                    overall_list.append([nan_keys[val]])

                    # Flatten the overall_list to just one list, instead of a list of many lists
                    overall_list = [y for x in overall_list for y in x]

                    # Remove data gaps removed based on user-input acceptable time gap
                    # In order to do this, we set the identified indices from overall_list to 0, which in the
                    # connect keyword argument in self.plotwindow.plot will cause that point to not be plotted
                    time_filtered = np.array([1]*len(dataset.index.tolist()))
                    time_filtered[overall_list] = 0

                if limit != 0:
                    # Plot with interpolation of all data gaps
                    self.curves.append(self.plotwindow.plot(x=dataset.index.tolist(),
                                                            y=dataset[i].tolist(),
                                                            pen=self.colors[line_num % len(self.colors)],
                                                            connect=time_filtered))
                else:
                    # Plot with interpolation of all data gaps
                    self.curves.append(self.plotwindow.plot(x=dataset.index.tolist(),
                                                            y=dataset[i].tolist(),
                                                            pen=self.colors[line_num % len(self.colors)]))

                line_num += 1



    def _setyaxistype(self):
        if self._getyaxistype() == 'log':
            self.plotwindow.setLogMode(y=True)
        else:
            self.plotwindow.setLogMode(y=False)
        return

    def _addlegend(self):
        if 'legend_names' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            legend_names = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['legend_names']
            n_items = len(legend_names)
            bottom_bound = 0.5 + (n_items - 1) * 0.05
            top_bound = 0.5 - (n_items - 1) * 0.05
            if len(legend_names) != len(self.curves):
                print("Number of lines do not match length of legend names")
            if len(legend_names) == 1:
                pos_array = [.5]
            else:
                pos_array = np.linspace(bottom_bound, top_bound, len(legend_names))
            i = 0
            for legend_name in legend_names:
                def rgb(red, green, blue): return '#%02x%02x%02x' % (red, green, blue)
                r = self.colors[i % len(self.colors)][0]
                g = self.colors[i % len(self.colors)][1]
                b = self.colors[i % len(self.colors)][2]
                hex_num = rgb(r, g, b)
                color_text = 'color: ' + hex_num
                font_size = 'font-size: ' + str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])+'pt'
                opts = [color_text, font_size]
                full = "<span style='%s'>%s</span>" % ('; '.join(opts), legend_name)
                if i + 1 == len(legend_names):  # Last
                    text = pg.TextItem(anchor=(0, 0.5))
                    text.setHtml(full)
                elif i == 0:  # First
                    text = pg.TextItem(anchor=(0, 0.5))
                    text.setHtml(full)
                else:  # All others
                    text = pg.TextItem(anchor=(0, 0.5))
                    text.setHtml(full)
                self.legendvb.addItem(text)
                text.setPos(0, pos_array[i])
                i += 1

    def _addmouseevents(self):
        if self.plotwindow.scene() is not None:
            self.plotwindow.scene().sigMouseMoved.connect(self._mousemoved)

    def round_sig(self, x, sig=4):
        return round(x, sig - int(floor(log10(abs(x)))) - 1)

    def _mousemoved(self, evt):
        # get current position
        pos = evt
        # if plot window contains position
        if self.plotwindow.sceneBoundingRect().contains(pos):
            mousepoint = self.plotwindow.vb.mapSceneToView(pos)
            # grab x and y mouse locations
            index_x = int(mousepoint.x())
            # set log magnitude if log plot
            if self._getyaxistype() == 'log':
                index_y = self.round_sig(10 ** (float(mousepoint.y())), 4)
            else:
                index_y = round(float(mousepoint.y()), 4)

            date = (pytplot.tplot_utilities.int_to_str(index_x))[0:10]
            time = (pytplot.tplot_utilities.int_to_str(index_x))[11:19]
            # add crosshairs
            pytplot.hover_time.change_hover_time(int(mousepoint.x()), self.tvar_name)
            if self.crosshair:
                self.vLine.setPos(mousepoint.x())
                self.hLine.setPos(mousepoint.y())
                self.vLine.setVisible(True)
                self.hLine.setVisible(True)

                self.hoverlegend.setVisible(True)
                self.hoverlegend.setItem("Date:", date)
                # Allow the user to set x-axis(time) and y-axis data names in crosshairs
                self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['crosshair'] + ':', time)
                self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['crosshair'] + ':', str(index_y))

        else:
            self.hoverlegend.setVisible(False)
            self.vLine.setVisible(False)
            self.hLine.setVisible(False)

    def _getyaxistype(self):
        if 'y_axis_type' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            return pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_axis_type']
        else:
            return 'linear'

    def _setzaxistype(self):
        if self._getzaxistype() == 'log':
            self.zscale = 'log'
        else:
            self.zscale = 'linear'

    def _getzaxistype(self):
        return

    def _setcolors(self):
        if 'line_color' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']:
            return pytplot.tplot_utilities.rgb_color(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['line_color'])
        else:
            if pytplot.tplot_opt_glob["black_background"]:
                return pytplot.tplot_utilities.rgb_color(['w', 'r', 'seagreen', 'b', 'darkturquoise', 'm', 'goldenrod'])
            else:
                return pytplot.tplot_utilities.rgb_color(['k', 'r', 'seagreen', 'b', 'darkturquoise', 'm', 'goldenrod'])

    def _setcolormap(self):
        return

    @staticmethod
    def getaxistype():
        axis_type = 'time'
        link_y_axis = False
        return axis_type, link_y_axis

    def _setxrange(self):
        # Check if x range is set.  Otherwise, x range is automatic
        if 'x_range' in pytplot.tplot_opt_glob:
            self.plotwindow.setXRange(pytplot.tplot_opt_glob['x_range'][0], pytplot.tplot_opt_glob['x_range'][1])

    def _setyrange(self):
        if self._getyaxistype() == 'log':
            if pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0] <= 0 or \
                    pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1] <= 0:
                return
            self.plotwindow.vb.setYRange(np.log10(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0]),
                                         np.log10(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1]),
                                         padding=0)
        else:
            self.plotwindow.vb.setYRange(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0],
                                         pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1],
                                         padding=0)

    def _setzrange(self):
        return

    def _addtimebars(self):
        # find number of times to plot
        dict_length = len(pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'])
        # for each time
        for i in range(dict_length):
            # pull date, color, thickness, and dimensions
            if pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]["dimension"] == 'height':
                angle = 90
            else:
                angle = 0
            date_to_highlight = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]["location"]
            color = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]["line_color"]
            thick = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]["line_width"]
            # make infinite line w/ parameters
            infline = pg.InfiniteLine(pos=date_to_highlight, pen=pg.mkPen(color, width=thick), angle=angle)
            # add to plot window
            self.plotwindow.addItem(infline)

        return
