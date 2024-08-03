# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pytplot
from collections import OrderedDict
import logging

def tplot_rename(old_name, new_name):
    """
    This function will rename tplot variables that are already stored in memory.  
    
    Parameters
    ----------
        old_name : str 
            Old name of the Tplot Variable
        new_name : str
            New name of the Tplot Variable
         
    Returns
    -------
        None
        
    Examples
    --------
        >>> # Rename Variable 1 to Variable 2
        >>> import pytplot
        >>> pytplot.tplot_rename("Variable1", "Variable2")

    """

    #if old name input is a number, convert to corresponding name
    if isinstance(old_name, int):
        if isinstance(pytplot.data_quants[old_name], dict):
            old_name = pytplot.data_quants[old_name]['name']
        else:
            old_name = pytplot.data_quants[old_name].name

    # check if old name is in current dictionary
    if old_name not in pytplot.data_quants.keys():
        logging.info("The name %s is currently not in pytplot", old_name)
        return

    # remake dictionary with new name in old name's slot

    # Why not just delete/reinsert the variable being renamed?  Doing it this way
    # preserves the ordering of variables in the dictionary.  This matches the IDL
    # behavior, where if 'tha_fit' is the first variable in the list, with index 0,
    # tplot_rename,'tha_fit', 'tha_fit_rename'
    # keeps 'tha_fit_rename' at position 0.
    # No arrays are being copied here, only references, so it's not as inefficient as
    # it might look.
    # If the variable being renamed is part of a pseudovariable, you'll end up
    # with a dangling reference to the old name.  This also matches the IDL behavior,
    # but should it?   JWL 2024/07/31

    d = pytplot.data_quants
    d2 = OrderedDict([(new_name, v) if k == old_name else (k, v) for k, v in d.items()])
    new_data_quants = d2
    for key in d2:
        if isinstance(new_data_quants[key], dict):
            # the variable is non-record varying
            new_data_quants[key]['name'] = key
        else:
            new_data_quants[key].name = key
    
    pytplot.data_quants = new_data_quants
    return
