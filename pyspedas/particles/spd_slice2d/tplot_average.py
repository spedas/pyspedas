import numpy as np
from pytplot import get_data
from pyspedas import time_double


def tplot_average(tvar, trange):
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
    data = get_data(tvar)

    if data is None:
        print('Error reading: ' + tvar)
        return

    if len(trange) != 2:
        print('Error: time range must be two element array.')
        return

    trange = time_double(trange)

    t0 = np.min(trange)
    t1 = np.max(trange)

    print('Averaging ' + tvar)

    # find the data within the time range
    indices = np.argwhere((data.times <= t1) & (data.times >= t0))

    if len(indices) != 0:
        return np.nanmean(data.y[indices])
