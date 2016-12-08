from . import tplot_common
from . import tplot_utilities

def tplot_options(option, value):
    
    option = option.lower()
    
    tplot_common.tplot_opt_glob = tplot_utilities.set_tplot_options(option, value, tplot_common.tplot_opt_glob)
    
    return
