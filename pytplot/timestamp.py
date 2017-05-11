from bokeh.core.properties import String
from bokeh.models import LayoutDOM
import os 
import datetime

from . import tplot_common

JS_CODE = '''
import * as p from "core/properties"
import {div, empty} from "core/dom"
import {LayoutDOM, LayoutDOMView} from "models/layouts/layout_dom"

export class TimeStampView extends LayoutDOMView

    initialize: (options) ->
        super(options)
        
        @render()
        
    render: () ->
        empty(@el)
        @el.appendChild(div({
          style: {
            'width': '800px'
            'word-spacing': '10px'
            'font-size': '11px'
            'color': '#000000'
            'background-color': '#ffffff'
            }
        }, "#{ @model.text }"))

export class TimeStamp extends LayoutDOM

    default_view: TimeStampView
    
    type: "TimeStamp"
    
    @define {
        text: [ p.String ]
    }
 


'''



def timestamp(val):  
    if val is 'on':
        todaystring = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tplot_common.extra_layouts['time_stamp'] = todaystring
    else:
        if 'time_stamp' in tplot_common.extra_layouts:
            del tplot_common.extra_layouts['time_stamp']
    
    return

class TimeStamp(LayoutDOM):
    __implementation__ = JS_CODE
    text = String(default = "Testing")

    
def timestamp_help(in_date):
    
    form_datetime = datetime.datetime.utcfromtimestamp(in_date)
    form_string = form_datetime.strftime("%m/%d/%Y")
    
    return form_string
