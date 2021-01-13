# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from pytplot import data_quants

def tplot_names(quiet=False):
    """
    This function will print out and return a list of all current Tplot Variables stored in the memory.  
    
    Parameters:
        quiet : bool
            If True, does not print out the variables (only returns the list variables)
         
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

    # TODO: Print out links as well?

    for key, _ in data_quants.items():
        if isinstance(data_quants[key], dict):
            # non-record varying variables are stored as dictionaries
            if isinstance(key, str):
                names_to_print = key

            if quiet != True:
                print(index, ":", names_to_print)

            return_names.append(names_to_print)
            index += 1
            continue

        if len(data_quants[key].attrs['plot_options']['overplots']) != 0:
            names_to_print = data_quants[key].name + "  data from: "
            for oplot_name in data_quants[key].attrs['plot_options']['overplots']:
                names_to_print = names_to_print + " " + oplot_name

        else:
            if isinstance(key, str):
                names_to_print = data_quants[key].name

        if quiet != True:
            print(index, ":", names_to_print)
            
        index += 1

        return_names.append(names_to_print)
    return return_names