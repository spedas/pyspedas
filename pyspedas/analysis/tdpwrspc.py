"""
This function has now been deprecated. Please use pytplot.tplot_math.tdpwrspc instead.

"""
import logging
from pytplot import tdpwrspc as pytplot_tdpwrspc


def tdpwrspc(
    varname,
    newname=None,
    trange=["0.0", "0.0"],
    nboxpoints=None,
    nshiftpoints=None,
    polar=False,
    bin=3,
    nohanning=False,
    noline=False,
    notperhz=False,
    notmvariance=False,
):

    """
    Compute power spectra for a tplot variable.

    Parameters
    ----------
    varname: str
        Name of pytplot variable.
    newname: str, optional
        Name of new pytplot variable to save data to.
        Default: None. If newname is not set '_dpwrspc' will be appended to the varname
    trange: list of float, optional
        Start and end times for the calculation.
    nboxpoints: int, optional
        The number of points to use for the hanning window.
        Default: 256
    nshiftpoints: int, optional
        The number of points to shift for each spectrum.
        Default: 128
    polar: bool, optional
        If True, the input data is in polar coordinates.
        Default: False
    bin: int, optional
        Size for binning of the data along the frequency domain.
        Default: 3
    nohanning: bool, optional
        If True, no hanning window is applied to the input.
        Default: False
    noline: bool, optional
        If True, no straight line is subtracted.
        Default: False
    notperhz: bool, optional
        If True, the output units are the square of the input units.
        Default: False
    notmvariance: bool, optional
        If True, replace output spectrum for any windows that have variable.
        cadence with NaNs.
        Default: False

    Returns
    -------
    str
        Name of new pytplot variable.

    Example
    -------
        >>> import pytplot
        >>> import numpy as np
        >>> pytplot.store_data('a', data={'x': range(100), 'y': np.random.random(100)})
        >>> pytplot.get_data('a_pwrspc')
        >>> pytplot.tdpwrspc('a_pwrspc')

    logging.warning(
        "This function has now been deprecated. Please use pytplot.tplot_math.tdpwrspc instead."
    )

    return pytplot_tdpwrspc(
        varname,
        newname=newname,
        trange=trange,
        nboxpoints=nboxpoints,
        nshiftpoints=nshiftpoints,
        polar=polar,
        bin=bin,
        nohanning=nohanning,
        noline=noline,
        notperhz=notperhz,
        notmvariance=notmvariance,
    )
