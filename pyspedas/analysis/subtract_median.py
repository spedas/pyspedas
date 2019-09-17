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
        If '', then pytplot variables are replaced.
        If not given, then a suffix is applied.
    suffix:
        A suffix to apply. Default is '-m'.

Notes:
    Allowed wildcards are ? for a single character, * from multiple characters.
"""

import pyspedas
import pytplot
import numpy


def subtract_median(names, new_names=None, suffix=None):

    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        print('Subtract Median error: No pytplot names were provided.')
        return

    if suffix is None:
        suffix = '-m'

    if new_names is None:
        n_names = [s + suffix for s in old_names]
    elif new_names == '':
        n_names = old_names
    else:
        n_names = new_names

    if len(n_names) != len(old_names):
        n_names = [s + suffix for s in old_names]

    for i in range(len(old_names)):
        alldata = pytplot.get_data(old_names[i])
        time = alldata[0]
        data = alldata[1]
        new_data = data-numpy.median(data, axis=0)
        pytplot.store_data(n_names[i], data={'x': time, 'y': new_data})
        print('Subtract Median was applied to: ' + n_names[i])
