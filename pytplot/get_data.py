# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from pytplot import data_quants

def get_data(name):
    """
    This function extracts the data from the Tplot Variables stored in memory.  
    
    Parameters:
        name : str 
            Name of the tplot variable
         
    Returns:
        time_val : pandas dataframe index
        data_val : list
            
    Examples:
        >>> # Retrieve the data from Variable 1
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> time, data = pytplot.get_data("Variable1")

    """
    
    global data_quants
    if name not in data_quants.keys():
        print("That name is currently not in pytplot")
        return
    
    temp_data_quant = data_quants[name]
    
    return temp_data_quant