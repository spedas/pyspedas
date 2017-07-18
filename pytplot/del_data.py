# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from . import tplot_common


def del_data(name):
    """
    This function will delete tplot variables that are already stored in memory.  
    
    Parameters:
        name : str 
            Name of the tplot variable to be deleted
         
    Returns:
        None
        
    Examples:
        >>> # Delete Variable 1
        >>> import pytplot
        >>> pytplot.del_data("Varaible1")

    """
    if not isinstance(name, list):
        name = [name]
    for i in name:
        if i not in tplot_common.data_quants.keys():
            print(str(i) + " is currently not in pytplot.")
            return
        
        temp_data_quants = tplot_common.data_quants[i]
        str_name = temp_data_quants.name
        
            
        del tplot_common.data_quants[str_name]
        
    return
