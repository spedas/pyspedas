import logging
import numpy as np
from pytplot import tnames, get_data, pwrspc, store_data, options, time_string


def tpwrspc(varname, newname=None, overwrite=False, noline=False, nohanning=False, bin=3, notperhz=False, trange=None, axis=0):
    """
    This function is a wrapper for pwrspc.
    It applies pwrspc to a pytplot variable and stores the result in a new pytplot variable.

    Parameters:
        varname (str):
            Name of the tplot variable.
        newname (str, optional):
            New name for the output tplot variable.
        overwrite (bool):
            If True, overwrite the existing tplot variable.
            If True, then the newname keyword has no effect.
        noline, nohanning, bin, notperhz (optional):
            Power spectrum computation options.
            Same as in the pwrspc function.
        trange (list, optional):
            Time range for the data extraction.
        axis (int, optional):
            If the input variable is multi-dimensional, this specifies the axis to operate along.
            Default is the first axis.

    Returns:
        newname (string)
            Name of the new tplot variable created by this function.
            The output variable contains a single data point, frequency as v, and power as y.
    """

    # Check if the variable exists
    if tnames(varname) == []:
        logging.info('This tplot variable does not exist.')
        return ''

    # Check for conflicting arguments
    if overwrite:
        logging.info('Variable will be overwritten.')
        newname = varname
    else:
        if newname:
            if tnames(newname) != []:
                logging.info('This new tplot variable already exists. Please use overwrite=True to overwrite it.')
                return ''
        else:
            newname = varname + '_pwrspc'

    # Get data from tplot variable
    d = get_data(varname)
    t = np.array(d[0], dtype='float64')
    data = np.array(d[1], dtype='float64')

    # If the input variable is multi-dimensional, operate along the specified axis
    if data.ndim == 1:
        y = data
    elif data.ndim == 2:
        if axis < 1:
            axis = 0
        elif axis > data.shape[1]:
            axis = data.shape[1] - 1
        logging.info(f'Operating along axis {axis}')
        y = data[:, axis]
    else:
        logging.info('Cannot handle data with more than two dimensions.')
        return ''

    # Remove NaN points
    tav = np.mean(t)  # We are going to store f,p at the time average point
    goodpoints = ~np.isnan(t) & ~np.isnan(y)
    if np.any(goodpoints):
        t = t[goodpoints]
        y = y[goodpoints]
        logging.info('NaN points have been removed.')
    else:
        logging.info(f'No valid data points in {varname}')
        return ''

    # Restrict to a time range if specified
    if trange and len(trange) == 2:
        ok = (trange[0] <= t < trange[1])
        if not np.any(ok):
            logging.info('No data in time range for:', varname)
            logging.info('No Power spectrum for:', varname)
            return ''
        else:
            t = t[ok]
            y = y[ok]

    # Call the power spectrum function (previously defined)
    t = t-t[0]
    f, p = pwrspc(t, y, noline=noline, nohanning=nohanning, bin=bin, notperhz=notperhz)

    if f is not None and p is not None and len(f) > 0 and len(p) > 0 and len(f) == len(p):
        # Store the result in a new tplot variable
        # A single data point will be created, with frequency as v, and power as y
        pp = np.array([p,])
        ff = np.array([f,])
        tt = np.array([tav,], dtype='float64')
        store_data(newname, data={'x': tt, 'y':  pp, 'v':  ff})
        options(newname, 'data_type', 'power_spectrum')
        options(newname, 'spec', 1)
        options(newname, 'ylog', 1)
    else:
        print('No Power spectrum for:', varname)
        return ''

    return newname
