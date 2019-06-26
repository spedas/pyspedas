# -*- coding: utf-8 -*-
"""
File:
    tclip.py

Desrciption:
    Clip data and replace values with flag.

Parameters:
    names: str/list of str
        List of pytplot names.
    ymin:
        Minimum value to clip
    ymax:
        Maximum value to clip
    flag:
        Values outside (ymin, ymax) are replaced with flag.
        Default is float('nan').
    new_names: str/list of str
        List of new_names for pytplot variables.
        If '', then pytplot variables are replaced.
        If not given, then a suffix is applied.
    suffix:
        A suffix to apply. Default is '-clip'.

Notes:
    Allowed wildcards are ? for a single character, * from multiple characters.
    Similar to tclip in IDL SPEDAS.
    This function clips y-axis data. To clip time-axis, use time_clip.
"""

import pyspedas
import pytplot
import numpy


def tclip(names, ymin, ymax, flag=None, new_names=None, suffix=None):

    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        print('tclip error: No pytplot names were provided.')
        return

    if suffix is None:
        suffix = '-clip'

    if flag is None:
        flag = float('nan')

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
        new_data = numpy.array(data)
        new_data[new_data <= ymin] = flag
        new_data[new_data >= ymax] = flag
        pytplot.store_data(n_names[i], data={'x': time, 'y': new_data})
        print('tclip was applied to: ' + n_names[i])
