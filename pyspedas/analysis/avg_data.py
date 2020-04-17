"""
    Creates a new pytplot variable as the time average of original.

Parameters
----------
    names: str/list of str
        List of pytplot names.
    width: int
        Number of values for the averaging window.
        Default is 60 points (usually this means 60 seconds).
    noremainder: boolean
        If True, the remainter (last part of data) will not be included.
    new_names: str/list of str
        List of new_names for pytplot variables.
        If not given, then a suffix is applied.
    suffix: str
        A suffix to apply. Default is '-avg'.
    overwrite: bool
        Replace the existing tplot name.

Notes
-----
    Similar to avg_data.pro in IDL SPEDAS.
"""

import numpy as np
import pyspedas
import pytplot
from pytplot import store_data


def avg_data(names, width=60, noremainder=True,
             new_names=None, suffix=None, overwrite=None):
    """Get a new tplot variable with averaged data."""
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

        d = pytplot.data_quants[old].copy()
        data = d.values
        time = d.time.values

        dim = data.shape
        dim0 = dim[0]
        if len(dim) < 2:
            dim1 = 1
        else:
            dim1 = dim[1]

        new_data = []
        new_time = []
        for i in range(0, dim0, width):
            last = (i + width) if (i + width) < dim0 else dim0
            idx = int(i + width/2)
            if idx > dim0-1:
                if noremainder:  # Skip the last part of data
                    continue
                idx = dim0 - 1  # Include the last part of data
            new_time.append(time[idx])
            if dim1 < 2:
                nd0 = np.average(data[i:last])
            else:
                nd0 = []
                for j in range(dim1):
                    nd0.append(np.average(data[i:last, j]))
            new_data.append(nd0)

        store_data(new, data={'x': new_time, 'y': new_data})
        # copy attributes
        pytplot.data_quants[new].attrs = d.attrs.copy()

        print('avg_data was applied to: ' + new)
