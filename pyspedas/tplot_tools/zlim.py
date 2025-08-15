# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pyspedas
import logging
from pyspedas.tplot_tools import options

def zlim(name, min, max, logflag=None):
    """
    This function will set the z axis range displayed for a specific tplot variable.
    This is only used for spec plots, where the z axis represents the magnitude of the values
    in each bin.  
    
    Parameters
    ----------
        name : str, int, list of str, list of int
            The names, indices, or wildcard patterns of the tplot variable that you wish to set z limits for.
        min : flt
            The start of the z axis.
        max : flt
            The end of the z axis.
        logflag: bool
            (Optional) If True, use logarithmic scale; if False, linear scale, if None, no change
            
    Returns
    -------
        None
    
    Examples
    --------
        >>> # Change the z range of Variable1 
        >>> import pyspedas
        >>> x_data = [1,2,3]
        >>> y_data = [ [1,2,3] , [4,5,6], [7,8,9] ]
        >>> v_data = [1,2,3]
        >>> pyspedas.store_data("Variable3", data={'x':x_data, 'y':y_data, 'v':v_data})
        >>> pyspedas.zlim('Variable1', 2, 3)

    """
    if logflag is None:
        options(name,'z_range',[min,max])
    else:
        options(name,'z_range',[min, max, logflag])
    return