# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pytplot

def zlim(name, min, max):
    """
    This function will set the z axis range displayed for a specific tplot variable.
    This is only used for spec plots, where the z axis represents the magnitude of the values
    in each bin.  
    
    Parameters:
        name : str
            The name of the tplot variable that you wish to set z limits for.  
        min : flt
            The start of the z axis.
        max : flt
            The end of the z axis.   
            
    Returns:
        None
    
    Examples:
        >>> # Change the z range of Variable1 
        >>> import pytplot
        >>> x_data = [1,2,3]
        >>> y_data = [ [1,2,3] , [4,5,6], [7,8,9] ]
        >>> v_data = [1,2,3]
        >>> pytplot.store_data("Variable3", data={'x':x_data, 'y':y_data, 'v':v_data})
        >>> pytplot.zlim('Variable1', 2, 3)

    """
    if name not in pytplot.data_quants.keys():
        print("That name is currently not in pytplot.")
        return

    pytplot.data_quants[name].attrs['plot_options']['zaxis_opt']['z_range'] = [min, max]
    
    return