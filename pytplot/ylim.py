# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pytplot

def ylim(name, min, max):
    """
    This function will set the y axis range displayed for a specific tplot variable.
    
    Parameters:
        name : str
            The name of the tplot variable that you wish to set y limits for.  
        min : flt
            The start of the y axis.
        max : flt
            The end of the y axis.   
            
    Returns:
        None
    
    Examples:
        >>> # Change the y range of Variable1 
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> pytplot.ylim('Variable1', 2, 4)

    """
    if name not in pytplot.data_quants.keys():
        print("That name is currently not in pytplot.")
        return

    pytplot.data_quants[name].attrs['plot_options']['yaxis_opt']['y_range'] = [min, max]
    
    return