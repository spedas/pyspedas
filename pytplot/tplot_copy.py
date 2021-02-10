# Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pytplot
from copy import deepcopy
from collections import OrderedDict


def tplot_copy(old_name, new_name):
    """
    This function will copy a tplot variables that is already stored in memory.

    Parameters:
        name : str
            Old name of the Tplot Variable
        new_name : str
            Name of the copied Tplot Variable

    Returns:
        None

    Examples:
        >>> # Copy Variable 1 into a new Variable 2
        >>> import pytplot
        >>> pytplot.tplot_copy("Variable1", "Variable2")

    """

    # if old name input is a number, convert to corresponding name
    if isinstance(old_name, int):
        if isinstance(pytplot.data_quants[old_name], dict):
            old_name = pytplot.data_quants[old_name]['name']
        else:
            old_name = pytplot.data_quants[old_name].name

    # check if old name is in current dictionary
    if old_name not in pytplot.data_quants.keys():
        print("That name is currently not in pytplot")
        return

    # Add a new data quantity with the copied data
    if isinstance(pytplot.data_quants[old_name], dict):
        # old variable is a non-record varying variable
        pytplot.store_data(new_name, data={'y': pytplot.data_quants[old_name]['data']})
    else:
        attr_dict = deepcopy(pytplot.data_quants[old_name].attrs)
        data_dict = {}
        data_dict['x'] = pytplot.data_quants[old_name].coords['time'].values
        data_dict['y'] = pytplot.data_quants[old_name].values
        if len(data_dict['y'].shape) <= 2:
            pass
        else:
            for c in pytplot.data_quants[old_name].coords:
                if c == 'time' or c == 'spec_bins':
                    continue
                data_dict[c] = pytplot.data_quants[old_name].coords[c].values
        pytplot.store_data(new_name, data=data_dict)
        pytplot.data_quants[new_name].attrs = attr_dict

    return
