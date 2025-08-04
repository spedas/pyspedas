import pyqtgraph as pg


class NoPaddingPlot(pg.ViewBox):

    def suggestPadding(self, axis):
        l = self.width() if axis == 0 else self.height()
        if l > 0:
            padding = 0.002
        else:
            padding = 0.002
        return padding