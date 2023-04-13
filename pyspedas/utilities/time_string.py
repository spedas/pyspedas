"""
Transform datetimes from decimal to string.

Examples
--------
time_string()
time_string([1498780799.1234, 1512087321.1234])

Notes
-----
Compare to https://www.epochconverter.com/

"""
import logging
import pytplot

def time_string(float_time=None, fmt=None):
    """
    Transform a list of float daytime values to a list of strings.

    Parameters
    ----------
    float_time: float/list of floats, optional
        Input time.
        The default is None, which returns the time now.
    fmt: str, optional
        Time format.
        The default is None, which uses '%Y-%m-%d %H:%M:%S.%f'.

    Returns
    -------
    list of str
        Datetimes as string.

    """
    logging.info("time_string has been moved to the pytplot package. Please update your imports!")
    logging.info("This version will eventually be removed.")
    return pytplot.time_string(float_time=float_time,fmt=fmt)

def time_datetime(time=None, tz=None):
    """Find python datetime.

    Transform a list of float daytime values to a list of pythonic
        'datetime.datetime' values.

    Parameters
    ----------
    time: float/list of floats or str/list of str, optional
        Input time.
        The default is None, which returns the time now.

    Returns
    -------
    list of datetime.datetime
        Datetimes as `datetime.datetime`.

    """
    logging.info("time_datetime has been moved to the pytplot package. Please update your imports!")
    logging.info("This version will eventually be removed.")
    return pytplot.time_datetime(time=time,tz=tz)
