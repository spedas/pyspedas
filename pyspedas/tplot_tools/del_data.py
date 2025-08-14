# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pyspedas
import fnmatch
import logging


def del_data(name=None):
    """
    This function will delete tplot variables that are already stored in memory.  
    
    Parameters
    ----------
        name : str or list[str]
            Names of the tplot variables to be deleted.  If no name is provided, then
            all tplot variables will be deleted.  (wildcards accepted)
         
    Returns
    -------
        None
        
    Examples
    --------
        >>> # Delete Variable 1
        >>> import pyspedas
        >>> pyspedas.del_data("Variable1")

    """
    if name is None:
        name = '*'

    names=pyspedas.tnames(name)
    if len(names) < 1:
        logging.warning("del_data: No valid tplot variables found, returning")
        return

    for name in names:
        if isinstance(pyspedas.tplot_tools.data_quants[name], dict):
            temp_data_quants = pyspedas.tplot_tools.data_quants[name]
            str_name = temp_data_quants['name']
        else:
            temp_data_quants = pyspedas.tplot_tools.data_quants[name]
            str_name = temp_data_quants.name

        del pyspedas.tplot_tools.data_quants[str_name]
        
    return