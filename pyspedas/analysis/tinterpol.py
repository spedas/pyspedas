import datetime
import logging
from pytplot import get_data, store, tnames
import numpy as np


def tinterpol(names, interp_to, method=None, newname=None, extrapolate=False, suffix=None):
    """
    Interpolate data to times in interp_to.

    Parameters
    ----------
    names : array_like or str
        List of tplot variables to interpolate.
        Allowed wildcards are ? for a single character, * from multiple characters.
    interp_to : array_like or str
        String containing the tplot variable with the time stamps to interpolate to.
    method : str, optional
        Interpolation method. Default is 'linear'.
        Specifies the kind of interpolation as a string ('linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic', 'previous', 'next')
        where 'zero', 'slinear', 'quadratic' and 'cubic' refer to a spline interpolation of zeroth, first, second or third order;
        'previous' and 'next' simply return the previous or next value of the point) or as an integer specifying the order of the spline interpolator to use.
    newname : str or list of str, optional
        List of new names for tplot variables. If '', then tplot variables are replaced. If not given, then a suffix is applied.
    extrapolate: bool
        If true, extrapolate beyond the start/end times of the interp_to variable.  Default is False (for now)
    suffix : str, optional
        A suffix to apply. Default is '-itrp'.

    Returns
    -------
    None
        This function works in-place or creates new tplot variables depending on the 'newname' parameter.


    Notes
    -----

    Uses xarray interp method to interpolate data to the times in interp_to.
    See: https://docs.xarray.dev/en/latest/generated/xarray.DataArray.interp.html
    Similar to tinterpol.pro in IDL SPEDAS.

    'linear' vs. 'slinear' methods:  Due to a quirk in the implmentation of the scipy interp1d routine (used
    internally by xarray.interp),'linear' interpolation may yield unexpected results under certain conditions.
    In particular, when using 32-bit floating point data, if an output time exactly matches one of the input times, the
    interpolated value may differ slightly (on the order of 1 ULP) from the input value at that timestamp.
    This can cause problems for downstream calculations: for example, if the input is strictly non-negative, but
    contains zero values, the interpolated data may contain small negative values. The 'slinear' method does not appear
    to suffer from this issue, but may be slightly slower.


    Examples
    --------
        >>> import numpy as np
        import pyspedas
        >>> import pyspedas

        >>> # Create some time series data
        >>> times = np.array(['2002-02-03T04:05:00', '2002-02-03T04:05:05', '2002-02-03T04:05:10'], dtype='datetime64')
        >>> data = np.array([0.0, 5.0, 10.0])

        >>> # Store the data as a tplot variable
        >>> pyspedas.store_data('variable1', data={'x': times, 'y': data})

        >>> # Create some new times to interpolate to
        >>> new_times = np.array(['2002-02-03T04:05:07', '2002-02-03T04:05:08', '2002-02-03T04:05:09'], dtype='datetime64')
        >>> new_data = np.array([11.0, 12.0, 13.0])

        >>> # Store the new times in a tplot variable, the new_data will be ignored in this example
        >>> pyspedas.store_data('variable2', data={'x': new_times, 'y': new_data})

        >>> # Interpolate 'variable1' to the new times using the default linear method
        >>> pyspedas.tinterpol(names='variable1', interp_to='variable2')

        >>> # The interpolated data is now stored in 'variable1-itrp'
        >>> interpolated_data = pyspedas.get_data('variable1-itrp')
        >>> print(interpolated_data)
    """
    if not isinstance(names, list):
        names = [names]
    if not isinstance(newname, list):
        newname = [newname]

    old_names = tnames(names)  # expand any wildcards

    if len(old_names) < 1:
        logging.error("tinterpol error: No pytplot names were provided.")
        return

    if suffix is None:
        suffix = "-itrp"

    if method is None:
        method = "linear"

    if (newname is None) or (len(newname) == 1 and newname[0] is None):
        n_names = [s + suffix for s in old_names]
    else:
        n_names = newname

    if isinstance(interp_to, str):
        interp_to_data = get_data(interp_to, dt=True)

        if interp_to_data is None:
            logging.error("Error, tplot variable: " + interp_to + " not found.")
            return

        interp_to_times = interp_to_data[0]
    else:
        interp_to_times = interp_to

    kwargs={}
    if extrapolate:
        kwargs={'fill_value':'extrapolate'}


    for name_idx, name in enumerate(old_names):
        xdata = get_data(name, xarray=True)
        metadata = get_data(name, metadata=True)

        if isinstance(interp_to_times[0], (datetime.datetime, np.datetime64)):
            # Timezone-naive datetime or np.datetime64, use as-is
            interp_to_datetimes = interp_to_times
        elif isinstance(interp_to_times[0], (int, float, np.integer, np.float64)):
            # Assume seconds since Unix epoch, convert to np.datetime64 with nanosecond precision
            if isinstance(interp_to_times, np.ndarray):
                interp_to_datetimes = np.array(
                    interp_to_times * 1e09, dtype="datetime64[ns]"
                )
            else:
                # We need to convert input to a numpy array before scaling to nanoseconds
                interp_to_datetimes = np.array(
                    np.array(interp_to_times) * 1e9, dtype="datetime64[ns]"
                )
        elif isinstance(interp_to_times[0], str):
            # Interpret strings as timestamps, convert to np.datetime64 with nanosecond precision
            interp_to_datetimes = np.array(interp_to_times, dtype="datetime64[ns]")
        else:
            # Give up for any other type
            logging.error(
                "tinterpol: Unable to convert type %s to timestamp.",
                type(interp_to_times[0]),
            )
            return

        xdata_interpolated = xdata.interp({"time": interp_to_datetimes}, method=method, kwargs=kwargs)

        if "spec_bins" in xdata.coords:
            store(
                n_names[name_idx],
                data={
                    "x": interp_to_times,
                    "y": xdata_interpolated.values,
                    "v": xdata_interpolated.coords["spec_bins"].values,
                },
                metadata=metadata,
            )
        else:
            store(
                n_names[name_idx],
                data={"x": interp_to_times, "y": xdata_interpolated.values},
                metadata=metadata,
            )

        logging.info("tinterpol (" + method + ") was applied to: " + n_names[name_idx])
