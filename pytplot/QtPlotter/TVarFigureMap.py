import pyqtgraph as pg
import numpy as np
import os
from .. import tplot_utilities 
from pytplot import tplot_opt_glob
import pytplot
from pyqtgraph.Qt import QtCore
from .CustomAxis.BlankAxis import BlankAxis

class TVarFigureMap(pg.GraphicsLayout):
    def __init__(self, tvar_name, show_xaxis=False, mouse_function=None):
        
        self.tvar_name=tvar_name
        self.show_xaxis = show_xaxis
        
        #Sets up the layout of the Tplot Object
        pg.GraphicsLayout.__init__(self)
        self.layout.setHorizontalSpacing(50)
        self.layout.setContentsMargins(0,0,0,0)
        #Set up the x axis
        self.xaxis = pg.AxisItem(orientation='bottom')
        self.xaxis.setHeight(35)
        self.xaxis.enableAutoSIPrefix(enable=False)
        #Set up the y axis
        self.yaxis = pg.AxisItem("left")
        self.yaxis.setWidth(100)
        
        
        self.plotwindow = self.addPlot(row=0, col=0, axisItems={'bottom': self.xaxis, 'left': self.yaxis})
        self.plotwindow.vb.setLimits(xMin=0, xMax=360, yMin=-90, yMax=90)
        
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
        self._setbackground()
        self._visdata()
        self._setyaxislabel()
        self._setxaxislabel()
        self._addmouseevents()
        self._addlegend()
        
    
    def _setyaxislabel(self):
        self.yaxis.setLabel("Longitude")
    
    def _setxaxislabel(self):
        self.xaxis.setLabel("Latitude")
    
    def getfig(self):
        return self
    
    def _visdata(self):    
        datasets = []
        if isinstance(pytplot.data_quants[self.tvar_name].data, list):
            for oplot_name in pytplot.data_quants[self.tvar_name].data:
                datasets.append(pytplot.data_quants[oplot_name])
        else:
            datasets.append(pytplot.data_quants[self.tvar_name])
        
        for dataset in datasets: 
            _, lat = pytplot.get_data(dataset.links['lat']) 
            lat = lat.transpose()[0]
            _, lon = pytplot.get_data(dataset.links['lon']) 
            lon = lon.transpose()[0]    
            for column_name in dataset.data.columns:
                values = dataset.data[column_name].tolist()
                colors = pytplot.tplot_utilities.get_heatmap_color(color_map=self.colormap, 
                                                                        min_val=self.zmin, 
                                                                        max_val=self.zmax, 
                                                                        values=values, 
                                                                        zscale=self.zscale)
                brushes = []
                for color in colors:
                    brushes.append(pg.mkBrush(color))
                self.curves.append(self.plotwindow.scatterPlot(lon.tolist(), lat.tolist(), 
                                                               pen=pg.mkPen(None), brush=brushes))
        
    def _setyaxistype(self):
        if self._getyaxistype() == 'log':
            self.plotwindow.setLogMode(y=True)
        else:
            self.plotwindow.setLogMode(y=False)
        return
        
    def _addlegend(self):
        zaxis=pg.AxisItem('right')
        
        if 'axis_label' in pytplot.data_quants[self.tvar_name].zaxis_opt:
            zaxis.setLabel(pytplot.data_quants[self.tvar_name].yaxis_opt['axis_label'])
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
            #I have literally no idea why this is true, but I need to set the range twice
            p2.setYRange(np.log10(self.zmin),np.log10(self.zmax), padding=0)
            p2.setYRange(np.log10(self.zmin),np.log10(self.zmax), padding=0)
        else:
            colorbar.setRect(QtCore.QRectF(0,self.zmin,1,self.zmax-self.zmin))
            p2.setYRange(self.zmin,self.zmax, padding=0)
        colorbar.setLookupTable(self.colormap)
    
    def _addmouseevents(self):
        return
    
    def _getyaxistype(self):
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
            return 'linear'
            
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
            return pytplot.tplot_utilities.return_lut("inferno")
    
    def getaxistype(self):
        axis_type = 'lat'
        link_y_axis = True
        return axis_type, link_y_axis
    
    def _setxrange(self):
        #Check if x range is set.  Otherwise, x range is automatic 
        self.plotwindow.setXRange(0,360)
    
    def _setyrange(self):
        self.plotwindow.vb.setYRange(-90, 90)
    
    def _setzrange(self):
        #Get Z Range
        if 'z_range' in pytplot.data_quants[self.tvar_name].zaxis_opt:
            self.zmin = pytplot.data_quants[self.tvar_name].zaxis_opt['z_range'][0]
            self.zmax = pytplot.data_quants[self.tvar_name].zaxis_opt['z_range'][1]
        else:
            if isinstance(pytplot.data_quants[self.tvar_name].data, list):
                #Check the first one
                dataset_temp = pytplot.data_quants[pytplot.data_quants[self.tvar_name].data[0]].data.replace([np.inf, -np.inf], np.nan)
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
        #Not yet implemented
        return
    
    def _setbackground(self):
        if 'alpha' in pytplot.data_quants[self.tvar_name].extras:
            alpha=pytplot.data_quants[self.tvar_name].extras['alpha']
        else:
            alpha=1
        if 'basemap' in pytplot.data_quants[self.tvar_name].extras:
            if os.path.isfile(pytplot.data_quants[self.tvar_name].extras['basemap']):
                from scipy import misc
                img = misc.imread(pytplot.data_quants[self.tvar_name].extras['basemap'], mode='RGBA') 
                #Need to flip the image upside down...This will probably be fixed in 
                #a future release, so this will need to be deleted at some point
                img = img[::-1]  
                bm = pg.ImageItem(image = img, opacity=alpha)
                bm.setRect(QtCore.QRect(0,-90, 360, 180))
                self.plotwindow.addItem(bm)