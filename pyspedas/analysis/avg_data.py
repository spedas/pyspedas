
"""
File:
    avg_data.py

Description:
    Creates a new tplot variable that is the time average of original.

Parameters:
    names: str/list of str
        List of pytplot names.
    new_names: str/list of str
        List of new_names for pytplot variables.
        If not given, then a suffix is applied.
    suffix: str
        A suffix to apply. Default is '-avg'.
    overwrite: bool
        Replace the existing tplot name.
    width: int
        Number of values for the averaging window.
        Default is 60 points (usually seconds).

Notes:
    Similar to avg_data.pro in IDL SPEDAS.
"""

import numpy as np
import pyspedas
import pytplot
from pytplot import store_data


def avg_data(names, width=60, median=None,
             new_names=None, suffix=None, overwrite=None):

    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        print('avg_data error: No pytplot names were provided.')
        return

    if suffix is None:
        suffix = '-avg'

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

    for i, old in enumerate(old_names):
        new = n_names[i]
        tmp = new + '_tmp_avg_data'

        # make sure that the end time is included
        time = pytplot.data_quants[old].time.values
        nt = time[::width]
        np.append(nt, time[-1] + 1.0)

        # group values
        g = pytplot.data_quants[old].groupby_bins('time', nt).mean()
        # new times are midpoints
        nts = nt[:len(g.values)] + (width/2)
        store_data(tmp, data={'x': nts, 'y': g.values})
        # copy attributes
        pytplot.data_quants[tmp].attrs = pytplot.data_quants[old].attrs.copy()
        pytplot.data_quants[tmp].name = tmp
        pytplot.data_quants[new] = pytplot.data_quants[tmp].copy()
        pytplot.data_quants[new].name = new
        # remove temp data
        del pytplot.data_quants[tmp]

        print('avg_data was applied to: ' + new)
