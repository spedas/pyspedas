# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import pytplot

from .xlim import xlim

def tlimit(arg):

    if arg is 'last':
        xlast = pytplot.lim_info['xlast']
        pytplot.lim_info['xlast'] = pytplot.tplot_opt_glob['x_range']
        pytplot.tplot_opt_glob['x_range'] = xlast
    elif arg is 'full':
        pytplot.tplot_opt_glob['x_range'] = pytplot.lim_info['xfull']
    elif isinstance(arg, list):
        minn = arg[0]
        maxx = arg[1]
        xlim(minn, maxx)
        
    return