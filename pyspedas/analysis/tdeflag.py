
"""
File:
    tdeflag.py

Description:
    Removes NaNs and other flags.

Parameters:
    names: str/list of str
        List of pytplot names.
    method: str
        Method to apply. Default is 'remove_nan.
        Other options 'repeat' (repeat last good value).
    flag: float
        Value to be replaced. Default is NaN.
    new_names: str/list of str
        List of new_names for pytplot variables.
        If '', then pytplot variables are replaced.
        If not given, then a suffix is applied.
    suffix:
        A suffix to apply. Default is '-clip'.

Notes:
    Allowed wildcards are ? for a single character, * from multiple characters.
    Similar to tdeflag in IDL SPEDAS.
"""

import pyspedas
import pytplot
import numpy


def tdeflag(names, method=None, flag=None, new_names=None, suffix=None):

    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        print('tdeflag error: No pytplot names were provided.')
        return

    if suffix == None:
        suffix = '-deflag'

    if flag == None:
        flag = float('nan')

    if new_names == None:
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
        new_time = []
        new_data = []
        for j in range(len(time)):
            if not numpy.isnan(data[j]):
                new_time.append(time[j])
                new_data.append(data[j])
        pytplot.store_data(n_names[i], data={'x': new_time, 'y': new_data})
        print('tdeflag was applied to: ' + n_names[i])
