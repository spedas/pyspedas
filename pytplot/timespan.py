# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from . import tplot_common
from . import tplot_utilities
from .xlim import xlim

def timespan(t1, dt, keyword = None):
    if keyword is None or keyword is 'days':
        # days is the duration
        dt *= 86400
    elif keyword is 'hours':
        dt *= 3600
    elif keyword is 'minutes':
        dt *= 60
    elif keyword is 'seconds':
        dt *= 1
    else:
        print("Invalid 'keyword' option.\nEnum(None, 'hours', 'minutes', 'seconds', 'days')")
        
    if not isinstance(t1, (int, float, complex)):
        t1 = tplot_utilities.str_to_int(t1)
    t2 = t1+dt
    xlim(t1, t2)
    
    return