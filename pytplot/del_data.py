# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pytplot
import fnmatch

def del_data(name=None):
    """
    This function will delete tplot variables that are already stored in memory.  
    
    Parameters:
        name : str 
            Name of the tplot variable to be deleted.  If no name is provided, then 
            all tplot variables will be deleted.  
         
    Returns:
        None
        
    Examples:
        >>> # Delete Variable 1
        >>> import pytplot
        >>> pytplot.del_data("Variable1")

    """
    if name is None:
        tplot_names = list(pytplot.data_quants.keys())
        for i in tplot_names:
            del pytplot.data_quants[i]
        return
    
    if not isinstance(name, list):
        name = [name]
    
    entries = []
    for i in name:
        if ('?' in i) or ('*' in i):
            for j in pytplot.data_quants.keys():
                if isinstance(pytplot.data_quants[j], dict):
                    # NRV variable
                    var_verif = fnmatch.fnmatch(pytplot.data_quants[j]['name'], i)
                    if var_verif == 1:
                        entries.append(pytplot.data_quants[j]['name'])
                    else:
                        continue
                else:
                    var_verif = fnmatch.fnmatch(pytplot.data_quants[j].name, i)
                    if var_verif == 1:
                        entries.append(pytplot.data_quants[j].name)
                    else:
                        continue
            for key in entries:
                if key in pytplot.data_quants:
                    del pytplot.data_quants[key]
        elif i not in pytplot.data_quants.keys():
            print(str(i) + " is currently not in pytplot.")
            return
        
        else:
            if isinstance(pytplot.data_quants[i], dict):
                temp_data_quants = pytplot.data_quants[i]
                str_name = temp_data_quants['name']
            else:
                temp_data_quants = pytplot.data_quants[i]
                str_name = temp_data_quants.name
            
            del pytplot.data_quants[str_name]
        
    return