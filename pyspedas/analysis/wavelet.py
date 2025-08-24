"""
Apply a wavelet transformation to every component of a tplot variable.

Notes
-----
Similar to wav_data.pro in IDL SPEDAS.
For pywavelets library, see:
    https://pywavelets.readthedocs.io/en/latest/ref/cwt.html
For an example, see:
    http://spedas.org/wiki/index.php?title=Wavelet

"""
import logging
import numpy as np
import pywt
import pyspedas
from pyspedas.tplot_tools import options, store_data

def idl_wavelet_scales(n, dt, w0=2*np.pi, dj=None):
    """
    Reproduce the IDL/T&C logic for generating wavelet scales and frequencies.

    Parameters
    ----------
    n : int
        Number of samples in the time series.
    dt : float
        Sampling interval (in seconds).
    w0 : float
        Central frequency (default 2*pi for Morlet).
    dj : float or None
        Scale resolution step. Default: (1/8)*(2*pi/w0)

    Returns
    -------
    scales : ndarray
        Array of wavelet scales.
    freqs : ndarray
        Array of corresponding Fourier frequencies (Hz).
    periods : ndarray
        Fourier periods corresponding to each scale.
    """
    if dj is None:
        dj = (1/8) * (2*np.pi / w0)

    # Period range: [Nyquist period, 5% of total duration]
    nyquist_period = 2 * dt
    max_period = 0.05 * n * dt
    prange = [nyquist_period, max_period]

    # Scale range from period
    fourier_factor = (w0 + np.sqrt(2 + w0**2)) / (4 * np.pi)
    srange = np.array(prange) * fourier_factor

    # Number of scales
    j = int(np.floor(np.log2(srange[1] / srange[0]) / dj))
    if j <= 0:
        raise ValueError("Too few data points for wavelet analysis")

    # Log-spaced scales
    scales = srange[0] * 2**(np.arange(j + 1) * dj)

    # Periods and frequencies
    periods = scales / fourier_factor
    freqs = 1.0 / periods

    return scales, freqs, periods


def wavelet(
    names,
    newname=None,
    suffix='_pow',
    wavename='morl',
    scales=None,
    method='fft',
    sampling_period=1.0):
    """
    Find the wavelet transformation of a tplot variable.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    newname: str/list of str, optional
        List of new names for tplot variables.
        Default: If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply.
        Default: '_pow'.
    wavename: str, optional
        The name of the continuous wavelet function to apply.
        Examples: 'gaus1', 'morl', 'cmorlB-C'.
        Default: 'morl'
    scales: list of float, optional
        The wavelet scales to use.
        Default: None
    method: str, optional
        Either ‘fft’ for  frequency domain convolution,
        or 'conv' for numpy.convolve.
        Default: 'fft'
    sampling_period: float, optional
        The sampling period for the frequencies output.
        Default: 1.0

    Returns
    -------
    A list of tplot variables that contain the wavelet power.

    Example
    -------
        >>> import numpy as np
        >>> import pyspedas
        >>> from pyspedas import time_float
        >>> from pyspedas.analysis.wavelet import wavelet
        >>> # Create a tplot variable that contains a wave.
        >>> t = np.arange(4000.)
        >>> y = np.sin(2*np.pi*t/32.)
        >>> y2 = np.sin(2*np.pi*t/64.)
        >>> y[1000:3000] = y2[1000:3000]
        >>> var = 'sin_wav'
        >>> time = time_float('2010-01-01') + 10*t
        >>> pyspedas.store_data(var, data={'x':time, 'y':y})
        >>> # Gaussian Derivative wavelets transformation.
        >>> powervar = wavelet(var, wavename='gaus1')
        >>> pvar = powervar[0]
        >>> # Define plotting parameters and plot.
        >>> pyspedas.options(pvar, 'colormap', 'jet')
        >>> pyspedas.ylim(pvar, 0.001, 0.1)
        >>> pyspedas.options(pvar, 'ylog', True)
        >>> pyspedas.options(pvar, 'ytitle', pvar)
        >>> pyspedas.tplot([var, pvar])
    """

    varnames = pyspedas.split_vec(names)
    powervar = []

    if len(varnames) < 1:
        logging.error('wavelet error: No pytplot names were provided.')
        return

    for i, old in enumerate(varnames):
        old = varnames[i]

        if (newname is not None) and (len(newname) == len(varnames)):
            new = newname[i]
        else:
            new = old + suffix

        alldata = pyspedas.get_data(old)
        time = alldata[0]
        len_time = len(time)
        data = alldata[1]

        if len_time < 2:
            logging.error('wavelet error: Not enought data points for ' + old)
            continue

        if scales is None:
            n = len_time
            # This is just the first sample difference.  We should probably check that the dt values
            # are consistent throughout, and if not, interpolate onto a regular grid

            dt = time[1] - time[0]

            scales, idl_freqs, idl_periods = idl_wavelet_scales(n, dt)
            sampling_period = 1.0


        coef, freqs = pywt.cwt(data, scales=scales, wavelet=wavename,
                               method=method, sampling_period=sampling_period)

        power = np.abs(coef)**2
        power = power.transpose()
        store_data(new, data={'x': time, 'y': power, 'v': freqs})
        options(new, 'spec', 1)
        powervar.append(new)

        logging.info('wavelet was applied to: ' + new)

    return powervar
