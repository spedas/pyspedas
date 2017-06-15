# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from . import tplot_common

def ylim(name, min, max, log_opt=False):
    
    if name not in tplot_common.data_quants.keys():
        print("That name is currently not in pytplot.")
        return
    
    temp_data_quant = tplot_common.data_quants[name]
    temp_data_quant.yaxis_opt['y_range'] = [min, max]
    
    return