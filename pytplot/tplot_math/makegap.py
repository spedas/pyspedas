import pytplot
import numpy as np


def makegap(var_data, dt=None, margin=0.0, func="nan"):
    """
    Fill gaps in the data either with NaNs or the last number.  This
    is identical to degap, except operates directly on the data and
    time arrays, rather than the tplot variable. This is intended for
    use with the data_gap option. This version actually puts the data
    into a temporary tplot variable, and call degap, then extracts
    that data into the proper form.

    Parameters
    ----------
        var_data : named tuple
            The data for the tplot variable, a structure that contains at least, tags for 'y' and 'times'
        dt : int/float
            Step size of the data in seconds, default is to use the median time interval
        margin : int/float, optional, default is 0.0 seconds (there is no margin in the IDL tplot makegap)
            The maximum deviation from the step size allowed before degapping occurs.  In other words,
            if you'd like to fill in data every 4 seconds but occasionally the data is 4.1 seconds apart,
            set the margin to .1 so that a data point is not inserted there.
        func : str, optional
            Either 'nan' or 'ffill', which overrides normal interpolation with NaN
            substitution or forward-filled values.

    Returns
    -------
    tuple
        A tuple returned by calling get_data() on the degapped temp variable

    Examples
    --------

        >>> import pytplot
        >>> time = [pytplot.time_float("2020-01-01") + i for i in [1, 2, 3, 4, 5, 6, 9, 10, 11]]
        >>> y = [1, 2, 3, 4, 5, 6, 9, 10, 11]
        >>> pytplot.store_data("a", data={"x": time, "y": y})
        >>> a = pytplot.get_data("a")
        >>> print(a)
        >>> b = pytplot.makegap(a)
        >>> print(b)

    """
    # vt = var_data.times
    # gap_size = np.diff(vt) #vt is in nanoseconds, and np.diff works over day boundaries
    # Default for dt is the median value of gap_size, the time interval differences
    # if dt == None:
    #    dt = np.median(gap_size)
    #    dt0 = dt
    # else:
    # change dt to appropriate type
    #    dt0 = np.timedelta64(int(dt*1e9), 'ns')

    # gap_index_locations = np.where(gap_size > dt0)

    # First create a temporary tplot variable for the data, times need to be in unix time
    #x = pytplot.time_float(var_data.times)
    x = np.int64(var_data.times)/1e9
    if var_data.y.ndim == 1:
        pytplot.store_data("makegap_tmp", data={"x": x, "y": var_data.y})
    else:  # multiple dimensions
        var_data_out = None
        pytplot.store_data("makegap_tmp", data={"x": x, "y": var_data.y})
        # Check for values, v, or v1, v2, v3
        if len(var_data) == 2:  # No v's
            pytplot.store_data("makegap_tmp", data={"x": x, "y": var_data.y})
        elif len(var_data) == 3:  # v or v1,needs indexing if it's 2d
            pytplot.store_data(
                "makegap_tmp", data={"x": x, "y": var_data.y, "v": var_data[2]}
            )
        elif len(var_data) == 4:  # has both v1 and v2
            pytplot.store_data(
                "makegap_tmp",
                data={"x": x, "y": var_data.y, "v1": var_data[2], "v2": var_data[3]},
            )
        elif len(var_data) == 5:  # has v1, v2, v3
            pytplot.store_data(
                "makegap_tmp",
                data={
                    "x": x,
                    "y": var_data.y,
                    "v1": var_data[2],
                    "v2": var_data[3],
                    "v3": var_data[3],
                },
            )
    # Now, degap the variable
    pytplot.degap("makegap_tmp", dt=dt, margin=margin, func=func)
    # and return the getdata result
    var_data_out = pytplot.get_data("makegap_tmp", dt=True)
    pytplot.del_data("makegap_tmp")
    return var_data_out
