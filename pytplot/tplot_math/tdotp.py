import logging
from pytplot import get_data, store_data


def tdotp(variable1, variable2, newname=None):
    """
    Routine to calculate the dot product of two tplot variables
    containing arrays of vectors and storing the results in a
    tplot variable

    Parameters
    -----------
    variable1: str
        First tplot variable
    variable2: str
        Second tplot variable
    newname: str
        Name of the output variable
        Default: None. If newname is not specified a new tplot variable will be created
            with the name variable1_dot_variable2
            
    Returns
    --------
        Name of the tplot variable

    Examples
    --------

        >>> # Compute the dot products of a given time series
        >>> import pytplot
        >>> x1 = [0, 4, 8]
        >>> x2 = [0, 4, 8]
        >>> time1 = [pytplot.time_float("2020-01-01") + i for i in x1]
        >>> time2 = [pytplot.time_float("2020-01-01") + i for i in x2]
        >>> pytplot.store_data("a", data={"x": time1, "y": [[1, 2, 3],[2, 3, 4],[3, 4, 5]]})
        >>> pytplot.store_data("c", data={"x": time2, "y": [[1, 4, 1],[2, 5, 2],[3, 5, 3]]})
        >>> n = pytplot.tdotp("a", "c", newname="a_dot_c")
        >>> print('new tplot variable:', n)
        >>> ac = pytplot.get_data(n)
        >>> print(ac)

    """

    data1 = get_data(variable1, xarray=True)
    data2 = get_data(variable2, xarray=True)

    if data1 is None:
        logging.error('Variable not found: ' + variable1)
        return

    if data2 is None:
        logging.error('Variable not found: ' + variable2)
        return

    if newname is None:
        newname = variable1 + '_dot_' + variable2

    # calculate the dot product
    # Note: "dims" is deprecated in favor of "dim", but we'll keep this version for a few more xarray minor releases
    out = data1.dot(data2, dims='v_dim')

    # save the output
    saved = store_data(newname, data={'x': data1.time.values, 'y': out.values})

    if saved is not None:
        return newname
