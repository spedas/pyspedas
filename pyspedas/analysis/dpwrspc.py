"""
This function has now been deprecated. Please use pytplot.tplot_math.dpwrspc instead.

"""
import logging
from pytplot import dpwrspc as pytplot_dpwrspc

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

    logging.warning(
        "This function has now been deprecated. Please use pytplot.tplot_math.dpwrspc instead."
    )

    return pytplot_dpwrspc(
        time,
        quantity,
        nboxpoints=nboxpoints,
        nshiftpoints=nshiftpoints,
        bin=bin,
        tbegin=tbegin,
        tend=tend,
        noline=noline,
        nohanning=nohanning,
        notperhz=notperhz,
        notmvariance=notmvariance,
        tm_sensitivity=tm_sensitivity,
    )
