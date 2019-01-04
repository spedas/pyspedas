import pyqtgraph as pg
from pyqtgraph import functions as fn


class CustomLinearRegionItem(pg.LinearRegionItem):
    """Inheriting the LinearRegionItem class because if someone hovers over a region of interest box,
    I don't want it to have a different alpha value than when the mouse is not over the box."""

    def setMouseHover(self, hover):
        # Inform the item that the mouse is(not) hovering over it
        if self.mouseHovering == hover:
            return
        self.mouseHovering = hover
        if hover:
            c = self.brush.color()
            c.setAlpha(c.alpha() * 1)
            self.currentBrush = fn.mkBrush(c)
        else:
            self.currentBrush = self.brush
        self.update()
