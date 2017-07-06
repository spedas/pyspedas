# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from . import tplot_common

def tplot_names():
    index = 0
    return_names=[]
    for key, _ in tplot_common.data_quants.items():
        if isinstance(tplot_common.data_quants[key].data, list):
            if isinstance(key, str):
                
                names_to_print = tplot_common.data_quants[key].name + "  data from: "
                for name in tplot_common.data_quants[key].data:
                    names_to_print = names_to_print + " " + name
                print(index, ":", names_to_print)
                index+=1
        else:
            if isinstance(key, str):
                names_to_print = tplot_common.data_quants[key].name
                print(index, ":", names_to_print)
                index+=1
        return_names.append(names_to_print)
    return return_names