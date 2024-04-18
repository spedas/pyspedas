from . import time_double
from .xlim import xlim
import logging


def timespan(t1, dt, keyword="days"):
    """
    This function will set the time range for all time series plots. This is a wrapper for the function "xlim" to
    better handle time axes.

    Parameters
    ----------
    t1 : float or str
        The time to start all time series plots. Can be given in seconds since epoch, or as a string
        in the format "YYYY-MM-DD HH:MM:SS".
    dt : float
        The time duration of the plots. Default is number of days.
    keyword : str, optional
        Sets the units of the "dt" variable. Days, hours, minutes, and seconds are all accepted. Default is 'days'.

    Returns
    -------
    None

    Examples
    --------
    >>> # Set the timespan to be 2017-07-17 00:00:00 plus 1 day
    >>> import pytplot
    >>> pytplot.timespan(1500249600, 1)

    >>> # The same as above, but using different inputs
    >>> pytplot.timespan("2017-07-17 00:00:00", 24, keyword='hours')
    """

    if keyword == "days":
        dt *= 86400
    elif keyword == "hours":
        dt *= 3600
    elif keyword == "minutes":
        dt *= 60
    elif keyword == "seconds":
        dt *= 1
    else:
        logging.warning(
            "Invalid 'keyword' option %s.\nEnum(None, 'hours', 'minutes', 'seconds', 'days')",
            keyword,
        )

    if not isinstance(t1, (int, float, complex)):
        t1 = time_double.time_double(t1)
    t2 = t1 + dt
    xlim(t1, t2)

    return
