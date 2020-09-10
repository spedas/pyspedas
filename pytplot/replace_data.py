# Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import pytplot
import numpy as np
from pytplot import tplot_utilities as utilities
from copy import deepcopy
from collections import OrderedDict


def replace_data(tplot_name, new_data):
    """
    This function will replace all of the data in a tplot variable

    Parameters:
        tplot_name : str
            The name of the tplot variable
        new_data : np array (or something that can be converted to a np.array)
            The data to replace the

    Returns:
        None

    Examples:
        >>> # Copy Variable 1 into a new Variable 2
        >>> import pytplot
        >>> pytplot.replace_data("Variable1", [[1,2,3,4],[5,6,7,8]])

    """

    # if old name input is a number, convert to corresponding name
    if isinstance(tplot_name, int):
        tplot_name = pytplot.data_quants[tplot_name].name

    # check if old name is in current dictionary
    if tplot_name not in pytplot.data_quants.keys():
        print(f"{tplot_name} is currently not in pytplot")
        return

    new_data_np = np.asarray(new_data)
    shape_old = pytplot.data_quants[tplot_name].values.shape
    shape_new = new_data_np.shape
    if shape_old != shape_new:
        print(f"Dimensions do not match for replace data. {shape_new} does not equal {shape_old}.  Returning...")
        return

    pytplot.data_quants[tplot_name].values = new_data_np

    pytplot.data_quants[tplot_name].attrs['plot_options']['yaxis_opt']['y_range'] = utilities.get_y_range(pytplot.data_quants[tplot_name])

    return
