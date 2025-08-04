import pyqtgraph as pg


class BlankAxis(pg.AxisItem):
    #Will need to override other functions in the future for this one
    #Right now it chooses weird stupid places for ticks
    def __init__(self, orientation, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        pg.AxisItem.__init__(self, orientation=orientation, pen=pen, linkView=linkView, parent=parent, maxTickLength=maxTickLength, showValues=showValues)
        
    def tickStrings(self, values, scale, spacing):
        strns = []        
        for _ in values:
            try:
                strns.append('')
            except ValueError: 
                strns.append('')
        return strns
    