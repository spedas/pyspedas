# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pytplot
from collections import OrderedDict

def tplot_rename(old_name, new_name):
    """
    This function will rename tplot variables that are already stored in memory.  
    
    Parameters:
        old_name : str 
            Old name of the Tplot Variable
        new_name : str
            New name of the Tplot Variable
         
    Returns:
        None
        
    Examples:
        >>> # Rename Variable 1 to Variable 2
        >>> import pytplot
        >>> pytplot.tplot_rename("Variable1", "Variable2")

    """
    
    #check if old name is in current dictionary
    if old_name not in pytplot.data_quants.keys():
        print("That name is currently not in pytplot")
        return
    #if old name input is a number, convert to corresponding name
    if isinstance(old_name, int):
        old_name = pytplot.data_quants[old_name].name
         
    #remake dictionary with new name in old name's slot
    d = pytplot.data_quants
    d2 = OrderedDict([(new_name, v) if k == old_name else (k, v) for k, v in d.items()])
    data_quants = d2
    for key in d2:
        data_quants[key].name = key
    
    return