"""
Clip data and replace values with flag.

Notes:
Allowed wildcards are ? for a single character, * from multiple characters.
Similar to tclip.pro in IDL SPEDAS.
This function clips y-axis data. To clip time-axis, use time_clip.

"""

import pyspedas
import pytplot
import numpy as np


def yclip(names, ymin, ymax, flag=None, new_names=None, suffix=None,
          overwrite=None):
    """
    Clip data values.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    ymin: float
        Minimum value to clip.
    ymax: float
        Maximum value to clip.
    flag: float, optional
        Values outside (ymin, ymax) are replaced with flag.
        Default is float('nan').
    new_names: str/list of str, optional
        List of new_names for pytplot variables.
        If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply. Default is '-clip'.
    overwrite: bool, optional
        Replace the existing tplot name.

    Returns
    -------
    None.

    """
    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        print('yclip error: No pytplot names were provided.')
        return

    if suffix is None:
        suffix = '-clip'

    if flag is None:
        flag = np.nan

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

        data = pytplot.clip(old, ymin, ymax, new)

        print('yclip was applied to: ' + new)
