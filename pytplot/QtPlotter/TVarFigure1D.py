import pyqtgraph as pg
import numpy as np
from .. import tplot_utilities 
import pytplot
from pytplot import tplot_opt_glob
from pyqtgraph.Qt import QtCore
from .CustomAxis.DateAxis import DateAxis
from .CustomAxis.BlankAxis import BlankAxis

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


    def buildfigure(self):
        self._setxrange()
        self._setyrange()
        self._setyaxistype()
        self._setzaxistype()
        self._setzrange()
        self._addtimebars()
        self._visdata()
        self._setyaxislabel()
        self._setxaxislabel()
        self._addmouseevents()
        self._addlegend()
    
    def _setyaxislabel(self):
        self.yaxis.setLabel(pytplot.data_quants[self.tvar_name].yaxis_opt['axis_label'])
    
    def _setxaxislabel(self):
        self.xaxis.setLabel("Time")
    
    def getfig(self):
        return self
    
    def _visdata(self):
        for i in range(0,len(pytplot.data_quants[self.tvar_name].data.columns)):
            self.curves.append(self.plotwindow.plot(pytplot.data_quants[self.tvar_name].data.index.tolist(), 
                                                    pytplot.data_quants[self.tvar_name].data[i].tolist(), 
                                                    pen=self.colors[i % len(self.colors)]))

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
        pos = evt
        if self.plotwindow.sceneBoundingRect().contains(pos):
            mousePoint = self.plotwindow.vb.mapSceneToView(pos)
            if self._mouseMovedFunction != None:
                self._mouseMovedFunction(int(mousePoint.x()))
    
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
        self.tvar_name.time_bar
        time_list = pytplot.data_quants[self.tvar_name].data.index
        date_to_highlight = []
        for i, val in enumerate(time_list):
            date_to_highlight = pytplot.tplot_utilities.str_to_int(self[i])
            pg.InfiniteLine(pos=date_to_highlight,pen=pg.mkPen(self.color),width = self.lwidth)
        return
    
    