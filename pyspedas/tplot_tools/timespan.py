import pyspedas
from pyspedas.tplot_tools import time_double
from pyspedas.tplot_tools import xlim
import logging
import numpy as np


def timespan(t1=None, dt=None, units="days", keyword=None, reset=False):
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
    units : str, optional
        Sets the units of the "dt" variable. Days, hours, minutes, and seconds and reasonable abbreviations are all accepted. Default is 'days'.
    keyword : str, optional
        Synonym for units keyword
    reset: bool, optional
        If True, clears all previously set time ranges.

    Returns
    -------
    None

    Examples
    --------
    >>> # Set the timespan to be 2017-07-17 00:00:00 plus 1 day
    >>> import pyspedas
    >>> pyspedas.timespan(1500249600, 1)

    >>> # The same as above, but using different inputs
    >>> pyspedas.timespan("2017-07-17 00:00:00", 24, units='hours')
    """

    if reset is True:
        if 'x_range_full' in pyspedas.tplot_tools.tplot_opt_glob.keys():
            del pyspedas.tplot_tools.tplot_opt_glob['x_range_full']
        if 'x_range_last' in pyspedas.tplot_tools.tplot_opt_glob.keys():
            del pyspedas.tplot_tools.tplot_opt_glob['x_range_last']
        if 'x_range' in pyspedas.tplot_tools.tplot_opt_glob.keys():
            del pyspedas.tplot_tools.tplot_opt_glob['x_range']
        if 'xfull' in pyspedas.tplot_tools.lim_info.keys():
            del pyspedas.tplot_tools.lim_info['xfull']
        if 'xlast' in pyspedas.tplot_tools.lim_info.keys():
            del pyspedas.tplot_tools.lim_info['xlast']
        return
    elif isinstance(t1, (list, tuple, np.ndarray)):
        if len(t1) != 2:
            logging.warning('timespan: If input is a list or array, it must have 2 elements')
            return None
        else:
            t1 = pyspedas.tplot_tools.time_double(t1)
            xlim(t1[0], t1[1])
            return
    elif isinstance(t1, str):
        t1 = pyspedas.tplot_tools.time_double(t1)

    if keyword is not None:
        units = keyword

    if dt is None or not isinstance(dt, (int, float)):
        logging.warning('timespan: Invalid value for dt: ', dt)
    if units.lower() in ["days", 'day', 'd']:
        dt *= 86400
    elif units.lower() in ["hours", 'hour', 'hr', 'hrs', 'h']:
        dt *= 3600
    elif units.lower() in ["minutes", 'minute', 'min', 'mins', 'm']:
        dt *= 60
    elif units.lower() in ["seconds", 'second', 'sec', 'secs', 's']:
        dt *= 1
    else:
        logging.warning(
            "Invalid 'units' option %s.\nEnum(None, 'days', 'day', 'd', 'hours', 'hour', 'hr', 'hrs', 'h', 'minutes', 'minute', 'min', 'mins', 'm', 'seconds', 'second', 'secs', 'sec', 's')",
            keyword,
        )

    if not isinstance(t1, (int, float, complex)):
        t1 = pyspedas.tplot_tools.time_double(t1)
    t2 = t1 + dt
    xlim(t1, t2)

    return
