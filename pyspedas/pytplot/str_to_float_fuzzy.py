# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import datetime
from dateutil.parser import parse

def str_to_float_fuzzy(time_str):
    """
    Implementation of str_to_int (below) that uses dateutil and .timestamp()
    to convert the date/time string to integer (number of seconds since Jan 1, 1970)

    This function is slower than str_to_int, but more flexible
    """
    dt_object = parse(time_str)
    return dt_object.replace(tzinfo=datetime.timezone.utc).timestamp()
