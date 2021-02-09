# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pickle
import pytplot

def tplot_save(names, filename=None):
    """
    This function will save tplot variables into a single file by using the python "pickle" function.
    This file can then be "restored" using tplot_restore.  This is useful if you want to end the pytplot session,
    but save all of your data/options.  All variables and plot options can be read back into tplot with the 
    "tplot_restore" command.  
    
    Parameters:
        names : str/list
            A string or a list of strings of the tplot variables you would like saved.  
        filename : str, optional
            The filename where you want to save the file.  
            
    Returns:
        None
    
    Examples:
        >>> # Save a single tplot variable
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> pytplot.ylim('Variable1', 2, 4)
        >>> pytplot.save('Variable1', filename='C:/temp/variable1.pytplot')

    """
    if isinstance(names,int):
        names = list(pytplot.data_quants.keys())[names-1]
    if not isinstance(names, list):
        names = [names]
    
    #Check that we have all available data
    for name in names:
        if not isinstance(pytplot.data_quants[name], dict): # not a NRV variable
            # variable is a time series
            for oplot_name in pytplot.data_quants[name].attrs['plot_options']['overplots']:
                if oplot_name not in names:
                    names.append(oplot_name)
    
    #Pickle it up
    to_pickle =[]
    for name in names:    
        if name not in pytplot.data_quants.keys():
            print("That name is currently not in pytplot") 
            return
        to_pickle.append(pytplot.data_quants[name])
    
    num_quants = len(to_pickle)
    to_pickle = [num_quants] + to_pickle
    temp_tplot_opt_glob = pytplot.tplot_opt_glob
    to_pickle.append(temp_tplot_opt_glob)
    
    if filename==None:
        filename='var_'+'-'.join(names)+'.pytplot'
    
    out_file = open(filename, "wb")
    pickle.dump(to_pickle, out_file)
    out_file.close()
    
    return