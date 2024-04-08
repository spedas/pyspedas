"""
Transform datetimes from decimal to string.
"""
from datetime import datetime, timezone
from .time_double import time_float

def time_string_one(float_time=None, fmt=None):
    """
    Transforms a single float daytime value into a string representation.

    Parameters
    ----------
    float_time : float, optional
        The input time as a float. If not provided, the current time is used.
    fmt : str, optional
        The format string for time conversion. The default format is '%Y-%m-%d %H:%M:%S.%f'.

    Returns
    -------
    str
        The datetime as a string formatted according to `fmt`. If `float_time` is not provided,
        returns the current datetime formatted as specified.

    Examples
    --------
    >>> from pytplot import time_string_one
    >>> time_string_one(1679745600.0)
    '2023-03-25 12:00:00.000000'

    >>> time_string_one(1679745600.0, '%Y-%m-%d')
    '2023-03-25'

    >>> time_string_one()
    # Returns the current datetime in the default format
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
    Transforms a list of float daytime values into a list of string representations.

    Parameters
    ----------
    float_time : floats, or list of floats, optional
        The input time(s) as float(s). If not provided, the current time is used.
    fmt : str, optional
        The format string for time conversion. The default format is '%Y-%m-%d %H:%M:%S.%f'.

    Returns
    -------
    str or list of str
        The datetimes as strings formatted according to `fmt`. If `float_time` is not provided, returns
        the current datetime formatted as specified. If `float_time` is a single float, returns
        a single datetime string.

    Examples
    --------
    >>> time_string(1679745600.0)
    '2023-03-25 12:00:00.000000'

    >>> time_string([1679745600.0, 1679832000.0], "%Y-%m-%d %H:%M:%S")
    ['2023-03-25 12:00:00', '2023-03-26 12:00:00']

    >>> time_string()
    #'Returns the current datetime in the default format'

    Notes
    -----
    Compare to https://www.epochconverter.com/
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


def time_datetime(time=None, tz=None):
    """
    Transforms a list of float daytime values or strings to a list of pythonic `datetime.datetime` objects.

    Parameters
    ----------
    time : float, list of floats, str, or list of strs, optional
        The input time(s) as float(s) representing UNIX timestamps or strings.
        If not provided, the current time is used.
    tz : datetime.timezone, optional
        The timezone for the datetime object(s).
        If not provided, UTC is used.

    Returns
    -------
    datetime.datetime or list of datetime.datetime
        The datetimes as `datetime.datetime` objects. If `time` is a single value, returns a single `datetime.datetime` object;
        if `time` is a list, returns a list of `datetime.datetime` objects. If `time` is None, returns the current datetime in UTC.

    Examples
    --------
    >>> from pytplot import time_datetime
    >>> from datetime import timezone, timedelta
    >>> time_datetime(1679745600.0)
    # or
    >>> time_datetime('2023-03-25 12:00:00')
    # Returns a datetime object for 2023-03-25 12:00:00 UTC
    datetime.datetime(2023, 3, 25, 12, 0, tzinfo=datetime.timezone.utc)

    >>> time_datetime([1679745600.0, 1679832000.0])
    # or
    >>> time_datetime(['2023-03-25 12:00:00', '2023-03-26 12:00:00'])
    # Returns a list of datetime objects for 2023-03-25 12:00:00 UTC and 2023-03-26 12:00:00 UTC
    [datetime.datetime(2023, 3, 25, 12, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2023, 3, 26, 12, 0, tzinfo=datetime.timezone.utc)]

    >>> time_datetime()
    # Returns the current datetime object in UTC

    >>> time_datetime(1679745600.0, tz=timezone(timedelta(hours=-6)))
    # Returns a datetime object for 2023-03-25 06:00:00 in a timezone that is -6 hour from UTC
    datetime.datetime(2023, 3, 25, 6, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=64800)))

    """

    if tz is None:
        tz = timezone.utc

    if time is None:
        return datetime.now()

    if isinstance(time, str):
        return time_datetime(time_float(time))

    if isinstance(time, (int, float)):
        return datetime.fromtimestamp(time, tz=tz)

    return [time_datetime(_time) for _time in time]
