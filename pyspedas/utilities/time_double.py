"""
Transform datetimes from string to decimal.

Examples
--------
time_float()
time_float(['2017-06-29 23:59:59.1234', '2017-12-01 00:15:21.1234'])
time_double()

Notes
-----
Similar to time_double.pro in IDL SPEDAS.

"""

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
        Input string.
        The default is None, which returns Now.

    Returns
    -------
    float
        Output time.

    """
    if s_time is None:
        s_time = str(datetime.now())

    if isinstance(s_time, (int, float, np.integer, np.float)):
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
    str_time : str/list of str, optional
        Input times. The default is None.

    Returns
    -------
    list of float
        Output times as floats.

    """
    if str_time is None:
        return time_float_one()
    else:
        if isinstance(str_time, str):
            return time_float_one(str_time)
        else:
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

    Same as time_float.

    Parameters
    ----------
    str_time : str/list of str, optional
        Input times. The default is None.

    Returns
    -------
    list of float
        Output times as floats.

    """
    return time_float(str_time)
