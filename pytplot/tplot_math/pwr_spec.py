import numpy as np
import logging
import pytplot
from scipy import signal


# First pass at the power spectrum function.  This is still missing several features of the IDL power spectrum routine, such as
# bin, nohanning, notperhertz, and tm_sensativity.  The IDL routine is located in dpwrspc.pro.

# There is also the issue of this not quite having the same units as the plot I use as my reference.
# https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2015GL065366#grl53372-bib-0016
# Interestingly enough, the output is the same if units of seconds are used in the periodogram instead of Hertz.
# Perhaps they calculated it differently?


def pwr_spec(tvar, nbp=256, nsp=128, newname=None):
    """
    Calculates the power spectrum of a line, and adds a tplot variable for this new spectrogram

    Parameters:
        tvar : str
            Name of tvar to use
        nbp : int, optional
            The number of points to use when calculating the FFT
        nsp : int, optional
            The number of points to shift over to calculate the next FFT
        newname : str, optional
            The name of the new tplot variable created,

    Returns:
        None

    Examples:
        >>> import pytplot
        >>> import math
        >>> time = [pytplot.time_float("2020-01-01") + i for i in range(10000)]
        >>> quantity = [math.sin(i) for i in range(10000)]
        >>> pytplot.store_data("dp", data={"x": time, "y": quantity})
        >>> pytplot.pwr_spec("dp", name="dp_pwrspec")
        >>> pytplot.tplot("dp_pwrspec")
    """

    d = pytplot.get_data(tvar)
    x, y = d[0], d[1]

    if len(y.shape) > 1:
        logging.warning(
            "Cannot create pwr_spec for variable %s, must be a single line", tvar
        )

    l = len(x)
    x_new = []
    f_new = []
    pxx_new = []
    shift_lsp = np.arange(0, l - 1, nsp)
    for i in shift_lsp:
        x_n = x[i : i + nbp]
        y_n = y[i : i + nbp]
        if len(x_n) < nbp:
            continue

        median_diff_between_points = np.median(np.diff(x_n))
        w = signal.get_window("hamming", nbp)
        f, pxx = signal.periodogram(
            y_n, fs=(1 / median_diff_between_points), window=w, detrend="linear"
        )
        f = f[1:-1]
        pxx = pxx[1:-1]
        x_new.append((x_n[-1] + x_n[0]) / 2)
        f_new.append(f)
        pxx_new.append(pxx)

    if name is None:
        name = tvar + "_pwrspec"

    pytplot.store_data(name, data={"x": x_new, "y": pxx_new, "v": f_new})
    pytplot.options(name, "spec", 1)
    pytplot.options(name, "zlog", 1)
    pytplot.options(name, "ylog", 1)

    return
