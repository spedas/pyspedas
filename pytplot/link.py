# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from pytplot import data_quants

def link(names, link_name, link_type='alt'):
    
    link_type = link_type.lower()
    if not isinstance(names, list):
        names = [names]
        
    for i in names:
        if i not in data_quants.keys():
            print(str(i) + " is currently not in pytplot.")
            return
        
        if isinstance(i,int):
            i = list(data_quants.keys())[i-1]
    
        data_quants[i].link_to_tvar(link_type, link_name)
                
    return
        
    