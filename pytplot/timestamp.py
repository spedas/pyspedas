# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pytplot
import datetime

def timestamp(val):  
    """
    This function will turn on a time stamp that shows up at the bottom of every generated plot.
    
    Parameters
        val  str
            A string that can either be 'on' or 'off'.  
            
    Returns
        None
    
    Examples
         # Turn on the timestamp
         import pytplot
         pytplot.timestamp('on')
    """
    
    
    
    if val is 'on':
        todaystring = datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')
        pytplot.extra_layouts['time_stamp'] = todaystring
    else:
        if 'time_stamp' in pytplot.extra_layouts:
            del pytplot.extra_layouts['time_stamp']
    
    return