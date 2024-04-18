"""
Compute power spectra for data.

Notes
-----
Similar to dpwrspc.pro in IDL SPEDAS.

"""

import logging
import numpy as np


def dpwrspc(
    time,
    quantity,
    nboxpoints=256,
    nshiftpoints=128,
    bin=3,
    tbegin=-1.0,
    tend=-1.0,
    noline=False,
    nohanning=False,
    notperhz=False,
    notmvariance=False,
    tm_sensitivity=None,
):
    """
    Compute power spectra.

    Parameters
    ----------
    time: list of float
        Time array.
    quantity: list of float
        Data array.
    nboxpoints: int, optional
        The number of points to use for the hanning window.
        The default is 256.
    nshiftpoints: int, optional
        The number of points to shift for each spectrum.
        The default is 128.
    bin: int, optional
        Size for binning of the data along the frequency domain.
        The default is 3.
    tbegin: float, optional
        Start time for the calculation.
        If -1.0, the start time is the first time in the time array.
    tend: float, optional
        End time for the calculation.
        If -1.0, the end time is the last time in the time array.
    noline: bool, optional
        If True, no straight line is subtracted.
        The default is False.
    nohanning: bool, optional
        If True, no hanning window is applied to the input.
        The default is False.
    notperhz: bool, optional
        If True, the output units are the square of the input units.
        The default is False.
    notmvariance: bool, optional
        If True, replace output spectrum for any windows that have variable
        cadence with NaNs.
        The default is False.
    tm_sensitivity: float, optional
        If noTmVariance is set, this number controls how much of a dt anomaly
        is accepted.
        The default is None.

    Returns
    -------
    tdps: array of float
        The time array for the dynamic power spectrum, the center time of the
        interval used for the spectrum.
    fdps: array of float
        The frequency array (units =1/time units).
    dps: array of float
        The power spectrum, (units of quantity)^2/frequency_units.

    Example:
        >>> # Compute the power spectrum of a given time series
        >>> import numpy as np
        >>> from pytplot import tplot_math
        >>> time = range(3000)
        >>> quantity = np.random.random(3000)
        >>> power = pytplot.tplot_math.dpwrspc(time, quantity)
    """
    tdps, fdps, dps = np.array(-1.0), np.array(-1.0), np.array(-1.0)
    tdps0, fdps0, dps0 = np.array(-1.0), np.array(-1.0), np.array(-1.0)

    if nohanning is False:
        window = np.array(np.hanning(nboxpoints), dtype=np.float64)
    else:
        window = np.ones(nboxpoints)

    time = np.array(time, dtype=np.float64)
    quantity = np.array(quantity, dtype=np.float64)

    if tbegin == -1.0:
        tbegin = time[0]
    if tend == -1.0:
        tend = time[-1]

    # Find the time array that correspond to the start and end times
    tbegin_idx = np.where(time >= tbegin)[0][0]
    tend_idx = np.where(time <= tend)[0][-1]
    if tend_idx - tbegin_idx < nboxpoints:
        logging.error("Not enough points for a calculation")
        return tdps0, fdps0, dps0
    time = time[tbegin_idx : tend_idx + 1]
    quantity = quantity[tbegin_idx : tend_idx + 1]

    # remove NaNs from the data
    where_finite = np.where(np.isnan(quantity) == False)
    quantity2process = quantity[where_finite[0]]
    times2process = time[where_finite[0]]
    nboxpnts = int(nboxpoints)
    nshiftpnts = nshiftpoints

    totalpoints = len(times2process)
    nspectra = int((totalpoints - nboxpnts / 2.0) / nshiftpnts)

    # test nspectra, if the value of nshiftpnts is much smaller than
    # nboxpnts/2 strange things happen

    nbegin = np.array([nshiftpnts * i for i in range(nspectra)], dtype=np.int64)
    nend = nbegin + nboxpnts

    okspec = np.where(nend <= totalpoints - 1)

    if len(okspec[0]) <= 0:
        logging.error("Not enough points for a calculation")
        return tdps0, fdps0, dps0
    else:
        nspectra = len(okspec[0])

    tdps = np.zeros(nspectra)
    nfreqs = int(int(nboxpnts / 2) / bin)

    if nfreqs <= 1:
        logging.error("Not enough frequencies for a calculation")
        return tdps0, fdps0, dps0

    dps = np.zeros([nspectra, nfreqs])
    fdps = np.zeros([nspectra, nfreqs])

    # Main calculation loop
    for nthspectrum in range(0, nspectra):
        nbegin = int(nthspectrum * nshiftpnts)
        nend = nbegin + nboxpnts

        if nend <= totalpoints:
            t = times2process[nbegin:nend]
            t0 = t[0]
            t = t - t0
            x = quantity2process[nbegin:nend]

            # Use center time
            tdps[nthspectrum] = (times2process[nbegin] + times2process[nend - 1]) / 2.0

            if noline is False:
                coef = np.polyfit(t, x, 1)
                poly1d_fn = np.poly1d(coef)
                line = poly1d_fn(t)
                x = x - line

            if nohanning is False:
                x = x * window

            bign = nboxpnts

            if bign % 2 != 0:
                logging.warning(
                    "dpwrspc: needs an even number of data points, dropping last point..."
                )
                t = t[0 : bign - 1]
                x = x[0 : bign - 1]
                bign = bign - 1

            n_tm = len(t)

            # time variance can break power spectrum
            # this keyword skips over those gaps
            if notmvariance and n_tm > 1:
                if tm_sensitivity is not None:
                    tmsn = tm_sensitivity
                else:
                    tmsn = 100.0

                tdiff = t[1:n_tm] - t[0 : n_tm - 1]
                med_diff = np.median(tdiff)

                idx = np.where(np.abs(tdiff / med_diff - 1) > 1.0 / tmsn)

                if len(idx[0]) > 0:
                    dps[nthspectrum, :] = float("nan")
                    fdps[nthspectrum, :] = float("nan")

                    continue

            # following Numerical recipes in Fortran, p. 421, sort of...
            # (actually following the IDL implementation)
            k = np.array(range(int(bign / 2) + 1))
            tres = np.median(t[1 : len(t)] - t[0 : len(t) - 1])
            fk = k / (bign * tres)

            xs2 = np.abs(np.fft.fft(x)) ** 2

            pwr = np.zeros(int(bign / 2 + 1))
            pwr[0] = xs2[0] / bign**2
            ptmp = 1 + np.array(range(int(bign / 2 - 1)))
            pwr[1 : int(bign / 2)] = (
                xs2[1 : int(bign / 2)] + xs2[bign - ptmp]
            ) / bign**2
            pwr[int(bign / 2)] = xs2[int(bign / 2)] / bign**2

            if nohanning is False:
                wss = float(bign) * float(np.sum(window**2))
                pwr = bign**2 * pwr / wss

            dfreq = bin * (fk[1] - fk[0])

            npwr = len(pwr) - 1
            nfinal = int(npwr / bin)
            iarray = np.array(range(nfinal))
            power = np.zeros(nfinal)

            # Note: zeroth point includes zero freq. power.
            freqcenter = (fk[iarray * bin + 1] + fk[iarray * bin + bin]) / 2.0

            for i in range(bin):
                power = power + pwr[iarray * bin + i + 1]

            if notperhz is False:
                power = power / dfreq

            dps[nthspectrum, :] = power
            fdps[nthspectrum, :] = freqcenter

    return tdps, fdps, dps
