import numpy as np
from pytplot import get_data
from pyspedas import time_double


def tplot_average(tvar, trange):
    """

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
