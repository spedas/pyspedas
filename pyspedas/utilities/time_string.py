# -*- coding: utf-8 -*-
"""
File:
    time_string.py

Desrciption:
    Transforms datetimes from decimal to string.

Parameters:
    float_time: float/list of floats
    If None, then uses Now.

Returns:
    str/list of str
    A time string ('YYYY-MM-DD HH:MM:SS.NNN') .

Examples:
    time_string()
    time_string(None, '%Y-%m-%d')
    time_string([1498780799.1234, 1512087321.1234])

Notes:
    Test with https://www.epochconverter.com/
"""

from datetime import datetime


def time_string_one(float_time=None, fmt=None):

    if fmt is None:
        fmt = '%Y-%m-%d %H:%M:%S.%f'

    if float_time is None:
        str_time = datetime.now().strftime(fmt)
    else:
        str_time = datetime.utcfromtimestamp(float_time).strftime(fmt)

    return str_time


def time_string(float_time=None, fmt=None):

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
