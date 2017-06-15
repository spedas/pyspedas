# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from . import tplot_common
from . import tplot_utilities

def tplot_options(option, value):
    
    option = option.lower()
    
    tplot_common.tplot_opt_glob = tplot_utilities.set_tplot_options(option, value, tplot_common.tplot_opt_glob)
    
    return
