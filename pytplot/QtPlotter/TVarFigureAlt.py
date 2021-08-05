# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pyqtgraph as pg
import numpy as np
import pytplot
from pyqtgraph.Qt import QtGui
from .CustomLegend.CustomLegend import CustomLegendItem
from .CustomAxis.AxisItem import AxisItem
from .CustomViewBox.NoPaddingPlot import NoPaddingPlot
from math import log10, floor

class TVarFigureAlt(pg.GraphicsLayout):
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
        self.yaxis = AxisItem("left")
        self.yaxis.setStyle(textFillLimits=pytplot.tplot_opt_glob["axis_tick_num"])  # Set an absurdly high number for the first 3, ensuring that at least 3 axis labels are always present
        vb = NoPaddingPlot()

        # Creating axes to bound the plots with lines
        self.xaxis2 = pg.AxisItem(orientation='top')
        self.xaxis2.setHeight(0)
        self.yaxis2 = AxisItem("right")
        self.yaxis2.setWidth(0)

        self.plotwindow = self.addPlot(row=0, col=0, axisItems={'bottom': self.xaxis,
                                                                'left': self.yaxis,
                                                                'right': self.yaxis2,
                                                                'top': self.xaxis2}, viewBox=vb)

        # Turn off zooming in on the y-axis, altitude resolution is much more important
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
        self.xaxis.setTickFont(font)
        self.yaxis.setTickFont(font)
        self.yaxis.setStyle(textFillLimits=pytplot.tplot_opt_glob["axis_tick_num"],
                            tickFont=font)  # Set an absurdly high number for the first 3, ensuring that at least 3 axis labels are always present

        if show_xaxis:
            self.plotwindow.showAxis('bottom')
        else:
            self.plotwindow.hideAxis('bottom')

        self._mouseMovedFunction = mouse_function

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

        self.label = pg.LabelItem(justify='left')
        self.addItem(self.label, row=1, col=0)

        # Set legend options
        self.hoverlegend = CustomLegendItem(offset=(0, 0))
        # Allow the user to set x-axis(time) and y-axis data names in crosshairs
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['crosshair'] + ':', "0")
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['crosshair'] + ':', "0")

        self.hoverlegend.setVisible(False)
        self.hoverlegend.setParentItem(self.plotwindow.vb)

    def buildfigure(self):
        self._setxrange()
        self._setyrange()
        self._setyaxistype()
        self._setzaxistype()
        self._setzrange()
        self._visdata()
        self._addtimebars()
        self._setxaxislabel()
        self._setyaxislabel()
        if self.crosshair:
            self._addmouseevents()
        self._addlegend()

    def getfig(self):
        return self

    def _setxaxislabel(self):
        self.xaxis.setLabel("Altitude", **self.labelStyle)

    def _setyaxislabel(self):
        ylabel = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_label'].replace(" \ ", " <br> ")
        if "axis_subtitle" in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            sublabel = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_subtitle'].replace(" \ ", " <br> ")
            self.yaxis.setLabel(f"{ylabel} <br> {sublabel}", **self.labelStyle)
        else:
            self.yaxis.setLabel(ylabel, **self.labelStyle)

    def _setyaxistype(self):
        if self._getyaxistype() == 'log':
            self.plotwindow.setLogMode(y=True)
        else:
            self.plotwindow.setLogMode(y=False)
        return

    def _getyaxistype(self):
        if 'y_axis_type' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            return pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_axis_type']
        else:
            return 'linear'

    def _setxrange(self):
        if 'alt_range' in pytplot.tplot_opt_glob:
            self.plotwindow.setXRange(pytplot.tplot_opt_glob['alt_range'][0], pytplot.tplot_opt_glob['alt_range'][1])
        else:
            return

    @staticmethod
    def getaxistype():
        axis_type = 'altitude'
        link_y_axis = False
        return axis_type, link_y_axis

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
            # add crosshairs
            if self._mouseMovedFunction is not None:
                self._mouseMovedFunction(int(mousepoint.x()))
                self.vLine.setPos(mousepoint.x())
                self.hLine.setPos(mousepoint.y())
                self.vLine.setVisible(True)
                self.hLine.setVisible(True)

            # Set legend options
            self.hoverlegend.setVisible(True)
            # Allow the user to set x-axis(time) and y-axis data names in crosshairs
            self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['crosshair'] + ':', index_x)
            self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['crosshair'] + ':', index_y)
        else:
            self.hoverlegend.setVisible(False)
            self.vLine.setVisible(False)
            self.hLine.setVisible(False)

    def _addlegend(self):
        if 'legend_names' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            legend_names = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['legend_names']
            if len(legend_names) != len(self.curves):
                print("Number of lines do not match length of legend names")
            if len(legend_names) == 1:
                pos_array = [.5]
            else:
                pos_array = np.linspace(1, 0, len(legend_names))
            i = 0
            for legend_name in legend_names:
                if i + 1 == len(legend_names):  # Last
                    text = pg.TextItem(text=legend_name, anchor=(0, 1.5), color=self.colors[i % len(self.colors)])
                elif i == 0:  # First
                    text = pg.TextItem(text=legend_name, anchor=(0, -.5), color=self.colors[i % len(self.colors)])
                else:  # All others
                    text = pg.TextItem(text=legend_name, anchor=(0, 0.5), color=self.colors[i % len(self.colors)])
                self.legendvb.addItem(text)
                text.setPos(0, pos_array[i])
                i += 1

    def _setzaxistype(self):
        if self._getzaxistype() == 'log':
            self.zscale = 'log'
        else:
            self.zscale = 'linear'

    def _getzaxistype(self):
        return

    def _setcolors(self):
        if 'line_color' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']:
            return pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['line_color']
        else:
            if pytplot.tplot_opt_glob['black_background']:
                return pytplot.tplot_utilities.rgb_color(['w', 'r', 'seagreen', 'b', 'darkturquoise', 'm', 'goldenrod'])
            else:
                return pytplot.tplot_utilities.rgb_color(['k', 'r', 'seagreen', 'b', 'darkturquoise', 'm', 'goldenrod'])

    def _setcolormap(self):
        return

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
                                         pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1], padding=0)

    def _setzrange(self):
        return

    def _addtimebars(self):
        # initialize dataset variable
        datasets = []
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
                self.plotwindow.scatterPlot([alt_point], [data_point], size=pointsize, pen=pg.mkPen(None), brush=color)
        return

    def _visdata(self):

        datasets = [pytplot.data_quants[self.tvar_name]]
        for oplot_name in pytplot.data_quants[self.tvar_name].attrs['plot_options']['overplots']:
            datasets.append(pytplot.data_quants[oplot_name])

        line_num = 0
        for dataset_xr in datasets:
            # TODO: The below function is essentially a hack for now, because this code was written assuming the data was a dataframe object.
            # This needs to be rewritten to use xarray
            dataset = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(dataset_xr.name, no_spec_bins=True)
            coords = pytplot.tplot_utilities.return_interpolated_link_dict(dataset_xr, ['alt'])
            for i in range(0, len(dataset.columns)):
                t_link = coords['alt'].coords['time'].values
                x = coords['alt'].values
                # Need to trim down the data points to fit within the link
                t_tvar = dataset.index.values
                data = dataset[i].values
                while t_tvar[-1] > t_link[-1]:
                    t_tvar = np.delete(t_tvar, -1)
                    data = np.delete(data, -1)
                while t_tvar[0] < t_link[0]:
                    t_tvar = np.delete(t_tvar, 0)
                    data = np.delete(data, 0)

                self.curves.append(self.plotwindow.scatterPlot(x.tolist(), data.tolist(),
                                                               pen=pg.mkPen(None), brush=self.colors[line_num %
                                                                                                     len(self.colors)]))
                line_num += 1
