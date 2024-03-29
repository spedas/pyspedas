import logging
import numpy as np
from pytplot import get_data, time_string


def tplot_average(tvar, trange, quiet=False):
    """
    Returns the average value of a tplot variable over a specified time range.

    Input
    -----
        tvar: str
            Name of the tplot variable to average

        trange: list of str or list of float
            Time range to average over

    Returns
    -------
        Average value of the tplot variable
    """
    data = get_data(tvar, dt=True)

    if data is None:
        logging.error('Error reading: ' + tvar)
        return

    if len(trange) != 2:
        logging.error('Error: time range must be two element array.')
        return

    trange = time_string(trange)

    t0 = np.datetime64(trange[0])
    t1 = np.datetime64(trange[-1])

    if not quiet:
        logging.info('Averaging ' + tvar)

    # find the data within the time range
    indices = np.argwhere((data.times <= t1) & (data.times >= t0))

    if len(indices) != 0:
        if len(data.y.shape) > 1:
            return np.array([np.nanmean(data.y[indices, 0]), np.nanmean(data.y[indices, 1]), np.nanmean(data.y[indices, 2])])
        else:
            return np.nanmean(data.y[indices])
