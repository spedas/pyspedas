# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
from pytplot import lim_info, tplot_opt_glob

from .xlim import xlim

def tlimit(arg):
    global lim_info
    
    if arg is 'last':
        xlast = lim_info['xlast']
        lim_info['xlast'] = tplot_opt_glob['x_range']
        tplot_opt_glob['x_range'] = xlast
    elif arg is 'full':
        tplot_opt_glob['x_range'] = lim_info['xfull'] 
    elif isinstance(arg, list):
        minn = arg[0]
        maxx = arg[1]
        xlim(minn, maxx)
        
    return