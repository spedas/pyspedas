# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pytplot


def get_ylimits(name, trg=None):
    """
    This function will get extract the y-limits from the Tplot Variables stored in memory.  
    
    Parameters:
        name : str 
            Name of the tplot variable
        trg : list, optional
            The time range that you would like to look in
         
    Returns:
        ymin : float
            The minimum value of y
        ymax : float
            The maximum value of y
            
    Examples:
        >>> # Retrieve the y-limits from Variable 1
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> y1, y2 = pytplot.get_ylimits("Variable1")

    """
    if isinstance(name, int):
        name = list(pytplot.data_quants.keys())[name-1]
    if not isinstance(name, list):
        name = [name]
    name_num = len(name)
    ymin = None
    ymax = None

    for i in range(name_num):

        if name[i] not in pytplot.data_quants.keys():
            print(str(name[i]) + " is currently not in pytplot.")
            return
        y = pytplot.data_quants[name[i]]

        # Slice the data around a time range
        if trg is not None:
            y = y.sel(time=slice(trg[0], trg[1]))

        ymin = y.min(skipna=True)
        ymax = y.max(skipna=False)

    return ymin, ymax
