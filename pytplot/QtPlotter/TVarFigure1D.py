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

        self.labelStyle = {'font-size': str(pytplot.data_quants[self.tvar_name].extras['char_size'])+'pt'}

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
        self._setxaxislabel()
        self._setyaxislabel()
        self._addlegend()
        self._addtimebars()

        if self.crosshair:
            self._set_crosshairs()
            self._addmouseevents()

    def _setxaxislabel(self):
        self.xaxis.setLabel("Time", **self.labelStyle)

    def _setyaxislabel(self):
        self.yaxis.setLabel(pytplot.data_quants[self.tvar_name].yaxis_opt['axis_label'], **self.labelStyle)

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
            for i in range(0, len(dataset.data.columns)):
                self.curves.append(self.plotwindow.plot(dataset.data.index.tolist(),
                                                        dataset.data[i].tolist(),
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
                def rgb(red, green, blue): return '#%02x%02x%02x' % (red, green, blue)
                r = self.colors[i % len(self.colors)][0]
                g = self.colors[i % len(self.colors)][1]
                b = self.colors[i % len(self.colors)][2]
                hex_num = rgb(r, g, b)
                color_text = 'color: ' + hex_num
                font_size = 'font-size: '+str(pytplot.data_quants[self.tvar_name].extras['char_size'])+'pt'
                opts = [color_text, font_size]
                full = "<span style='%s'>%s</span>" % ('; '.join(opts), legend_name)
                print(full)
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
