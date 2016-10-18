from bokeh.core.properties import String
import os 
from bokeh.models.annotations import ColorBar



class ColorBarSideTitle(ColorBar):
    __implementation__ = open(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "colorbarsidetitle.coffee").read()