import pyqtgraph as pg


class AxisItem(pg.AxisItem):
    """
    GraphicsItem showing a single plot axis with ticks, values, and label.
    Can be configured to fit on any side of a plot, and can automatically synchronize its displayed scale with ViewBox
    items. Ticks can be extended to draw a grid.
    If maxTickLength is negative, ticks point into the plot.
    """

    def __init__(self, orientation, pen=None, linkView=None, parent=None, maxTickLength=5, showValues=True):
            pg.AxisItem.__init__(self, orientation, pen=None, linkView=None, parent=None, maxTickLength=-5,
                                 showValues=True)

    def _updateWidth(self):
        if not self.isVisible():
            w = 0
        else:
            if self.fixedWidth is None:
                if not self.style['showValues']:
                    w = 0
                elif self.style['autoExpandTextSpace'] is True:
                    w = self.textWidth
                else:
                    w = self.style['tickTextWidth']
                w += self.style['tickTextOffset'][0] if self.style['showValues'] else 0
                w += max(0, self.style['tickLength'])
                if self.label.isVisible():
                    # CHANGE
                    # This was originally multiplied by 0.8, however that resulted in a saved plot's colorbar label
                    # running into the tick labels
                    w += self.label.boundingRect().height() * 1.4  # bounding rect is usually an overestimate
            else:
                w = self.fixedWidth

        self.setMaximumWidth(w)
        self.setMinimumWidth(w)
        self.picture = None
