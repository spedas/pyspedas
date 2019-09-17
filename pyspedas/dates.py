# -*- coding: utf-8 -*-
"""
File:
    dates.py

Description:
    Date functions.
"""

import datetime
import dateutil.parser


def validate_date(date_text):
    # Checks if date_text is an acceptable format
    try:
        return dateutil.parser.parse(date_text)
    except ValueError:
        raise ValueError("Incorrect data format, should be yyyy-mm-dd: '"
                         + date_text + "'")


def get_date_list(date_start, date_end):
    """Returns a list of dates between start and end dates"""
    d1 = datetime.date(int(date_start[0:4]), int(date_start[5:7]),
                       int(date_start[8:10]))
    d2 = datetime.date(int(date_end[0:4]), int(date_end[5:7]),
                       int(date_end[8:10]))

    delta = d2 - d1
    ans_list = []

    for i in range(delta.days + 1):
        ans_list.append(str(d1 + datetime.timedelta(days=i)))

    return ans_list


def get_dates(dates):
    """Returns a list of dates
       date format: yyyy-mm-dd
       input can be a single date or a list of two (start and end date)
    """
    ans_list = []
    if not isinstance(dates, (list, tuple)):
        dates = [dates]

    if len(dates) == 1:
        try:
            validate_date(dates[0])
            ans_list = dates
        except ValueError as e:
            print(e)
            ans_list = []
    elif len(dates) == 2:
        try:
            validate_date(dates[0])
            validate_date(dates[1])
            ans_list = get_date_list(dates[0], dates[1])
        except ValueError as e:
            print(e)
            ans_list = []

    return ans_list
