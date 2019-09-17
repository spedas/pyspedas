# -*- coding: utf-8 -*-
"""
File:
    time_double.py

Description:
    Transforms datetimes from string to decimal.

Parameters:
    str_time: str/list of str
    If None, then it assumes Now.

Returns:
    float/list of floats
    A UTC decimal time.

Examples:
    time_float()
    time_float(['2018-06-29'])
    time_float(['2017-06-29 23:59:59.1234', '2017-12-01 00:15:21.1234'])
    time_double()

Notes:
    Needs python 3.3+
    Similar to time_double() of IDL SPEDAS
    Test with https://www.epochconverter.com/
"""

from dateutil import parser
from datetime import datetime, timezone


def time_float_one(s_time=None):

    if s_time is None:
        s_time = str(datetime.now())

    if isinstance(s_time, (int, float)):
        return float(s_time)

    in_datetime = parser.parse(s_time)
    float_time = in_datetime.replace(tzinfo=timezone.utc).timestamp()

    return float_time


def time_float(str_time=None):

    if str_time is None:
        return time_float_one()
    else:
        if isinstance(str_time, str):
            return time_float_one(str_time)
        else:
            time_list = list()
            for t in str_time:
                time_list.append(time_float_one(t))
            return time_list


def time_double(str_time=None):
    return time_float(str_time)
