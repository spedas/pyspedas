import pytplot
import numpy as np
import copy
import logging


def degap(
    tvar,
    dt=None,
    margin=0.25,
    func="nan",
    newname=None,
    new_tvar=None,
    onenanpergap=False,
    twonanpergap=False,
):
    """
    Fills gaps in the data either with NaNs or the last number.

    Parameters
    ----------
        tvar : str
            Name of tplot variable to modify
        dt : int/float
            Step size of the data in seconds, default is to use the median time interval
        margin : int/float, optional, default is 0.25 seconds
            The maximum deviation from the step size allowed before degapping occurs.  In other words, if you'd like to fill in data every 4 seconds
            but occasionally the data is 4.1 seconds apart, set the margin to .1 so that a data point is not inserted there.
        func : str, optional
            Either 'nan' or 'ffill', which overrides normal interpolation with NaN
            substitution or forward-filled values.
        newname : str, optional
            The new tplot variable name to store the data into.  If None, then the data is overwritten.
            THIS is not an option for multiple variable input, for multiple or pseudo variables, the data is overwritten.
        new_tvar : str, optional (Deprecated)
            The new tplot variable name to store the data into.  If None, then the data is overwritten.
            THIS is not an option for multiple variable input, for multiple or pseudo variables, the data is overwritten.
        onenanpergap : bool
            if set to True, then only insert one NaN value, rather than adding NaN values at dt resolution
        twonanpergap : bool
            if set to True, then only insert one NaN value, rather than adding NaN values at dt resolution
    Returns
    -------
        None
            Creates a new tplot variable with the degap data

    Examples
    --------

        >>> import pytplot
        >>> time = [pytplot.time_float("2020-01-01") + i for i in [1, 2, 3, 4, 5, 6, 9, 10, 11]]
        >>> y = [1, 2, 3, 4, 5, 6, 9, 10, 11]
        >>> pytplot.store_data("a", data={"x": time, "y": y})
        >>> degap("a", newname="b")
        >>> b = pytplot.get("b")
        >>> print(b)
    """

    # new_tvar is deprecated in favor of newname
    if new_tvar is not None:
        logging.info(
            "degap: The new_tvar parameter is deprecated. Please use newname instead."
        )
        newname = new_tvar

    # check for globbed or array input, and call recursively
    tn = pytplot.tnames(tvar)
    if len(tn) > 1:
        for j in range(len(tn)):
            pytplot.degap(
                tn[j],
                dt=dt,
                margin=margin,
                func=func,
                onenanpergap=onenanpergap,
                twonanpergap=twonanpergap,
            )
        return

    # here we have 1 variable

    # fix from T.Hori, 2023-04-10, jimm02
    #    gap_size = np.diff(pytplot.data_quants[tvar].coords['time']) This is in Nanoseconds, and causes a type mismatch with dt+margin
    #    new_tvar_index = pytplot.data_quants[tvar].coords['time']
    new_tvar_index = pytplot.get_data(tvar)[0]  # Unix time float64
    gap_size = np.diff(new_tvar_index)

    # Default for dt is the median value of gap_size, the time interval differences
    if dt == None:
        dt = np.median(gap_size)

    gap_index_locations = np.where(gap_size > dt + margin)
    values_to_add = np.array([])
    if onenanpergap == True:
        for i in gap_index_locations[0]:
            values_to_add = np.append(values_to_add, new_tvar_index[i] + dt)
    elif twonanpergap == True:
        # add two NaN values between the two values, either at margin if it's nonzero, or at dt/2
        # since the gap is greater than dt, this will work
        if margin > 0.0:
            if margin < dt / 2.0:
                dt_nan = margin
            else:
                dt_nan = dt / 2.0
        else:
            dt_nan = dt / 2.0
        for i in gap_index_locations[0]:
            values_to_add = np.append(values_to_add, new_tvar_index[i] + dt_nan)
            values_to_add = np.append(values_to_add, new_tvar_index[i + 1] - dt_nan)
    else:
        for i in gap_index_locations[0]:
            values_to_add = np.append(
                values_to_add, np.arange(new_tvar_index[i], new_tvar_index[i + 1], dt)
            )

    # new_index = np.sort(np.unique(np.concatenate((values_to_add, new_tvar_index))))
    new_index_float64 = np.sort(
        np.unique(np.concatenate((values_to_add, new_tvar_index)))
    )

    if func == "nan":
        method = None
    if func == "ffill":
        method = "ffill"

    # Replace any NaN or inf time values with 0.0  (Is this needed? It seems like it could result in non-monotonic times)
    cond=np.logical_not(np.isfinite(new_index_float64))
    new_index_float64[cond]=0.0

    # Convert back to datetime64 (nanoseconds since epoch)
    new_index=np.array(new_index_float64*1e9,dtype='datetime64[ns]')

    # This can fail if the stored quantities are np.datetime64 and new_index is something else, like datetime.datetime
    a = pytplot.data_quants[tvar].reindex({"time": new_index}, method=method)

    if newname is None:
        a.name = tvar
        a.attrs = copy.deepcopy(pytplot.data_quants[tvar].attrs)
        pytplot.data_quants[tvar] = copy.deepcopy(a)
    else:
        if "spec_bins" in a.coords:
            pytplot.store_data(
                newname,
                data={"x": a.coords["time"], "y": a.values, "v": a.coords["spec_bins"]},
            )
            pytplot.data_quants[newname].attrs = copy.deepcopy(
                pytplot.data_quants[tvar].attrs
            )
        else:
            pytplot.store_data(newname, data={"x": a.coords["time"], "y": a.values})
            pytplot.data_quants[newname].attrs = copy.deepcopy(
                pytplot.data_quants[tvar].attrs
            )

    return
