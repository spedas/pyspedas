import pyqtgraph as pg
from scipy import interpolate

class NonLinearAxis(pg.AxisItem):
    def __init__(self, orientation, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True, data=None):
        pg.AxisItem.__init__(self, orientation=orientation, pen=pen, linkView=linkView, parent=parent, maxTickLength=maxTickLength, showValues=showValues)
        self.data = data
        self.f = interpolate.interp1d(data.data.index.tolist(), data.data[0].tolist())
        self.num_ticks = 4
    
    def tickStrings(self, values, scale, spacing):
        strns = []
        for x in values:
            try:
                strns.append(str(int(self.f(x))))
            except ValueError:
                strns.append('')
        return strns
    
    def tickValues(self, minVal, maxVal, size):
        minVal, maxVal = sorted((minVal, maxVal))
        minVal *= self.scale  
        maxVal *= self.scale
        ticks=[]
        xrange = maxVal - minVal
        for i in range(0, self.num_ticks+1):
            ticks.append(minVal+(i*xrange/self.num_ticks))
        return [(1.0,ticks)]