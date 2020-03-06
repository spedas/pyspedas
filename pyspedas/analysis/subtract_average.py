# -*- coding: utf-8 -*-
"""
File:
    subtract_average.py

Description:
    Subtracts the average (mean) or the median from the data.

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
    median:
        If it is 0 or not set, then it computes the mean.
        Otherwise, it computes the median.

Notes:
    Allowed wildcards are ? for a single character, * from multiple characters.
"""

import pyspedas
import pytplot
import numpy


def subtract_average(names, new_names=None, suffix=None, overwrite=None,
                     median=None):

    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        print('Subtract Average error: No pytplot names were provided.')
        return

    if suffix is None:
        if median:
            suffix = '-m'
        else:
            suffix = '-d'

    if overwrite is not None:
        n_names = old_names
    elif new_names is None:
        n_names = [s + suffix for s in old_names]
    else:
        n_names = new_names

    if isinstance(n_names, str):
        n_names = [n_names]

    if len(n_names) != len(old_names):
        n_names = [s + suffix for s in old_names]

    old_names = pyspedas.tnames(names)

    for i, old in enumerate(old_names):
        new = n_names[i]

        if new != old:
            pyspedas.tcopy(old, new)

        data = pytplot.data_quants[new].values
        if median:
            data_new = data - numpy.median(data, axis=0)
            ptype = 'Median'
        else:
            data_new = data - numpy.mean(data, axis=0)
            ptype = 'Mean'

        pytplot.data_quants[new].values = data_new

        print('Subtract ' + ptype + ' was applied to: ' + new)
