# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from pytplot import data_quants


def get_ylimits(name, trg = None):
    """
    This function will get extract the y limites from the Tplot Variables stored in memory.  
    
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
        >>> # Retrieve the y limits from Variable 1
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> y1, y2 = pytplot.get_ylimits("Variable1")

    """
    if isinstance(name,int):
        name = list(data_quants.keys())[name-1]
    if not isinstance(name, list):
        name = [name]
    if not isinstance(name, list):
        name = [name]
    name_num = len(name)
    ymin = None
    ymax = None
    for i in range(name_num):
        if name[i] not in data_quants.keys():
            print(str(name[i]) + " is currently not in pytplot.")
            return
        temp_data_quant = data_quants[name[i]]
        yother = temp_data_quant.data
        if trg is not None:
            for column_name in yother.columns:
                y = yother[column_name]
                trunc_tempt_data_quant = y.truncate(before = trg[0], after = trg[1])
                loc_min = trunc_tempt_data_quant.min(skipna=True)
                loc_max = trunc_tempt_data_quant.max(skipna=True)
                if (ymin is None) or (loc_min < ymin):
                    ymin = loc_min
                if (ymax is None) or (loc_max > ymax):
                    ymax = loc_max
        else:
            for column_name in yother.columns:
                y = yother[column_name]
                loc_min = y.min(skipna=True)
                loc_max = y.max(skipna=False)
                if (ymin is None) or (loc_min < ymin):
                    ymin = loc_min
                if (ymax is None) or (loc_max > ymax):
                    ymax = loc_max
    print("Y Minimum: " + str(ymin))
    print("Y Maximum: " + str(ymax))
    
    return(ymin, ymax)