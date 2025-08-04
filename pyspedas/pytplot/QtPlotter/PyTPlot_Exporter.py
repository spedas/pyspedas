import pyqtgraph as pg
import numpy as np
import pyqtgraph.functions as fn
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.exporters import Exporter
from pyqtgraph.parametertree import Parameter


class PytplotExporter(pg.exporters.ImageExporter):

    def __init__(self, item):
        Exporter.__init__(self, item)
        tr = self.getTargetRect()
        if isinstance(item, QtGui.QGraphicsItem):
            scene = item.scene()
        else:
            scene = item
        # CHANGE: Used to be scene.views()[0].backgroundBrush()
        # That wasn't how to access the background of a GraphicsLayout object
        bgbrush = scene.backgroundBrush()
        bg = bgbrush.color()
        if bgbrush.style() == QtCore.Qt.NoBrush:
            bg.setAlpha(0)

        self.params = Parameter(name='params', type='group', children=[
            {'name': 'width', 'type': 'int', 'value': tr.width(), 'limits': (0, None)},
            {'name': 'height', 'type': 'int', 'value': tr.height(), 'limits': (0, None)},
            {'name': 'antialias', 'type': 'bool', 'value': True},
            {'name': 'background', 'type': 'color', 'value': bg},
        ])

        self.params.param('width').sigValueChanged.connect(self.widthChanged)
        self.params.param('height').sigValueChanged.connect(self.heightChanged)

    def export(self, fileName=None, toBytes=False, copy=False):
        if fileName is None and not toBytes and not copy:
            if pg.Qt.USE_PYSIDE:
                filter = ["*." + str(f) for f in QtGui.QImageWriter.supportedImageFormats()]
            else:
                filter = ["*." + bytes(f).decode('utf-8') for f in QtGui.QImageWriter.supportedImageFormats()]
            preferred = ['*.png', '*.tif', '*.jpg']
            for p in preferred[::-1]:
                if p in filter:
                    filter.remove(p)
                    filter.insert(0, p)
            self.fileSaveDialog(filter=filter)
            return

        targetRect = QtCore.QRect(0, 0, self.params['width'], self.params['height'])
        sourceRect = self.getSourceRect()


        # self.png = QtGui.QImage(targetRect.size(), QtGui.QImage.Format_ARGB32)
        # self.png.fill(pyqtgraph.mkColor(self.params['background']))
        w, h = self.params['width'], self.params['height']
        if w == 0 or h == 0:
            raise Exception("Cannot export image with size=0 (requested export size is %dx%d)" % (w, h))
        bg = np.empty((int(self.params['width']), int(self.params['height']), 4), dtype=np.ubyte)
        color = self.params['background']
        bg[:, :, 0] = color.blue()
        bg[:, :, 1] = color.green()
        bg[:, :, 2] = color.red()
        bg[:, :, 3] = color.alpha()
        self.png = fn.makeQImage(bg, alpha=True)

        # set resolution of image:
        origTargetRect = self.getTargetRect()
        resolutionScale = targetRect.width() / origTargetRect.width()

        painter = QtGui.QPainter(self.png)
        # dtr = painter.deviceTransform()
        try:
            self.setExportMode(True,
                               {'antialias': self.params['antialias'], 'background': self.params['background'],
                                'painter': painter, 'resolutionScale': resolutionScale})
            painter.setRenderHint(QtGui.QPainter.Antialiasing, self.params['antialias'])
            # CHANGE: Rendering the scence twice onto the QImage.  The first time, make it one pixel in size.
            # Next, render the full thing.  No idea why we need to render is twice, but we do.
            self.getScene().render(painter, QtCore.QRectF(0, 0, 1, 1), QtCore.QRectF(0, 0, 1, 1))
            self.getScene().render(painter, QtCore.QRectF(targetRect), QtCore.QRectF(sourceRect))
        finally:
            self.setExportMode(False)
        painter.end()

        if copy:
            QtGui.QApplication.clipboard().setImage(self.png)
        elif toBytes:
            return self.png
        else:
            self.png.save(fileName)

    def getPaintItems(self, root=None):
        """Return a list of all items that should be painted in the correct order."""
        if root is None:
            root = self.item
        preItems = []
        postItems = []
        if isinstance(root, QtGui.QGraphicsScene):
            childs = [i for i in root.items() if i.parentItem() is None]
            rootItem = []
        else:
            # CHANGE: For GraphicsLayouts, there is no function for childItems(), so I just
            # replaced it with .items()
            try:
                childs = root.childItems()
            except:
                childs = root.items()
            rootItem = [root]
        childs.sort(key=lambda a: a.zValue())
        while len(childs) > 0:
            ch = childs.pop(0)
            tree = self.getPaintItems(ch)

            if int(ch.flags() & ch.ItemStacksBehindParent) > 0 or (
                    ch.zValue() < 0 and int(ch.flags() & ch.ItemNegativeZStacksBehindParent) > 0):
                preItems.extend(tree)
            else:
                postItems.extend(tree)
        return preItems + rootItem + postItems

    def getTargetRect(self):
        # CHANGE: Used to return self.item.sceneBoundingRect().  GraphicsLayouts don't have a
        # sceneBoundingRect(), but they have a rect() which appears to work just as well.
        return self.item.rect()

    def getSourceRect(self):
        # CHANGE: Used to return self.item.mapRectToDevice(self.item.boundingRect()).  GraphicsLayouts don't have a
        # sceneBoundingRect() OR a mapRectToDevice, but they have a rect() which appears to work just as well.
        return self.item.rect()
