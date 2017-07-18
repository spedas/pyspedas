# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

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
    """
    This function will turn on a time stamp that shows up at the bottom of every generated plot.
    
    Parameters:
        val : str
            A string that can either be 'on' or 'off'.  
            
    Returns:
        None
    
    Examples:
        >>> # Turn on the timestamp
        >>> import pytplot
        >>> pytplot.timestamp('on')

    """
    
    
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

