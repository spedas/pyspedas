# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pytplot
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from scipy import interpolate
from .CustomAxis.NonLinearAxis import NonLinearAxis
from .CustomViewBox.CustomVB import CustomVB
from .CustomAxis.AxisItem import AxisItem


class TVarFigureAxisOnly(pg.GraphicsLayout):
    def __init__(self, tvar_name):
        self.tvar_name = tvar_name
        
        # Sets up the layout of the Tplot Object
        pg.GraphicsLayout.__init__(self)
        self.layout.setHorizontalSpacing(10)
        self.layout.setContentsMargins(0, 0, 0, 0)

        if pytplot.tplot_opt_glob['black_background']:
            self.labelStyle = {'font-size':
                               str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])
                               + 'pt', 'color': '#FFF'}
        else:
            self.labelStyle = {'font-size':
                               str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])
                               + 'pt', 'color': '#000'}
        
        vb = CustomVB(enableMouse=False)
        self.yaxis = AxisItem("left")
        self.yaxis.setLabel(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_label'], **self.labelStyle)
        self.yaxis.label.setRotation(0)
        qt_transform = pg.QtGui.QTransform()
        qt_transform.translate(0,-40)
        self.yaxis.label.setTransform(qt_transform)
        #self.yaxis.label.translate(0, -40)
        mapping_function = interpolate.interp1d(pytplot.data_quants[self.tvar_name].coords['time'].values, pytplot.data_quants[self.tvar_name].values)
        if 'var_label_ticks' in pytplot.data_quants[self.tvar_name].attrs['plot_options']:
            num_ticks = pytplot.data_quants[self.tvar_name].attrs['plot_options']['var_label_ticks']
        else:
            num_ticks=5
        xaxis = NonLinearAxis(orientation='bottom', mapping_function=mapping_function, num_ticks=num_ticks)

        # Set the font size of the axes
        font = QtGui.QFont()
        font.setPixelSize(pytplot.tplot_opt_glob['axis_font_size'])
        xaxis.setTickFont(font)

        self.plotwindow = self.addPlot(row=0, col=0, axisItems={'bottom': xaxis, 'left': self.yaxis}, viewBox=vb, colspan=1)
        self.plotwindow.buttonsHidden = True
        self.plotwindow.setMaximumHeight(20)
        
        # Set up the view box needed for the legends
        self.legendvb = pg.ViewBox(enableMouse=False)
        self.legendvb.setMaximumWidth(100)
        self.addItem(self.legendvb, 0, 1)
