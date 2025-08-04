
import pyqtgraph as pg

from pyqtgraph import GraphicsWidget
from pyqtgraph import LabelItem
from pyqtgraph import functions as fn
from pyqtgraph.Point import Point

__all__ = ['LegendItem']

class CustomLegendItem(pg.LegendItem):
        
    def addItem(self,name1,name2):
        label1 = LabelItem(name1)
        label2 = LabelItem(name2)
        row = self.layout.rowCount()
        self.items.append((label1, label2))
        self.layout.addItem(label1, row, 0)
        self.layout.addItem(label2, row, 1)
        self.updateSize()
    
    def removeItem(self, name):
        for label, data in self.items:
            if label.text == name:  # hit
                self.items.remove( (label, data) )    # remove from itemlist
                self.layout.removeItem(label)          # remove from layout
                label.close()                          # remove from drawing
                self.layout.removeItem(data)
                data.close()
                self.updateSize()                       # redraq box

    def setItem(self, label_name, new_data):
        for label, data in self.items:
            if label.text == label_name:
                data.setText(new_data)
                return
        self.addItem(label_name, new_data)
                
    def paint(self, p, *args):
        p.setPen(fn.mkPen(255,255,255,0))
        p.setBrush(fn.mkBrush(0,0,0,190))
        p.drawRect(self.boundingRect())

    def hoverEvent(self, ev):
        #ev.acceptDrags(QtCore.Qt.LeftButton)
        return
    
    def mouseDragEvent(self, ev):
        return
        #if ev.button() == QtCore.Qt.LeftButton:
        #    dpos = ev.pos() - ev.lastPos()
        #    self.autoAnchor(self.pos() + dpos)
