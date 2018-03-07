import pyqtgraph as pg
import numpy as np
from .. import tplot_utilities 
from pytplot import tplot_opt_glob
from pyqtgraph.Qt import QtCore
from .CustomAxis.DateAxis import DateAxis
from .CustomImage.UpdatingImage import UpdatingImage
from .CustomAxis.BlankAxis import BlankAxis

class TVarFigure1D(pg.GraphicsLayout):
    def __init__(self, tvar, show_xaxis=False, mouse_function=None):
        
        self.tvar=tvar
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
        self.yaxis.setLabel(self.tvar.yaxis_opt['axis_label'])
    
    def _setxaxislabel(self):
        self.xaxis.setLabel("Time")
    
    def getfig(self):
        return self
    
    def _visdata(self):
        spec_keyword = self.tvar.extras.get('spec', False)
        if spec_keyword:
            self._setzrange()
            specplot = UpdatingImage(self.tvar.data, 
                                     self.tvar.spec_bins, 
                                     self.tvar.spec_bins_ascending, 
                                     self._getyaxistype(), 
                                     self._getzaxistype(),
                                     self.colormap,
                                     self.zmin,
                                     self.zmax)
            self.plotwindow.addItem(specplot)
        else:
            for i in range(0,len(self.tvar.data.columns)):
                self.curves.append(self.plotwindow.plot(self.tvar.data.index.tolist(), self.tvar.data[i].tolist(), pen=self.colors[i % len(self.colors)]))

    def _setyaxistype(self):
        if self._getyaxistype() == 'log':
            self.plotwindow.setLogMode(y=True)
        else:
            self.plotwindow.setLogMode(y=False)
        return
        
    def _addlegend(self):
        spec_keyword = self.tvar.extras.get('spec', False)
        if spec_keyword:
            zaxis=pg.AxisItem('right')
            
            if 'axis_label' in self.tvar.zaxis_opt:
                zaxis.setLabel(self.tvar.zaxis_opt['axis_label'])
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
            if self.zscale=='log':
                colorbar.setRect(QtCore.QRectF(0,np.log10(self.zmin),1,np.log10(self.zmax)-np.log10(self.zmin)))
                p2.setYRange(np.log10(self.zmin),np.log10(self.zmax), padding=0)
                #colorbar.setRect(QtCore.QRectF(0,3,1,3))
                #p2.setYRange(3,6, padding=0)
            else:
                colorbar.setRect(QtCore.QRectF(0,self.zmin,1,self.zmax-self.zmin))
                p2.setYRange(self.zmin,self.zmax, padding=0)
            colorbar.setLookupTable(self.colormap)
        else:
            if 'legend_names' in self.tvar.yaxis_opt:
                legend_names = self.tvar.yaxis_opt['legend_names']
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
        if 'y_axis_type' in self.tvar.yaxis_opt:
            return self.tvar.yaxis_opt['y_axis_type']
        else:
            return 'linear'
    
    def _setzaxistype(self):
        if self._getzaxistype() == 'log':
            self.zscale = 'log'
        else:
            self.zscale = 'linear'
    
    def _getzaxistype(self):
        if 'z_axis_type' in self.tvar.zaxis_opt:
            return  self.tvar.zaxis_opt['z_axis_type']
        else:
            return 'log'
            
    def _setcolors(self):
        if 'line_color' in self.tvar.extras:
            return self.tvar.extras['line_color']
        else: 
            return ['k', 'r', 'g', 'c', 'y', 'm', 'b']
    
    def _setcolormap(self):          
        if 'colormap' in self.tvar.extras:
            for cm in self.tvar.extras['colormap']:
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
            if self.tvar.yaxis_opt['y_range'][0] <0 or self.tvar.yaxis_opt['y_range'][1] < 0:
                return
            self.plotwindow.vb.setYRange(np.log10(self.tvar.yaxis_opt['y_range'][0]), np.log10(self.tvar.yaxis_opt['y_range'][1]), padding=0)
        else:
            self.plotwindow.vb.setYRange(self.tvar.yaxis_opt['y_range'][0], self.tvar.yaxis_opt['y_range'][1], padding=0)
    
    def _setzrange(self):
        #Get Z Range
        if 'z_range' in self.tvar.zaxis_opt:
            self.zmin = self.tvar.zaxis_opt['z_range'][0]
            self.zmax = self.tvar.zaxis_opt['z_range'][1]
        else:
            dataset_temp = self.tvar.data.replace([np.inf, -np.inf], np.nan)
            self.zmax = dataset_temp.max().max()
            self.zmin = dataset_temp.min().min()
            
            #Cannot have a 0 minimum in a log scale
            if self.zscale=='log':
                zmin_list = []
                for column in self.tvar.data.columns:
                    series = self.tvar.data[column]
                    zmin_list.append(series.iloc[series.nonzero()[0]].min())
                self.zmin = min(zmin_list)
    
    def _addtimebars(self):
        #Not yet implemented
        return
    
    