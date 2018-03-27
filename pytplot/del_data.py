# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from pytplot import data_quants
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
        >>> pytplot.del_data("Varaible1")

    """
    if name is None:
        tplot_names = list(data_quants.keys())
        for i in tplot_names:
            del data_quants[i]
        return
    
    if not isinstance(name, list):
        name = [name]
    
    entries = []  
    ###    
    for i in name:
        if ('?' in i) or ('*' in i):
            for j in data_quants.keys():
                var_verif = fnmatch.fnmatch(data_quants[j].name, i)
                if var_verif == 1:
                    entries.append(data_quants[j].name)
                else:
                    continue
            for key in entries:
                if key in data_quants:
                    del data_quants[key]       
    ###            
        elif i not in data_quants.keys():
            print(str(i) + " is currently not in pytplot.")
            return
        
        else:
            temp_data_quants = data_quants[i]
            str_name = temp_data_quants.name
            
            del data_quants[str_name]
        
    return