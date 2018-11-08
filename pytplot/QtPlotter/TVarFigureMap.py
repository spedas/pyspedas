# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pyqtgraph as pg
import numpy as np
import os
import pytplot
from pyqtgraph.Qt import QtCore
from .CustomAxis.BlankAxis import BlankAxis
from .CustomLegend.CustomLegend import CustomLegendItem
from .CustomViewBox.NoPaddingPlot import NoPaddingPlot


class TVarFigureMap(pg.GraphicsLayout):
    def __init__(self, tvar_name, show_xaxis=False, mouse_function=None):
        self.tvar_name = tvar_name
        self.show_xaxis = show_xaxis
        self.crosshair = pytplot.tplot_opt_glob['crosshair']

        # Sets up the layout of the Tplot Object
        pg.GraphicsLayout.__init__(self)
        self.layout.setHorizontalSpacing(50)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # Set up the x axis
        self.xaxis = pg.AxisItem(orientation='bottom')
        self.xaxis.setHeight(35)
        self.xaxis.enableAutoSIPrefix(enable=False)
        # Set up the y axis
        self.yaxis = pg.AxisItem("left")
        self.yaxis.setWidth(100)

        vb = NoPaddingPlot()
        self.plotwindow = self.addPlot(row=0, col=0, axisItems={'bottom': self.xaxis, 'left': self.yaxis}, viewBox=vb)
        self.plotwindow.vb.setLimits(xMin=0, xMax=360, yMin=-90, yMax=90)

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
        self.hoverlegend.setItem("Date: ", "0")
        self.hoverlegend.setItem("Time: ", "0")
        self.hoverlegend.setItem("Latitude:", "0")
        self.hoverlegend.setItem("Longitude:", "0")
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
        self._setbackground()
        self._visdata()
        self._setyaxislabel()
        self._setxaxislabel()
        self._addlegend()
        self._addtimebars()
        if self.crosshair:
            self._set_crosshairs()
            self._addmouseevents()

    def _setyaxislabel(self):
        self.yaxis.setLabel("Latitude")

    def _setxaxislabel(self):
        self.xaxis.setLabel("Longitude")

    def getfig(self):
        return self

    def _visdata(self):
        datasets = []
        if isinstance(pytplot.data_quants[self.tvar_name].data, list):
            for oplot_name in pytplot.data_quants[self.tvar_name].data:
                datasets.append(pytplot.data_quants[oplot_name])
        else:
            datasets.append(pytplot.data_quants[self.tvar_name])

        cm_index = 0
        for dataset in datasets:
            _, lat = pytplot.get_data(dataset.links['lat'])
            lat = lat.transpose()[0]
            _, lon = pytplot.get_data(dataset.links['lon'])
            lon = lon.transpose()[0]
            for column_name in dataset.data.columns:
                values = dataset.data[column_name].tolist()
                colors = pytplot.tplot_utilities.get_heatmap_color(color_map=
                                                                   self.colormap[cm_index % len(self.colormap)],
                                                                   min_val=self.zmin, max_val=self.zmax, values=values,
                                                                   zscale=self.zscale)
                brushes = []
                for color in colors:
                    brushes.append(pg.mkBrush(color))
                self.curves.append(self.plotwindow.scatterPlot(lon.tolist(), lat.tolist(),
                                                               pen=pg.mkPen(None), brush=brushes))
                cm_index += 1

    def _setyaxistype(self):
        if self._getyaxistype() == 'log':
            self.plotwindow.setLogMode(y=True)
        else:
            self.plotwindow.setLogMode(y=False)
        return

    def _addlegend(self):
        zaxis = pg.AxisItem('right')

        if 'axis_label' in pytplot.data_quants[self.tvar_name].zaxis_opt:
            zaxis.setLabel(pytplot.data_quants[self.tvar_name].yaxis_opt['axis_label'])
        else:
            zaxis.setLabel(' ')

        if self.show_xaxis:
            emptyaxis = BlankAxis('bottom')
            emptyaxis.setHeight(35)
            p2 = self.addPlot(row=0, col=1, axisItems={'right': zaxis, 'bottom': emptyaxis}, enableMenu=False,
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
        if self.zscale == 'log':
            colorbar.setRect(QtCore.QRectF(0, np.log10(self.zmin), 1, np.log10(self.zmax) - np.log10(self.zmin)))
            # I have literally no idea why this is true, but I need to set the range twice
            p2.setYRange(np.log10(self.zmin), np.log10(self.zmax), padding=0)
            p2.setYRange(np.log10(self.zmin), np.log10(self.zmax), padding=0)
        else:
            colorbar.setRect(QtCore.QRectF(0, self.zmin, 1, self.zmax - self.zmin))
            p2.setYRange(self.zmin, self.zmax, padding=0)
        colorbar.setLookupTable(self.colormap[0])

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
            index_x = round(float(mousepoint.x()), 2)
            index_y = round(float(mousepoint.y()), 2)
            # get latitude and longitude arrays
            datasets = []
            if isinstance(pytplot.data_quants[self.tvar_name].data, list):
                for oplot_name in pytplot.data_quants[self.tvar_name].data:
                    datasets.append(pytplot.data_quants[oplot_name])
            else:
                datasets.append(pytplot.data_quants[self.tvar_name])

            time, latitude = pytplot.get_data(datasets[0].links['lat'])
            latitude = latitude.transpose()[0]
            time, longitude = pytplot.get_data(datasets[0].links['lon'])
            longitude = longitude.transpose()[0]
            # find closest time point to cursor
            radius = np.sqrt((latitude - index_y) ** 2 + (longitude - index_x) ** 2).argmin()
            time_point = time[radius]
            # get date and time
            date = (pytplot.tplot_utilities.int_to_str(time_point))[0:10]
            time = (pytplot.tplot_utilities.int_to_str(time_point))[11:19]

            # add crosshairs
            if self._mouseMovedFunction is not None:
                self._mouseMovedFunction(int(mousepoint.x()))
                self.vLine.setVisible(True)
                self.hLine.setVisible(True)
                self.vLine.setPos(mousepoint.x())
                self.hLine.setPos(mousepoint.y())

            # Set legend options
            self.hoverlegend.setVisible(True)
            self.hoverlegend.setItem("Date: ", date)
            self.hoverlegend.setItem("Time: ", time)
            self.hoverlegend.setItem("Longitude:", str(index_x))
            self.hoverlegend.setItem("Latitude:", str(index_y))
        else:
            self.hoverlegend.setVisible(False)
            self.vLine.setVisible(False)
            self.hLine.setVisible(False)

    def _getyaxistype(self):
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
            return 'linear'

    def _setcolors(self):
        if 'line_color' in pytplot.data_quants[self.tvar_name].extras:
            return pytplot.data_quants[self.tvar_name].extras['line_color']
        else:
            return pytplot.tplot_utilities.rgb_color(['k', 'r', 'seagreen', 'b', 'darkturquoise', 'm', 'goldenrod'])

    def _setcolormap(self):
        colors = []
        if 'colormap' in pytplot.data_quants[self.tvar_name].extras:
            for cm in pytplot.data_quants[self.tvar_name].extras['colormap']:
                colors.append(pytplot.tplot_utilities.return_lut(cm))
            return colors
        else:
            return [pytplot.tplot_utilities.return_lut("inferno")]

    def getaxistype(self):
        axis_type = 'lat'
        link_y_axis = True
        return axis_type, link_y_axis

    def _setxrange(self):
        # Check if x range is set. Otherwise, set it.
        if 'map_x_range' in pytplot.tplot_opt_glob:
            self.plotwindow.setXRange(pytplot.tplot_opt_glob['map_x_range'][0],
                                      pytplot.tplot_opt_glob['map_x_range'][1])
        else:
            self.plotwindow.setXRange(0, 360)

    def _setyrange(self):
        # Check if y range is set.  Otherwise, y range is automatic
        if 'map_y_range' in pytplot.tplot_opt_glob:
            self.plotwindow.setYRange(pytplot.tplot_opt_glob['map_y_range'][0],
                                      pytplot.tplot_opt_glob['map_y_range'][1])
        else:
            self.plotwindow.vb.setYRange(-90, 90)

    def _setzrange(self):
        # Get Z Range
        if 'z_range' in pytplot.data_quants[self.tvar_name].zaxis_opt:
            self.zmin = pytplot.data_quants[self.tvar_name].zaxis_opt['z_range'][0]
            self.zmax = pytplot.data_quants[self.tvar_name].zaxis_opt['z_range'][1]
        else:
            if isinstance(pytplot.data_quants[self.tvar_name].data, list):
                # Check the first one
                dataset_temp = pytplot.data_quants[pytplot.data_quants[self.tvar_name].data[0]].data.replace(
                    [np.inf, -np.inf], np.nan)
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
        # initialize dataset variable
        datasets = []
        # grab tbardict
        tbardict = pytplot.data_quants[self.tvar_name].time_bar
        ltbar = len(tbardict)
        # make sure data is in list format
        if isinstance(pytplot.data_quants[self.tvar_name].data, list):
            for oplot_name in pytplot.data_quants[self.tvar_name].data:
                datasets.append(pytplot.data_quants[oplot_name])
        else:
            datasets.append(pytplot.data_quants[self.tvar_name])
        for dataset in datasets:
            # for location in tbar dict
            for i in range(ltbar):
                # get times, color, point size
                test_time = pytplot.data_quants[self.tvar_name].time_bar[i]["location"]
                color = pytplot.data_quants[self.tvar_name].time_bar[i]["line_color"]
                pointsize = pytplot.data_quants[self.tvar_name].time_bar[i]["line_width"]
                # correlate given time with corresponding lat/lon points
                time, latitude = pytplot.get_data(dataset.links['lat'])
                time, longitude = pytplot.get_data(dataset.links['lon'])
                latitude = latitude.transpose()[0]
                longitude = longitude.transpose()[0]
                nearest_time_index = np.abs(time - test_time).argmin()
                lat_point = latitude[nearest_time_index]
                lon_point = longitude[nearest_time_index]
                # color = pytplot.tplot_utilities.rgb_color(color)
                self.plotwindow.scatterPlot([lon_point], [lat_point], size=pointsize, pen=pg.mkPen(None), brush=color)

        return

    def _setbackground(self):
        if 'alpha' in pytplot.data_quants[self.tvar_name].extras:
            alpha = pytplot.data_quants[self.tvar_name].extras['alpha']
        else:
            alpha = 1
        if 'basemap' in pytplot.data_quants[self.tvar_name].extras:
            if os.path.isfile(pytplot.data_quants[self.tvar_name].extras['basemap']):
                from scipy import misc
                img = misc.imread(pytplot.data_quants[self.tvar_name].extras['basemap'], mode='RGBA')
                # Need to flip the image upside down...This will probably be fixed in
                # a future release, so this will need to be deleted at some point
                img = img[::-1]
                bm = pg.ImageItem(image=img, opacity=alpha)
                bm.setRect(QtCore.QRect(0, -90, 360, 180))
                self.plotwindow.addItem(bm)
