import pyqtgraph as pg


class CustomVB(pg.ViewBox):

    def suggestPadding(self, axis):
        l = self.width() if axis == 0 else self.height()
        if l > 0:
            padding = 0
        else:
            padding = 0
        return padding

    def mouseDragEvent(self, ev, axis=None):
        return
