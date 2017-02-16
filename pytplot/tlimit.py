from __future__ import division
from . import tplot_common
from .xlim import xlim

def tlimit(arg):
    global lim_info
    
    if arg is 'last':
        xlast = tplot_common.lim_info['xlast']
        tplot_common.lim_info['xlast'] = tplot_common.tplot_opt_glob['x_range']
        tplot_common.tplot_opt_glob['x_range'] = xlast
    elif arg is 'full':
        tplot_common.tplot_opt_glob['x_range'] = tplot_common.lim_info['xfull']
    elif isinstance(arg, list):
        minn = arg[0]
        maxx = arg[1]
        xlim(minn, maxx)
        
    return