# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import logging
import pytplot
import numpy as np

def tres(tplot_var):
    """
    Returns the time resolution of a tplot variable, defined as the median value 
    of the differences between time values from the data points, e.g., median(d.x[1:*]-d.x). 
    Can be used for multiple variables.

    Parameters
    ----------
    - tplot_var (int or str or list): A tplot variable name or number, or a list of such names.

    Returns
    -------
    - delta_t (float or list): The time resolution, a median value. If the data variable 
        does not exist, or does not return a median, then the result is -1. If multiple 
        tplot variables are provided, returns a list of median values.

    Examples
    --------
    >>> import pyspedas
    >>> import pyspedas
    >>> import pytplot
    >>> fgm_vars = pyspedas.themis.fgm(probe='d', trange=['2013-11-5', '2013-11-6'])
    >>> dt = pytplot.tres('thd_fgs_gse')
    >>> dts = pytplot.tres(fgm_vars)

    """
    if isinstance(tplot_var, int):
        tplot_var = list(pytplot.data_quants.keys())[tplot_var]

    if isinstance(tplot_var, str):
        data = pytplot.get_data(tplot_var)
        if data is not None:
            delta_t = np.median(data.times[1:-1]-data.times[0:-2])
        else:
            delta_t = -1

        return delta_t
    
    elif isinstance(tplot_var, list):
        delta_t = []
        for name in tplot_var:
            delta_t.append(tres(name))

        return delta_t
    
    else:
        logging.info("tres input must be a int, str or list!")
        return