import pyqtgraph as pg
import numpy as np
from .. import tplot_utilities 
from pytplot import tplot_opt_glob
from pyqtgraph.Qt import QtCore
import pytplot
from .CustomAxis.DateAxis import DateAxis
from .CustomImage.UpdatingImage import UpdatingImage
from .CustomAxis.BlankAxis import BlankAxis

class TVarFigureSpec(pg.GraphicsLayout):
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
        zaxis=pg.AxisItem('right')
        
        if 'axis_label' in pytplot.data_quants[self.tvar_name].zaxis_opt:
            zaxis.setLabel(pytplot.data_quants[self.tvar_name].zaxis_opt['axis_label'])
        else:
            zaxis.setLabel(' ')
        
        if self.show_xaxis:
            emptyAxis=BlankAxis('bottom')
            emptyAxis.setHeight(35)
            p2 = self.addPlot(row=0, col=1, axisItems={'right':zaxis, 'bottom':emptyAxis}, enableMenu=False, viewBox=self.legendvb)
        else:
            p2 = self.addPlot(row=0, col=1, axisItems={'right':zaxis}, enableMenu=False, viewBox=self.legendvb)
            p2.hideAxis('bottom')
            
        p2.buttonsHidden=True
        p2.setMaximumWidth(100)
        p2.showAxis('right')
        p2.hideAxis('left')
        colorbar = pg.ImageItem()
        colorbar.setImage(np.array([np.linspace(1,2,200)]).T)
        
        p2.addItem(colorbar)
        p2.setLogMode(y=(self.zscale=='log'))
        p2.setXRange(0,1, padding=0)
        colorbar.setLookupTable(self.colormap)
        if self.zscale=='log':
            colorbar.setRect(QtCore.QRectF(0,np.log10(self.zmin),1,np.log10(self.zmax)-np.log10(self.zmin)))
            #I have literally no idea why this is true, but I need to set the range twice
            p2.setYRange(np.log10(self.zmin),np.log10(self.zmax), padding=0)
            p2.setYRange(np.log10(self.zmin),np.log10(self.zmax), padding=0)
        else:
            colorbar.setRect(QtCore.QRectF(0,self.zmin,1,self.zmax-self.zmin))
            p2.setYRange(self.zmin,self.zmax, padding=0)
        colorbar.setLookupTable(self.colormap)
        
    
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
        if 'z_axis_type' in pytplot.data_quants[self.tvar_name].zaxis_opt:
            return  pytplot.data_quants[self.tvar_name].zaxis_opt['z_axis_type']
        else:
            return 'log'
            
    def _setcolors(self):
        if 'line_color' in pytplot.data_quants[self.tvar_name].extras:
            return pytplot.data_quants[self.tvar_name].extras['line_color']
        else: 
            return ['k', 'r', 'g', 'c', 'y', 'm', 'b']
    
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
        #Get Z Range
        if 'z_range' in pytplot.data_quants[self.tvar_name].zaxis_opt:
            self.zmin = pytplot.data_quants[self.tvar_name].zaxis_opt['z_range'][0]
            self.zmax = pytplot.data_quants[self.tvar_name].zaxis_opt['z_range'][1]
        else:
            dataset_temp = pytplot.data_quants[self.tvar_name].data.replace([np.inf, -np.inf], np.nan)
            self.zmax = dataset_temp.max().max()
            self.zmin = dataset_temp.min().min()
            
            #Cannot have a 0 minimum in a log scale
            if self.zscale=='log':
                zmin_list = []
                for column in pytplot.data_quants[self.tvar_name].data.columns:
                    series = pytplot.data_quants[self.tvar_name].data[column]
                    zmin_list.append(series.iloc[series.nonzero()[0]].min())
                self.zmin = min(zmin_list)
    
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
            infline = pg.InfiniteLine(pos=date_to_highlight,pen=pg.mkPen(color,width = thick))
            #add to plot window
            self.plotwindow.addItem(infline)
                
        return
    
    