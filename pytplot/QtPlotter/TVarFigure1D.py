# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pyqtgraph as pg
import numpy as np
from .. import tplot_utilities 
import pytplot
from pytplot import tplot_opt_glob
from pyqtgraph.Qt import QtCore
from .CustomAxis.DateAxis import DateAxis
from .CustomAxis.BlankAxis import BlankAxis
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
from .CustomLegend.CustomLegend import CustomLegendItem
#import mpld3

class TVarFigure1D(pg.GraphicsLayout):
    def __init__(self, tvar_name, show_xaxis=False, mouse_function=None):
        
        self.tvar_name=tvar_name
        self.show_xaxis = show_xaxis
        
        #Sets up the layout of the Tplot Object
        pg.GraphicsLayout.__init__(self)
        self.layout.setHorizontalSpacing(50)
        self.layout.setContentsMargins(0,0,0,0)
        #Set up the x axis
        self.xaxis = DateAxis(orientation='bottom')
        self.xaxis.setHeight(35)
        self.xaxis.enableAutoSIPrefix(enable=False)
        #Set up the y axis
        self.yaxis = pg.AxisItem("left")
        self.yaxis.setWidth(100)
        
        self.plotwindow = self.addPlot(row=0, col=0, axisItems={'bottom': self.xaxis, 'left': self.yaxis})
        
        #Set up the view box needed for the legends
        self.legendvb = pg.ViewBox(enableMouse=False)
        self.legendvb.setMaximumWidth(100)
        self.legendvb.setXRange(0,1, padding=0)
        self.legendvb.setYRange(0,1, padding=0)
        self.addItem(self.legendvb,0,1)       
        
        
        self.curves = []
        self.colors = self._setcolors()
        self.colormap = self._setcolormap()

        if show_xaxis:
            self.plotwindow.showAxis('bottom')
        else:
            self.plotwindow.hideAxis('bottom')
        
        self._mouseMovedFunction = mouse_function

        ##
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('k'))
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('k'))
        self.plotwindow.addItem(self.vLine, ignoreBounds=True)
        self.plotwindow.addItem(self.hLine, ignoreBounds=True)
        self.vLine.setVisible(False)
        self.hLine.setVisible(False)
        
        self.label = pg.LabelItem(justify='left')
        self.addItem(self.label,row=1,col=0)
        #self.addItem(self.label)
        ##
        
        self.hoverlegend = CustomLegendItem(offset=(0,0))
        self.hoverlegend.setItem("Date:", "0")
        self.hoverlegend.setItem("Time:", "0")
        self.hoverlegend.setItem("Data:", "0")
        self.hoverlegend.setVisible(False)
        self.hoverlegend.setParentItem(self.plotwindow.vb)  
        
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
            for i in range(0,len(dataset.data.columns)):
                self.curves.append(self.plotwindow.plot(dataset.data.index.tolist(), 
                                                        dataset.data[i].tolist(), 
                                                        pen=self.colors[line_num % len(self.colors)]))
                line_num+=1

    def _setyaxistype(self):
        if self._getyaxistype() == 'log':
            self.plotwindow.setLogMode(y=True)
        else:
            self.plotwindow.setLogMode(y=False)
        return
        
    def _addlegend(self):
        if 'legend_names' in pytplot.data_quants[self.tvar_name].yaxis_opt:
            legend_names = pytplot.data_quants[self.tvar_name].yaxis_opt['legend_names']
            if len(legend_names) != len(self.curves):
                print("Number of lines do not match length of legend names")
            if len(legend_names) == 1:
                pos_array=[.5]
            else:
                pos_array=np.linspace(1,0,len(legend_names))
            i=0
            for legend_name in legend_names:
                if i+1 == len(legend_names): #Last
                    text = pg.TextItem(text=legend_name, anchor=(0,1.5), color=self.colors[i])
                elif i==0: #First
                    text = pg.TextItem(text=legend_name, anchor=(0,-.5), color=self.colors[i])
                else: #All others
                    text = pg.TextItem(text=legend_name, anchor=(0,0.5), color=self.colors[i])
                self.legendvb.addItem(text)
                text.setPos(0,pos_array[i])
                i+=1
    
    def _addmouseevents(self):
        if self.plotwindow.scene() is not None:
            self.plotwindow.scene().sigMouseMoved.connect(self._mousemoved)
    
    def _mousemoved(self, evt):
        #get current position
        pos = evt
        #if plot window contains position
        if self.plotwindow.sceneBoundingRect().contains(pos):
            mousePoint = self.plotwindow.vb.mapSceneToView(pos)
            #grab x and y mouse locations
            index_x = int(mousePoint.x())
            index_y = round(float(mousePoint.y()),4)
            date = (pytplot.tplot_utilities.int_to_str(index_x))[0:10]
            time = (pytplot.tplot_utilities.int_to_str(index_x))[11:19]
            #add crosshairs
            if self._mouseMovedFunction != None:
                self._mouseMovedFunction(int(mousePoint.x()))
                self.vLine.setPos(mousePoint.x())
                self.hLine.setPos(mousePoint.y())
                self.vLine.setVisible(True)
                self.hLine.setVisible(True)
                           
            self.hoverlegend.setVisible(True)
            self.hoverlegend.setItem("Date:", date)
            self.hoverlegend.setItem("Time:", time)
            self.hoverlegend.setItem("Data:", str(index_y))
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
            return ['k', 'r', 'g', 'c', 'y', 'm', 'b']
    
    def _setcolormap(self):          
        return
    
    def getaxistype(self):
        axis_type = 'time'
        link_y_axis = False
        return axis_type, link_y_axis
    
    def _setxrange(self):
        #Check if x range is set.  Otherwise, x range is automatic 
        if 'x_range' in tplot_opt_glob:
            self.plotwindow.setXRange(tplot_opt_glob['x_range'][0], tplot_opt_glob['x_range'][1])
    
    def _setyrange(self):
        if self._getyaxistype() == 'log':
            if pytplot.data_quants[self.tvar_name].yaxis_opt['y_range'][0] <0 or pytplot.data_quants[self.tvar_name].yaxis_opt['y_range'][1] < 0:
                return
            self.plotwindow.vb.setYRange(np.log10(pytplot.data_quants[self.tvar_name].yaxis_opt['y_range'][0]), np.log10(pytplot.data_quants[self.tvar_name].yaxis_opt['y_range'][1]), padding=0)
        else:
            self.plotwindow.vb.setYRange(pytplot.data_quants[self.tvar_name].yaxis_opt['y_range'][0], pytplot.data_quants[self.tvar_name].yaxis_opt['y_range'][1], padding=0)
    
    def _setzrange(self):
        return
    
    def _addtimebars(self):
        #find number of times to plot
        dict_length = len(pytplot.data_quants[self.tvar_name].time_bar)
        #for each time
        for i in range(dict_length):
            #pull date, color, thickness
            date_to_highlight = pytplot.data_quants[self.tvar_name].time_bar[i]["location"]
            color = pytplot.data_quants[self.tvar_name].time_bar[i]["line_color"]
            thick = pytplot.data_quants[self.tvar_name].time_bar[i]["line_width"]
            #make infinite line w/ parameters
            #color = pytplot.tplot_utilities.rgb_color(color)
            infline = pg.InfiniteLine(pos=date_to_highlight,pen=pg.mkPen(color,width = thick))
            #add to plot window
            self.plotwindow.addItem(infline)
                
        return
    
    