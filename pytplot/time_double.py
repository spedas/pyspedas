from dateutil import parser
from datetime import datetime, timezone
import numpy as np
from collections.abc import Iterable


def time_float_one(s_time=None):
    """
    Transform one datetime from string to decimal.

    Parameters
    ----------
    s_time : str, optional
        Input string representing a datetime. If not provided, the current time is used.

    Returns
    -------
    float_time : float
        The decimal representation of the input datetime, or the current local datetime if no input is provided.

    Examples
    --------
    >>> from pytplot import time_float_one
    >>> time_float_one('2023-03-25 12:00:00')
    1679745600.0

    """
    if s_time is None:
        s_time = str(datetime.now())

    if isinstance(s_time, (int, float, np.integer, np.float64)):
        return float(s_time)

    try:
        in_datetime = parser.isoparse(s_time)
    except ValueError:
        in_datetime = parser.parse(s_time)

    float_time = in_datetime.replace(tzinfo=timezone.utc).timestamp()

    return float_time


def time_float(str_time=None):
    """
    Transform a list of datetimes from string to decimal.

    Parameters
    ----------
    str_time : str or list of str, optional
        The input datetime(s) as a string or a list of strings. If not provided the current time is used.

    Returns
    -------
    time_list : list of float or float
        The decimal representation of the input datetime(s) as a list of floats. If the input is a single
        datetime string, the list will contain only one element. The current local datetime is used if no input is provided.

    Examples
    --------
    >>> from pytplot import time_float
    >>> time_float(['2023-03-25 12:00:00', '2023-03-26 12:00:00'])
    [1679745600.0, 1679832000.0]

    >>> time_float('2023-03-25 12:00:00')
    1679745600.0

    >>> time_float()
    # Returns the current timestamp as a list containing one float.

    Note
    ----
    This function is to time_double.pro in IDL SPEDAS.
    """

    if str_time is None:
        return time_float_one()

    if isinstance(str_time, str):
        return time_float_one(str_time)

    time_list = list()
    if isinstance(str_time, Iterable):
        for t in str_time:
            time_list.append(time_float_one(t))
        return time_list
    else:
        return time_float_one(str_time)


def time_double(str_time=None):
    """
    Transform a list of datetimes from string to decimal.

    Parameters
    ----------
    str_time : str or list of str, optional
        The input datetime(s) as a string or a list of strings. If not provided the current time is used.

    Returns
    -------
    time_list : list of float or float
        The decimal representation of the input datetime(s) as a list of floats. If the input is a single
        datetime string, the list will contain only one element. The current local datetime is used if no input is provided.

    Examples
    --------
    >>> from pytplot import time_double
    >>> time_double(['2023-03-25 12:00:00', '2023-03-26 12:00:00'])
    [1679745600.0, 1679832000.0]

    >>> time_double('2023-03-25 12:00:00')
    1679745600.0

    >>> time_double()
    # Returns the current timestamp as a list containing one float.

    Note
    ----
    This function is an alilas of time_float. This function is to time_double.pro in IDL SPEDAS.

    """
    return time_float(str_time)
