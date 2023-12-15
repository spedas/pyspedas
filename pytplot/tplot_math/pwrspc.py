import logging
import numpy as np
from scipy.stats import linregress


def pwrspc(time, quantity, noline=False, nohanning=False, bin=3, notperhz=False):
    """
    Compute the power spectrum of a given time series.

    Parameters:
        time (array):
            The time array.
        quantity (array):
            The data array for which the power spectrum is to be computed.
        noline (bool):
            If True, straight line is not subtracted from the data.
        nohanning (bool):
            If True, no Hanning window is applied to the data.
        bin (int):
            Bin size for binning the data. Default is 3.
        notperhz (bool):
            If True, the output units are the square of the input units.

    Returns:
        tuple: Tuple containing:
            - freq (array):
                The frequency array.
            - power (array):
                The computed power spectrum.

    Notes:
        This is similar to IDL pwrspc.pro routine.

    Example:
        >>> # Compute the power spectrum of a given time series
        >>> from pytplot import pwrspc
        >>> time = [1, 2, 3, 4, 5]
        >>> quantity = [1, 2, 3, 4, 5]
        >>> freq, power = pwrspc(time, quantity)
    """

    t = np.array(time, dtype=np.float64) - time[0]
    x = np.array(quantity, dtype=np.float64)

    if not noline:
        slope, intercept, _, _, _ = linregress(t, x)
        x -= (slope * t + intercept)

    binsize = bin

    window = 0.0
    if not nohanning:
        window = np.hanning(len(x))
        x *= window

    nt = len(t)
    if nt % 2 != 0:
        logging.info('needs an even number of data points, dropping last point...')
        t = t[:-1]
        x = x[:-1]
        nt -= 1

    xs2 = np.abs(np.fft.fft(x)) ** 2
    dbign = float(nt)
    logging.info('bign=', dbign)

    k = np.arange(0, dbign // 2 + 1)
    tres = float(np.median(np.diff(t)))
    fk = k / (dbign * tres)

    pwr = np.zeros(nt // 2 + 1)
    pwr[0] = xs2[0] / dbign**2
    pwr[1:nt // 2] = (xs2[1:nt // 2] + xs2[nt:nt // 2:-1]) / dbign**2
    pwr[-1] = xs2[-1] / dbign**2

    if not nohanning:
        wss = dbign * np.sum(window ** 2)
        pwr = pwr*dbign**2/wss

    dfreq = binsize * (fk[1] - fk[0])
    npwr = len(pwr) - 1
    nfinal = int(npwr / binsize)
    iarray = np.arange(nfinal)
    power = np.zeros(nfinal)

    idx = (iarray + 0.5) * binsize + 1
    freq = [fk[int(i)] for i in idx]

    for i in range(binsize):
        power += pwr[iarray * binsize + i + 1]

    if not notperhz:
        power /= dfreq

    logging.info('dfreq=', dfreq)

    return freq, power
