# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pyqtgraph as pg
import numpy as np
import os
import pytplot
from pyqtgraph.Qt import QtCore, QtGui
from .CustomImage.ColorbarImage import ColorbarImage
from .CustomAxis.BlankAxis import BlankAxis
from .CustomLegend.CustomLegend import CustomLegendItem
from .CustomAxis.AxisItem import AxisItem
from .CustomViewBox.NoPaddingPlot import NoPaddingPlot


class TVarFigureMap(pg.GraphicsLayout):
    def __init__(self, tvar_name, show_xaxis=False):
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
        self.yaxis = AxisItem("left")

        # Creating axes to bound the plots with lines
        self.xaxis2 = pg.AxisItem(orientation='top')
        self.xaxis2.setHeight(0)
        self.yaxis2 = AxisItem("right")
        self.yaxis2.setWidth(0)

        vb = NoPaddingPlot()
        self.plotwindow = self.addPlot(row=0, col=0, axisItems={'bottom': self.xaxis,
                                                                'left': self.yaxis,
                                                                "right": self.yaxis2,
                                                                "top": self.xaxis2}, viewBox=vb)

        self.plotwindow.vb.setLimits(xMin=0, xMax=360, yMin=-90, yMax=90)

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
        self.yaxis.setStyle(textFillLimits=pytplot.tplot_opt_glob["axis_tick_num"])  # Set an absurdly high number for the first 3, ensuring that at least 3 axis labels are always present

        if show_xaxis:
            self.plotwindow.showAxis('bottom')
        else:
            self.plotwindow.hideAxis('bottom')

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

    def buildfigure(self):
        self._setxrange()
        self._setyrange()
        self._setyaxistype()
        self._setzaxistype()
        self._setzrange()
        self._setbackground()
        self._visdata()
        self._setxaxislabel()
        self._setyaxislabel()
        self._addlegend()
        self._addtimebars()
        self._addtimelistener()
        if self.crosshair:
            self._set_crosshairs()
            self._addmouseevents()

    def _setxaxislabel(self):
        self.xaxis.setLabel("Longitude", **self.labelStyle)

    def _setyaxislabel(self):
        ylabel = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_label'].replace(" \ ", " <br> ")
        if "axis_subtitle" in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            sublabel = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_subtitle'].replace(" \ ", " <br> ")
            self.yaxis.setLabel(f"{ylabel} <br> {sublabel} ", **self.labelStyle)
        else:
            self.yaxis.setLabel(ylabel, **self.labelStyle)

    def getfig(self):
        return self

    def _visdata(self):
        datasets = [pytplot.data_quants[self.tvar_name]]
        for oplot_name in pytplot.data_quants[self.tvar_name].attrs['plot_options']['overplots']:
            datasets.append(pytplot.data_quants[oplot_name])

        cm_index = 0
        for dataset_xr in datasets:
            # TODO: The below function is essentially a hack for now, because this code was written assuming the data was a dataframe object.
            # This needs to be rewritten to use xarray
            dataset = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(dataset_xr.name, no_spec_bins=True)
            coords = pytplot.tplot_utilities.return_interpolated_link_dict(dataset_xr, ['lat', 'lon'])
            t_link = coords['lat'].coords['time'].values
            lat = coords['lat'].values
            # Need to trim down the data points to fit within the link
            t_tvar = dataset.index.values
            data = dataset[0].values
            while t_tvar[-1] > t_link[-1]:
                t_tvar = np.delete(t_tvar, -1)
                data = np.delete(data, -1)
            while t_tvar[0] < t_link[0]:
                t_tvar = np.delete(t_tvar, 0)
                data = np.delete(data, 0)

            t_link = coords['lon'].coords['time'].values
            lon = coords['lon'].values
            # Need to trim down the data points to fit within the link
            while t_tvar[-1] > t_link[-1]:
                t_tvar = np.delete(t_tvar, -1)
                data = np.delete(data, -1)
            while t_tvar[0] < t_link[0]:
                t_tvar = np.delete(t_tvar, 0)
                data = np.delete(data, 0)

            for column_name in dataset.columns:
                values = data.tolist()
                colors = pytplot.tplot_utilities.get_heatmap_color(color_map=
                                                                   self.colormap[cm_index % len(self.colormap)],
                                                                   min_val=self.zmin, max_val=self.zmax, values=values,
                                                                   zscale=self.zscale)
                brushes = []
                for color in colors:
                    brushes.append(pg.mkBrush(color))
                self.curves.append(self.plotwindow.scatterPlot(lon.tolist(), lat.tolist(),
                                                               pen=pg.mkPen(None), brush=brushes, size=4))
                cm_index += 1

    def _setyaxistype(self):
        if self._getyaxistype() == 'log':
            self.plotwindow.setLogMode(y=True)
        else:
            self.plotwindow.setLogMode(y=False)
        return

    def _addlegend(self):
        zaxis = AxisItem('right')
        zlabel = pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['axis_label'].replace(" \ ", " <br> ")
        if "axis_subtitle" in pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']:
            zsublabel = pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['axis_subtitle'].replace(" \ ", " <br> ")
            zaxis.setLabel(f"{zlabel} <br> {zsublabel}", **self.labelStyle)
        else:
            zaxis.setLabel(zlabel, **self.labelStyle)

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
        colorbar = ColorbarImage()
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
            time = pytplot.data_quants[pytplot.data_quants[self.tvar_name].attrs['plot_options']['links']['lat']].coords['time'].values
            latitude = pytplot.data_quants[pytplot.data_quants[self.tvar_name].attrs['plot_options']['links']['lat']].values
            longitude = pytplot.data_quants[pytplot.data_quants[self.tvar_name].attrs['plot_options']['links']['lon']].values
            # find closest time point to cursor
            radius = np.sqrt((latitude - index_y) ** 2 + (longitude - index_x) ** 2).argmin()

            time_point = time[radius]
            # get date and time
            date = (pytplot.tplot_utilities.int_to_str(time_point))[0:10]
            time = (pytplot.tplot_utilities.int_to_str(time_point))[11:19]

            # add crosshairs
            pytplot.hover_time.change_hover_time(time_point, name=self.tvar_name)
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
        if 'z_axis_type' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']:
            return pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['z_axis_type']
        else:
            return 'linear'

    def _setcolors(self):
        if 'line_color' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']:
            return pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['line_color']
        else:
            if pytplot.tplot_opt_glob['black_background']:
                return pytplot.tplot_utilities.rgb_color(['w', 'r', 'seagreen', 'b', 'darkturquoise', 'm', 'goldenrod'])
            else:
                return pytplot.tplot_utilities.rgb_color(['k', 'r', 'seagreen', 'b', 'darkturquoise', 'm', 'goldenrod'])

    def _setcolormap(self):
        colors = []
        if 'colormap' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']:
            for cm in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['colormap']:
                colors.append(pytplot.tplot_utilities.return_lut(cm))
            return colors
        else:
            return [pytplot.tplot_utilities.return_lut("inferno")]

    @staticmethod
    def getaxistype():
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
        if 'z_range' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']:
            self.zmin = pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['z_range'][0]
            self.zmax = pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['z_range'][1]
        else:
            dataset_temp = pytplot.data_quants[self.tvar_name].where(pytplot.data_quants[self.tvar_name] != np.inf)
            dataset_temp = dataset_temp.where(dataset_temp != -np.inf)
            # Cannot have a 0 minimum in a log scale
            if self.zscale == 'log':
                dataset_temp = dataset_temp.where(dataset_temp > 0)
            self.zmax = dataset_temp.max().max().values
            self.zmin = dataset_temp.min().min().values

    def _addtimebars(self):
        # grab tbardict
        tbardict = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar']
        ltbar = len(tbardict)

        for i in range(ltbar):
            # get times, color, point size
            test_time = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]["location"]
            color = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]["line_color"]
            pointsize = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]["line_width"]
            # correlate given time with corresponding lat/lon points
            time = pytplot.data_quants[pytplot.data_quants[self.tvar_name].attrs['plot_options']['links']['lat']].coords['time']
            latitude = pytplot.data_quants[pytplot.data_quants[self.tvar_name].attrs['plot_options']['links']['lat']].values
            longitude = pytplot.data_quants[pytplot.data_quants[self.tvar_name].attrs['plot_options']['links']['lon']].values
            nearest_time_index = np.abs(time - test_time).argmin()
            lat_point = latitude[nearest_time_index]
            lon_point = longitude[nearest_time_index]
            # color = pytplot.tplot_utilities.rgb_color(color)
            self.plotwindow.scatterPlot([lon_point], [lat_point], size=pointsize, pen=pg.mkPen(None), brush=color)

        return

    def _setbackground(self):
        if 'alpha' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']:
            alpha = pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['alpha']
        else:
            alpha = 1
        if 'basemap' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']:
            if os.path.isfile(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['basemap']):
                from matplotlib.pyplot import imread
                img = imread(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['basemap'],
                             format='RGBA')
                # Need to flip the image upside down...This will probably be fixed in
                # a future release, so this will need to be deleted at some point
                img = img[::-1]
                bm = ColorbarImage(image=img, opacity=alpha)
                bm.setRect(QtCore.QRect(0, -90, 360, 180))
                self.plotwindow.addItem(bm)

    def _set_crosshairs(self):
        if pytplot.tplot_opt_glob['black_background']:
            self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('w'))
            self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('w'))
        else:
            self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('k'))
            self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('k'))
        self.plotwindow.addItem(self.vLine, ignoreBounds=True)
        self.plotwindow.addItem(self.hLine, ignoreBounds=True)
        self.vLine.setVisible(False)
        self.hLine.setVisible(False)

    def _addtimelistener(self):
        self.spacecraft_position = self.plotwindow.scatterPlot([], [], size=14, pen=pg.mkPen(None), brush='b')
        pytplot.hover_time.register_listener(self._time_mover)

    def _time_mover(self, time, name):
        if name != self.tvar_name:
            hover_time = time
            time = \
            pytplot.data_quants[pytplot.data_quants[self.tvar_name].attrs['plot_options']['links']['lat']].coords[
                'time']
            latitude = pytplot.data_quants[
                pytplot.data_quants[self.tvar_name].attrs['plot_options']['links']['lat']].values
            longitude = pytplot.data_quants[
                pytplot.data_quants[self.tvar_name].attrs['plot_options']['links']['lon']].values
            nearest_time_index = np.abs(time - hover_time).argmin()
            lat_point = latitude[nearest_time_index]
            lon_point = longitude[nearest_time_index]
            self.spacecraft_position.setData([lon_point], [lat_point])
