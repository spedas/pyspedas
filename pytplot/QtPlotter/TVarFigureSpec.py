# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pyqtgraph as pg
import numpy as np
from .. import tplot_utilities
from pyqtgraph.Qt import QtCore
import pytplot
from .CustomAxis.DateAxis import DateAxis
from .CustomImage.UpdatingImage import UpdatingImage
from .CustomAxis.BlankAxis import BlankAxis
from .CustomLegend.CustomLegend import CustomLegendItem
from .CustomAxis.AxisItem import AxisItem
from .CustomViewBox.NoPaddingPlot import NoPaddingPlot


class TVarFigureSpec(pg.GraphicsLayout):
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
        self.yaxis = AxisItem('left')
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
        # Allow the user to set x-axis(time), y-axis, and z-axis data names in crosshairs
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].xaxis_opt['crosshair'] + ':', "0")
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].yaxis_opt['crosshair'] + ':', "0")
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].zaxis_opt['crosshair'] + ':', "0")
        self.hoverlegend.setVisible(False)
        self.hoverlegend.setParentItem(self.plotwindow.vb)

    def _set_crosshairs(self):
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('k'))
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('k'))
        self.plotwindow.addItem(self.vLine, ignoreBounds=True)
        self.plotwindow.addItem(self.hLine, ignoreBounds=True)

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
        self._addmouseevents()
        self._set_crosshairs()

    def _setxaxislabel(self):
        self.xaxis.setLabel(pytplot.data_quants[self.tvar_name].xaxis_opt['axis_label'])

    def _setyaxislabel(self):
        self.yaxis.setLabel(pytplot.data_quants[self.tvar_name].yaxis_opt['axis_label'])
        
    def getfig(self):
        return self

    def _visdata(self):
        self._setzrange()
        specplot = UpdatingImage(pytplot.data_quants[self.tvar_name].data,
                                 pytplot.data_quants[self.tvar_name].spec_bins,
                                 pytplot.data_quants[self.tvar_name].spec_bins_ascending,
                                 self._getyaxistype(),
                                 self._getzaxistype(),
                                 self.colormap,
                                 self.zmin,
                                 self.zmax)
        self.plotwindow.addItem(specplot)

    def _setyaxistype(self):
        if self._getyaxistype() == 'log':
            self.plotwindow.setLogMode(y=True)
        else:
            self.plotwindow.setLogMode(y=False)
        return

    def _addlegend(self):
        zaxis = AxisItem('right')
        zaxis.setLabel(pytplot.data_quants[self.tvar_name].zaxis_opt['axis_label'])

        if self.show_xaxis:
            emptyAxis = BlankAxis('bottom')
            emptyAxis.setHeight(35)
            p2 = self.addPlot(row=0, col=1, axisItems={'right': zaxis, 'bottom': emptyAxis}, enableMenu=False,
                              viewBox=self.legendvb)
        else:
            p2 = self.addPlot(row=0, col=1, axisItems={'right': zaxis}, enableMenu=False, viewBox=self.legendvb)
            p2.hideAxis('bottom')

        p2.buttonsHidden = True
        p2.setMaximumWidth(100)
        p2.showAxis('right')
        p2.hideAxis('left')
        colorbar = pg.ImageItem()
        colorbar.setImage(np.array([np.linspace(1, 2, 200)]).T)

        p2.addItem(colorbar)
        p2.setLogMode(y=(self.zscale == 'log'))
        p2.setXRange(0, 1, padding=0)
        colorbar.setLookupTable(self.colormap)
        if self.zscale == 'log':
            colorbar.setRect(QtCore.QRectF(0, np.log10(self.zmin), 1, np.log10(self.zmax) - np.log10(self.zmin)))
            # I have literally no idea why this is true, but I need to set the range twice
            p2.setYRange(np.log10(self.zmin), np.log10(self.zmax), padding=0)
            p2.setYRange(np.log10(self.zmin), np.log10(self.zmax), padding=0)
        else:
            colorbar.setRect(QtCore.QRectF(0, self.zmin, 1, self.zmax - self.zmin))
            p2.setYRange(self.zmin, self.zmax, padding=0)
        colorbar.setLookupTable(self.colormap)

    def _addmouseevents(self):
        if self.plotwindow.scene() is not None:
            self.plotwindow.scene().sigMouseMoved.connect(self._mousemoved)

    def _mousemoved(self, evt):
        # get current position
        pos = evt
        flag = 0
        # if plot window contains position
        if self.plotwindow.sceneBoundingRect().contains(pos):
            mousePoint = self.plotwindow.vb.mapSceneToView(pos)
            # grab x and y mouse locations
            index_x = int(mousePoint.x())
            # set log magnitude if log plot
            if self._getyaxistype() == 'log':
                index_y = 10 ** (round(float(mousePoint.y()), 4))
            else:
                index_y = round(float(mousePoint.y()), 4)

            dataframe = pytplot.data_quants[self.tvar_name].data
            specframe = pytplot.data_quants[self.tvar_name].spec_bins

            # find closest time/data to cursor location
            x = np.asarray(dataframe.index.tolist())
            x_sub = abs(x - index_x * np.ones(len(x)))
            x_argmin = np.nanargmin(x_sub)
            x_closest = x[x_argmin]
            speclength = len(specframe.loc[0])
            y = np.asarray((specframe.loc[0, 0:speclength - 1]))
            y_sub = abs(y - index_y * np.ones(y.size))
            y_argmin = np.nanargmin(y_sub)
            y_closest = y[y_argmin]
            index = int((np.nonzero(y == y_closest))[0])
            dp = dataframe[index][x_closest]

            # add crosshairs
            if self._mouseMovedFunction is not None:
                # Associate mouse position with current plot you're mousing over.
                self._mouseMovedFunction(int(mousePoint.x()), name=self.tvar_name)
                if self.crosshair:
                    self.vLine.setPos(mousePoint.x())
                    self.hLine.setPos(mousePoint.y())
                    self.vLine.setVisible(True)
                    self.hLine.setVisible(True)

            date = (pytplot.tplot_utilities.int_to_str(x_closest))[0:10]
            time = (pytplot.tplot_utilities.int_to_str(x_closest))[11:19]

            # Set legend options
            if self.crosshair:
                self.hoverlegend.setVisible(True)
                self.hoverlegend.setItem("Date:", date)
                # Allow the user to set x-axis(time), y-axis, and z-axis data names in crosshairs
                self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].xaxis_opt['crosshair'] + ':', time)
                self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].yaxis_opt['crosshair'] + ':', str(y_closest))
                self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].zaxis_opt['crosshair'] + ':', str(dp))

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
        if 'z_axis_type' in pytplot.data_quants[self.tvar_name].zaxis_opt:
            return pytplot.data_quants[self.tvar_name].zaxis_opt['z_axis_type']
        else:
            return 'log'

    def _setcolors(self):
        if 'line_color' in pytplot.data_quants[self.tvar_name].extras:
            return pytplot.data_quants[self.tvar_name].extras['line_color']
        else:
            return pytplot.tplot_utilities.rgb_color(['k', 'r', 'seagreen', 'b', 'darkturquoise', 'm', 'goldenrod'])

    def _setcolormap(self):
        if 'colormap' in pytplot.data_quants[self.tvar_name].extras:
            for cm in pytplot.data_quants[self.tvar_name].extras['colormap']:
                return tplot_utilities.return_lut(cm)
        else:
            return tplot_utilities.return_lut("inferno")

    def getaxistype(self):
        axis_type = 'time'
        link_y_axis = False
        return axis_type, link_y_axis

    def _setxrange(self):
        # Check if x range is set.  Otherwise, x range is automatic.
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
        # Get Z Range
        if 'z_range' in pytplot.data_quants[self.tvar_name].zaxis_opt:
            self.zmin = pytplot.data_quants[self.tvar_name].zaxis_opt['z_range'][0]
            self.zmax = pytplot.data_quants[self.tvar_name].zaxis_opt['z_range'][1]
        else:
            dataset_temp = pytplot.data_quants[self.tvar_name].data.replace([np.inf, -np.inf], np.nan)
            self.zmax = dataset_temp.max().max()
            self.zmin = dataset_temp.min().min()

            # Cannot have a 0 minimum in a log scale
            if self.zscale == 'log':
                zmin_list = []
                for column in pytplot.data_quants[self.tvar_name].data.columns:
                    series = pytplot.data_quants[self.tvar_name].data[column]
                    zmin_list.append(series.iloc[series.nonzero()[0]].min())
                self.zmin = min(zmin_list)

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
            # color = pytplot.tplot_utilities.rgb_color(color)
            infline = pg.InfiniteLine(pos=date_to_highlight, pen=pg.mkPen(color, width=thick))
            # add to plot window
            self.plotwindow.addItem(infline)

        return
