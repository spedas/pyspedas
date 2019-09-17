# -*- coding: utf-8 -*-
"""
File:
    tnames.py

Description:
    Finds all pytplot names that follow a pattern that may contain a wildcard.

Returns:
    list of str
    A list of tplot names.

Parameters:
    pattern: str/list of str
        List of strings with names and/or patterns.
        If not given, it returns all pytplot names.

Notes:
    Allowed wildcards are ? for a single character, * from multiple characters.
"""

import fnmatch
import pyspedas


def tnames(pattern=None):

    name_list = list()
    all_names = pyspedas.tplot_names()

    if pattern is None:
        name_list.extend(all_names)
    else:
        if isinstance(pattern, str):
            name_list.extend(fnmatch.filter(all_names, pattern))
        else:
            for p in pattern:
                name_list.extend(fnmatch.filter(all_names, p))

    return name_list
