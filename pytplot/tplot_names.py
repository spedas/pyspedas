# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from pytplot import data_quants

def tplot_names():
    """
    This function will print out and return a list of all current Tplot Variables stored in the memory.  
    
    Parameters:
        None
         
    Returns:
        list : list of str
            A list of all Tplot Variables stored in the memory
            
    Examples:
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> tnames = pyplot.tplot_names()
        0 : Variable 1

    """
    
    index = 0
    return_names=[]
    for key, _ in data_quants.items():
        if isinstance(data_quants[key].data, list):
            if isinstance(key, str):
                
                names_to_print = data_quants[key].name + "  data from: "
                for name in data_quants[key].data:
                    names_to_print = names_to_print + " " + name
                print(index, ":", names_to_print)
                index+=1
        else:
            if isinstance(key, str):
                names_to_print = data_quants[key].name
                print(index, ":", names_to_print)
                index+=1
        return_names.append(names_to_print)
    return return_names