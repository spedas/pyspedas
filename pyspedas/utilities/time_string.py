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
from datetime import datetime


def time_string_one(float_time=None, fmt=None):
    """
    Transform a single float daytime value to string.

    Parameters
    ----------
    float_time : float, optional
        Input time.
        The default is None, which returns the time now.
    fmt : float, optional
        Time format.
        The default is None, which uses '%Y-%m-%d %H:%M:%S.%f'.

    Returns
    -------
    str
        Datetime as string.

    """
    if fmt is None:
        fmt = '%Y-%m-%d %H:%M:%S.%f'

    if float_time is None:
        str_time = datetime.now().strftime(fmt)
    else:
        str_time = datetime.utcfromtimestamp(float_time).strftime(fmt)

    return str_time


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
    if float_time is None:
        return time_string_one(None, fmt)
    else:
        if isinstance(float_time, (int, float)):
            return time_string_one(float_time, fmt)
        else:
            time_list = list()
            for t in float_time:
                time_list.append(time_string_one(t, fmt))
            return time_list
