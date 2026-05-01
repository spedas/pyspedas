"""
This is a python version of the wavelet.pro script in IDL SPEDAS.
It computes the wavelet transform as described by Torrence & Compo (1998).

This function is a wrapper for wavelet98.py with some changes:
    - It can handle 1D or 2D data (while wavelet98.py can only handle 1D).
    - It uses the Morlet wavelet only (while wavelet98.py can also use Paul or DOG wavelets).
    - The default Morlet parameter is w0=2pi (while the wavelet98.py default is 6.0).
    - The default dj is dj=1/8 * (2pi/w0) (which is 1/8., the same as in wavelet98.py when w0=2pi).
    - Computes the scales.
    - Uses the normalization factor np.sqrt(2 * dt).
"""

import numpy as np
from pyspedas.analysis.wavelet98 import wavelet98


def wavelet2(
    y,
    dt,
    prange=None,
    frange=None,
    pad=False,
    period=None,
    dj=None,
    param=None,
):
    """
    Wrapper for the Torrence & Compo wavelet98.py function.
    Uses Morlet mother wavelet.

    Parameters
    ----------
    y : ndarray
        Input data, 1D or 2D (n x d2)
    dt : float
        Time step
    prange : list or tuple, optional
        Period range [min, max]
    frange : list or tuple, optional
        Frequency range [min, max] (overrides prange if set)
    pad : bool, optional
        If True, pad the time series for FFT
    period : array, optional
        Output: periods used (filled by wavelet)
    dj : float, optional
        Scale spacing
    param : float, optional
        Morlet parameter (w0)

    Returns
    -------
    wave : ndarray
        Wavelet transform (n, jv+1, d2)
        (n = number of time points, jv = number of scales, d2 = 1 or 2)
    period : ndarray
        Periods corresponding to each scale (jv+1)
    """
    y = np.asarray(y)
    if y.ndim == 1:
        y = y[:, np.newaxis]
    n, d2 = y.shape

    # Set default Morlet parameter if not provided
    if param is None:
        w0 = 2.0 * np.pi
    else:
        w0 = param

    # Set default dj if not provided
    if dj is None:
        dj = 1.0 / 8.0 * (2.0 * np.pi / w0)

    # If frange is set, override prange
    if frange is not None:
        prange = [min(1.0 / np.array(frange)), max(1.0 / np.array(frange))]
    # Default prange: [nyquist period, 5% of total interval]
    if prange is None:
        prange = [2.0 * dt, 0.05 * n * dt]
    if prange[0] == 0:
        prange[0] = 2.0 * dt

    # Compute srange (scales) from prange and Morlet factor
    morlet_factor = (w0 + np.sqrt(2 + w0**2)) / (4 * np.pi)
    srange = np.array(prange) * morlet_factor

    # Number of scales (jv)
    jv = int(np.floor(np.log(srange[1] / srange[0]) / np.log(2) / dj))
    if jv <= 0:
        return -1, None

    # Output arrays
    wave = np.zeros((n, jv + 1, d2), dtype=complex)
    period_arr = None

    # Loop over each column (component)
    for d in range(d2):
        # Call the main wavelet function for each component
        wv98 = wavelet98(
            y[:, d], dt, s0=srange[0], dj=dj, j_scales=jv, pad=pad, param=w0
        )
        wv = wv98[0]
        period = wv98[2]
        wave[:, :, d] = wv
        # IDL multiplies by sqrt(2*dt) for normalization
        wave[:, :, d] *= np.sqrt(2 * dt)
        if period_arr is None:
            period_arr = period

    # Remove singleton dimensions
    if wave.ndim > 0 and wave.shape[-1] == 1:
        wave = wave.squeeze(axis=-1)

    return wave, period_arr
