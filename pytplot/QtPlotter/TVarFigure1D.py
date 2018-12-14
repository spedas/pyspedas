# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pyqtgraph as pg
import numpy as np
import pytplot
from .CustomAxis.DateAxis import DateAxis
from .CustomLegend.CustomLegend import CustomLegendItem
from .CustomAxis.AxisItem import AxisItem
from .CustomViewBox.NoPaddingPlot import NoPaddingPlot
from pandas import Index


class TVarFigure1D(pg.GraphicsLayout):
    def __init__(self, tvar_name, show_xaxis=False, mouse_function=None):

        self.tvar_name = tvar_name
        self.show_xaxis = show_xaxis
        self.crosshair = pytplot.tplot_opt_glob['crosshair']

        # Sets up the layout of the Tplot Object
        pg.GraphicsLayout.__init__(self)
        self.layout.setHorizontalSpacing(50)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # Set up the x axis
        self.xaxis = DateAxis(orientation='bottom')
        self.xaxis.setHeight(35)
        self.xaxis.enableAutoSIPrefix(enable=False)
        # Set up the y axis
        self.yaxis = AxisItem("left")
        self.yaxis.setWidth(100)

        vb = NoPaddingPlot()
        self.plotwindow = self.addPlot(row=0, col=0, axisItems={'bottom': self.xaxis, 'left': self.yaxis}, viewBox=vb)

        # Set up the view box needed for the legends
        self.legendvb = pg.ViewBox(enableMouse=False)
        self.legendvb.setMaximumWidth(100)
        self.legendvb.setXRange(0, 1, padding=0)
        self.legendvb.setYRange(0, 1, padding=0)
        self.addItem(self.legendvb, 0, 1)

        self.curves = []
        self.colors = self._setcolors()
        self.colormap = self._setcolormap()

        if show_xaxis:
            self.plotwindow.showAxis('bottom')
        else:
            self.plotwindow.hideAxis('bottom')

        self._mouseMovedFunction = mouse_function

        self.label = pg.LabelItem(justify='left')
        self.addItem(self.label, row=1, col=0)

        # Set legend options
        self.hoverlegend = CustomLegendItem(offset=(0, 0))
        self.hoverlegend.setItem("Date:", "0")
        # Allow the user to set x-axis(time) and y-axis names in crosshairs
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].xaxis_opt['crosshair'] + ':', "0")
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].yaxis_opt['crosshair'] + ':', "0")
        self.hoverlegend.setVisible(False)
        self.hoverlegend.setParentItem(self.plotwindow.vb)

    def _set_crosshairs(self):
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('k'))
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('k'))
        self.plotwindow.addItem(self.vLine, ignoreBounds=True)
        self.plotwindow.addItem(self.hLine, ignoreBounds=True)
        self.vLine.setVisible(False)
        self.hLine.setVisible(False)

    def buildfigure(self):
        self._setxrange()
        self._setyrange()
        self._setyaxistype()
        self._setzaxistype()
        self._setzrange()
        self._visdata()
        self._setyaxislabel()
        self._setxaxislabel()
        self._addlegend()
        self._addtimebars()

        if self.crosshair:
            self._set_crosshairs()
            self._addmouseevents()

    def _setyaxislabel(self):
        self.yaxis.setLabel(pytplot.data_quants[self.tvar_name].yaxis_opt['axis_label'])

    def _setxaxislabel(self):
        self.xaxis.setLabel("Time")

    def getfig(self):
        return self

    def _visdata(self):
        datasets = []
        if isinstance(pytplot.data_quants[self.tvar_name].data, list):
            for oplot_name in pytplot.data_quants[self.tvar_name].data:
                datasets.append(pytplot.data_quants[oplot_name])
        else:
            datasets.append(pytplot.data_quants[self.tvar_name])
        line_num = 0

        for dataset in datasets:
            for i in range(len(dataset.data.columns)):
                limit = pytplot.tplot_opt_glob['data_gap']  # How big a data gap is allowed before those nans (default
                # is to plot as pyqtgraph would normally plot w / o worrying about data gap handling).
                if limit != 0:
                    index = 0  # What index in the below for loop we're on
                    nans = dict()  # Where nan value indices + times associated with those indices are housed
                    for j in dataset.data[i].keys():
                        point = dataset.data[i][j]  # Just grab the point in that dataset, at a specific time
                        if np.isnan(point):
                            nans[index] = j  # If we have a nan value, put the index/time in the nan dictionary
                        index += 1
                    # Putting the keys & values from the nans dictionary to lists to make them more easily accesible
                    nan_keys = list(nans.keys())
                    nan_values = list(nans.values())

                    count = 0   # Keeping a count of how big of a time gap we have
                    flag = False    # This flag changes to true when we accumulate a big enough period of time that we
                    #  exceed the user-specified data gap
                    consec_list = list()  # List of consecutive nan values (composed of indices for gaps not bigger than
                    # the user-specified data gap)
                    overall_list = list()  # List of consecutive nan values (composed of indices for gaps bigger than
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
                    time_filtered = np.array([1]*len(dataset.data.index.tolist()))
                    for index, pos in enumerate(overall_list):
                        # Remove unwanted time from being plotted
                        time_filtered[pos] = 0

                    # Finally, plot the thing with data gaps removed (if applicable)
                    self.curves.append(self.plotwindow.plot(x=dataset.data.index.tolist(),
                                                            y=dataset.data[i].tolist(),
                                                            pen=self.colors[line_num % len(self.colors)],
                                                            connect=time_filtered))
                else:
                    # Plot with interpolation of all data gaps
                    self.curves.append(self.plotwindow.plot(x=dataset.data.index.tolist(),
                                                            y=dataset.data[i].tolist(),
                                                            pen=self.colors[line_num % len(self.colors)]))

                line_num += 1

    def _setyaxistype(self):
        if self._getyaxistype() == 'log':
            self.plotwindow.setLogMode(y=True)
        else:
            self.plotwindow.setLogMode(y=False)
        return

    def _addlegend(self):
        if 'legend_names' in pytplot.data_quants[self.tvar_name].yaxis_opt:
            legend_names = pytplot.data_quants[self.tvar_name].yaxis_opt['legend_names']
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
                if i + 1 == len(legend_names):  # Last
                    text = pg.TextItem(text=legend_name, anchor=(0, 0.5), color=self.colors[i % len(self.colors)])
                elif i == 0:  # First
                    text = pg.TextItem(text=legend_name, anchor=(0, 0.5), color=self.colors[i % len(self.colors)])
                else:  # All others
                    text = pg.TextItem(text=legend_name, anchor=(0, 0.5), color=self.colors[i % len(self.colors)])
                self.legendvb.addItem(text)
                text.setPos(0, pos_array[i])
                i += 1

    def _addmouseevents(self):
        if self.plotwindow.scene() is not None:
            self.plotwindow.scene().sigMouseMoved.connect(self._mousemoved)

    def _mousemoved(self, evt):
        # get current position
        pos = evt
        # if plot window contains position
        if self.plotwindow.sceneBoundingRect().contains(pos):
            mousepoint = self.plotwindow.vb.mapSceneToView(pos)
            # grab x and y mouse locations
            index_x = int(mousepoint.x())
            index_y = round(float(mousepoint.y()), 4)
            date = (pytplot.tplot_utilities.int_to_str(index_x))[0:10]
            time = (pytplot.tplot_utilities.int_to_str(index_x))[11:19]
            # add crosshairs
            if self._mouseMovedFunction is not None:
                self._mouseMovedFunction(int(mousepoint.x()))
                self.vLine.setPos(mousepoint.x())
                self.hLine.setPos(mousepoint.y())
                self.vLine.setVisible(True)
                self.hLine.setVisible(True)

            self.hoverlegend.setVisible(True)
            self.hoverlegend.setItem("Date:", date)
            # Allow the user to set x-axis(time) and y-axis data names in crosshairs
            self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].xaxis_opt['crosshair'] + ':', time)
            self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].yaxis_opt['crosshair'] + ':', str(index_y))

        else:
            self.hoverlegend.setVisible(False)
            self.vLine.setVisible(False)
            self.hLine.setVisible(False)

    def _getyaxistype(self):
        if 'y_axis_type' in pytplot.data_quants[self.tvar_name].yaxis_opt:
            return pytplot.data_quants[self.tvar_name].yaxis_opt['y_axis_type']
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
        if 'line_color' in pytplot.data_quants[self.tvar_name].extras:
            return pytplot.data_quants[self.tvar_name].extras['line_color']
        else:
            return pytplot.tplot_utilities.rgb_color(['k', 'r', 'seagreen', 'b', 'darkturquoise', 'm', 'goldenrod'])

    def _setcolormap(self):
        return

    def getaxistype(self):
        axis_type = 'time'
        link_y_axis = False
        return axis_type, link_y_axis

    def _setxrange(self):
        # Check if x range is set.  Otherwise, x range is automatic
        if 'x_range' in pytplot.tplot_opt_glob:
            self.plotwindow.setXRange(pytplot.tplot_opt_glob['x_range'][0], pytplot.tplot_opt_glob['x_range'][1])

    def _setyrange(self):
        if self._getyaxistype() == 'log':
            if pytplot.data_quants[self.tvar_name].yaxis_opt['y_range'][0] < 0 or \
                    pytplot.data_quants[self.tvar_name].yaxis_opt['y_range'][1] < 0:
                return
            self.plotwindow.vb.setYRange(np.log10(pytplot.data_quants[self.tvar_name].yaxis_opt['y_range'][0]),
                                         np.log10(pytplot.data_quants[self.tvar_name].yaxis_opt['y_range'][1]),
                                         padding=0)
        else:
            self.plotwindow.vb.setYRange(pytplot.data_quants[self.tvar_name].yaxis_opt['y_range'][0],
                                         pytplot.data_quants[self.tvar_name].yaxis_opt['y_range'][1], padding=0)

    def _setzrange(self):
        return

    def _addtimebars(self):
        # find number of times to plot
        dict_length = len(pytplot.data_quants[self.tvar_name].time_bar)
        # for each time
        for i in range(dict_length):
            # pull date, color, thickness
            date_to_highlight = pytplot.data_quants[self.tvar_name].time_bar[i]["location"]
            color = pytplot.data_quants[self.tvar_name].time_bar[i]["line_color"]
            thick = pytplot.data_quants[self.tvar_name].time_bar[i]["line_width"]
            # make infinite line w/ parameters
            infline = pg.InfiniteLine(pos=date_to_highlight, pen=pg.mkPen(color, width=thick))
            # add to plot window
            self.plotwindow.addItem(infline)

        return
