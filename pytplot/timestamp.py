from bokeh.core.properties import String
from bokeh.models import LayoutDOM
import os 
import datetime

from . import tplot_common

def timestamp(val):
    global extra_layouts
    
    if val is 'on':
        todaystring = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tplot_common.extra_layouts['time_stamp'] = todaystring
    else:
        if 'time_stamp' in tplot_globals.extra_layouts:
            del tplot_common.extra_layouts['time_stamp']
    
    return

class TimeStamp(LayoutDOM):
    __implementation__ = open(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "timestamp.coffee").read()
    text = String(default = "Testing")

    
def timestamp_help(in_date):
    
    form_datetime = datetime.datetime.utcfromtimestamp(in_date)
    form_string = form_datetime.strftime("%m/%d/%Y")
    
    return form_string
