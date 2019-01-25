# -*- coding: utf-8 -*-
"""
File:
    subtract_median.py

Desrciption:
    Time clip of data.

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


def time_clip(names, time_start, time_end, new_names=None, suffix=None):

    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        print('Subtract Median error: No pytplot names were provided.')
        return

    if suffix is None:
        suffix = '-tclip'

    if new_names is None:
        n_names = [s + suffix for s in old_names]
    elif new_names == '':
        n_names = old_names
    else:
        n_names = new_names

    if len(n_names) != len(old_names):
        n_names = [s + suffix for s in old_names]

    for j in range(len(old_names)):
        if old_names[j] != n_names[j]:
            pyspedas.tcopy(old_names[j], n_names[j])

        time, data = pytplot.get_data(n_names[j])
        index_start = 0
        index_end = len(time)

        if index_end < 1:
            print('Time clip found empty list.')
            continue

        new_time = pyspedas.time_float(time)
        new_time_start = pyspedas.time_float(time_start)
        new_time_end = pyspedas.time_float(time_end)

        if new_time_start > new_time_end:
            print('Error: Start time is larger than end time.')
            continue

        if (new_time_start > new_time[-1]) or (new_time_end < new_time[0]):
            print('Time clip returns empty data.')
            continue

        if (new_time_start <= new_time[0]) and (new_time_end >= new_time[-1]):
            print('Time clip returns full data set.')
            continue

        for i in range(index_end):
            if new_time[i] >= new_time_start:
                index_start = i
                break
        found_end = index_end
        for i in range(index_start, index_end):
            if new_time[i] > new_time_end:
                found_end = i
                break
        index_end = found_end

        pytplot.store_data(n_names[j], data={'x': time[index_start:index_end],
                           'y': data[index_start:index_end, :]})
        print('Time clip was applied to: ' + n_names[j])
