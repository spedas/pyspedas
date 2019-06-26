# -*- coding: utf-8 -*-
"""
File:
    tinterpol.py

Desrciption:
    Interpolates data.

Parameters:
    names: str/list of str
        List of pytplot names.
    interp_names: str/list of str
        List of pytplot names. This should contain the new times array.
    method: str
        Interpolation method. Default is ‘linear’.
        Specifies the kind of interpolation as a string (‘linear’, ‘nearest’,
        ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘previous’, ‘next’)
        where ‘zero’, ‘slinear’, ‘quadratic’ and ‘cubic’ refer to a spline
        interpolation of zeroth, first, second or third order; ‘previous’ and
        ‘next’ simply return the previous or next value of the point) or
        as an integer specifying the order of the spline interpolator to use.
    new_names: str/list of str
        List of new_names for pytplot variables.
        If '', then pytplot variables are replaced.
        If not given, then a suffix is applied.
    suffix:
        A suffix to apply. Default is '-itrp'.

Notes:
    Allowed wildcards are ? for a single character, * from multiple characters.
    Similar to tinterpol in IDL SPEDAS.
"""

import pyspedas
import pytplot
import numpy
from scipy.interpolate import interp1d


def tinterpol(names, interp_names=None, method=None, new_names=None,
              suffix=None):

    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        print('tinterpol error: No pytplot names were provided.')
        return

    if suffix is None:
        suffix = '-itrp'

    if method is None:
        method = 'linear'

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
        alldata1 = pytplot.get_data(interp_names[i])        
        new_time = alldata1[0]
        new_data = alldata1[1]
        data = numpy.asarray(data).squeeze()
        f2 = interp1d(time, data, kind=method)
        new_data = f2(new_time)
        pytplot.store_data(n_names[i], data={'x': new_time, 'y': new_data})
        print('tinterpol (' + method + ') was applied to: ' + n_names[i])
