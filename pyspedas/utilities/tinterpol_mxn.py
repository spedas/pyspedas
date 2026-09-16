"""IDL SPEDAS compatibility entry point for time interpolation."""

from .time_interpolate import time_interpolate


def tinterpol_mxn(source, target, *, method='linear', newname=None,
                 suffix=None, overwrite=False, return_data=False,
                 no_extrapolate=False, nan_extrapolate=False,
                 repeat_extrapolate=False, ignore_nans=False):
    """Interpolate a time series using the IDL SPEDAS-compatible routine name.

    All arguments, defaults and return values are identical to
    :func:`pyspedas.time_interpolate`. See that function for the full parameter
    documentation and examples. This wrapper retains the familiar IDL name;
    new Python code can use ``time_interpolate`` directly.

    See Also
    --------
    pyspedas.time_interpolate
    """
    return time_interpolate(
        source, target, method=method, newname=newname, suffix=suffix,
        overwrite=overwrite, return_data=return_data,
        no_extrapolate=no_extrapolate, nan_extrapolate=nan_extrapolate,
        repeat_extrapolate=repeat_extrapolate, ignore_nans=ignore_nans,
    )
