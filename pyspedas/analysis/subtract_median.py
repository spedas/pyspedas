# -*- coding: utf-8 -*-
"""
File:
    subtract_median.py

Description:
    Subtracts the median from the data.

Parameters:
    names: str/list of str
        List of pytplot names.
    new_names: str/list of str
        List of new_names for pytplot variables.
        If not given, then a suffix is applied.
    suffix:
        A suffix to apply. Default is '-d'.
    overwrite:
        If set, then pytplot variables are replaced.

Notes:
    Allowed wildcards are ? for a single character, * from multiple characters.
"""

from .subtract_average import subtract_average


def subtract_median(names, new_names=None, suffix=None, overwrite=None):

    subtract_average(names, new_names=None, suffix=None, overwrite=None,
                     median=1)
    return 1
