"""
Compute power spectra for data.

Notes
-----
Similar to dpwrspc.pro in IDL SPEDAS.

"""
import numpy as np


def dpwrspc(time, quantity, nboxpoints=256, nshiftpoints=128, binsize=3,
            nohanning=False, noline=False, notperhz=False, notmvariance=False,
            tm_sensitivity=None):
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
    binsize: int, optional
        Size for binning of the data along the frequency domain.
        The default is 3.
    nohanning: bool, optional
        If True, no hanning window is applied to the input.
        The default is False.
    noline: bool, optional
        If True, no straight line is subtracted.
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

    """
    if nohanning is False:
        window = np.hanning(nboxpoints)

    # remove NaNs from the data
    where_finite = np.where(np.isnan(quantity) == False)

    quantity2process = quantity[where_finite[0]]
    times2process = time[where_finite[0]]
    nboxpnts = nboxpoints
    nshiftpnts = nshiftpoints

    totalpoints = len(times2process)
    nspectra = int((totalpoints-nboxpnts/2.)/nshiftpnts)

    # test nspectra, if the value of nshiftpnts is much smaller than
    # nboxpnts/2 strange things happen

    nbegin = np.array([nshiftpnts*i for i in range(nspectra)])
    nend = nbegin + nboxpnts

    okspec = np.where(nend <= totalpoints-1)

    if len(okspec[0]) <= 0:
        print('Not enough points for a calculation')
        return

    tdps = np.zeros(nspectra)
    nfreqs = int(int(nboxpnts/2)/binsize)

    if nfreqs <= 1:
        print('Not enough frequencies for a calculation')
        return

    dps = np.zeros([nspectra, nfreqs])
    fdps = np.zeros([nspectra, nfreqs])

    for nthspectrum in range(0, nspectra):
        nbegin = int(nthspectrum*nshiftpnts)
        nend = nbegin + nboxpnts

        if nend <= totalpoints-1:
            t = times2process[nbegin:nend]
            t0 = t[0]
            t = t - t0
            x = quantity2process[nbegin:nend]

            # Use center time
            tdps[nthspectrum] = (times2process[nbegin]+times2process[nend])/2.0

            if noline is False:
                coef = np.polyfit(t, x, 1)
                poly1d_fn = np.poly1d(coef)
                line = poly1d_fn(t)
                x = x - line

            if nohanning is False:
                x = x*window

            bign = nboxpnts

            if bign % 2 != 0:
                print('dpwrspc: needs an even number of data points,\
                      dropping last point...')
                t = t[0:bign-1]
                x = x[0:bign-1]
                bign = bign - 1

            n_tm = len(t)

            # time variance can break power spectrum
            # this keyword skips over those gaps
            if notmvariance and n_tm > 1:
                if tm_sensitivity is not None:
                    tmsn = tm_sensitivity
                else:
                    tmsn = 100.0

                tdiff = t[1:n_tm]-t[0:n_tm-1]
                med_diff = np.median(tdiff)

                idx = np.where(np.abs(tdiff/med_diff-1) > 1.0/tmsn)

                if len(idx[0]) > 0:
                    dps[nthspectrum, :] = float('nan')
                    fdps[nthspectrum, :] = float('nan')

                    continue

            # following Numerical recipes in Fortran, p. 421, sort of...
            # (actually following the IDL implementation)
            k = np.array(range(int(bign/2)+1))
            tres = np.median(t[1:len(t)] - t[0:len(t)-1])
            fk = k/(bign*tres)

            xs2 = np.abs(np.fft.fft(x))**2

            pwr = np.zeros(int(bign/2+1))
            pwr[0] = xs2[0]/bign**2
            ptmp = (1+np.array(range(int(bign/2-1))))
            pwr[1:int(bign/2)] = (xs2[1:int(bign/2)] + xs2[bign-ptmp])/bign**2
            pwr[int(bign/2)] = xs2[int(bign/2)]/bign**2

            if nohanning is False:
                wss = bign*np.sum(window**2)
                pwr = bign**2*pwr/wss

            dfreq = binsize*(fk[1]-fk[0])

            npwr = len(pwr)-1
            nfinal = int(npwr/binsize)
            iarray = np.array(range(nfinal))
            power = np.zeros(nfinal)

            # Note: zeroth point includes zero freq. power.
            freqcenter = (fk[iarray*binsize+1]+fk[iarray*binsize+binsize])/2.

            for i in range(binsize):
                power = power+pwr[iarray*binsize+i+1]

            if notperhz is False:
                power = power/dfreq

            dps[nthspectrum, :] = power
            fdps[nthspectrum, :] = freqcenter

    return (tdps, fdps, dps)
