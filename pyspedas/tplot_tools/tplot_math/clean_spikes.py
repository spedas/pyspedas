"""
Creates a new tplot variable that has spikes removed.

Notes
-----
Similar to clean_spikes.pro in IDL SPEDAS.

"""
import logging
import numpy as np
#import pyspedas
from pyspedas.tplot_tools import tsmooth
from pyspedas.tplot_tools import subtract_average
from pyspedas.tplot_tools import tnames, tplot_copy
from pyspedas.tplot_tools import get_data
from pyspedas.tplot_tools import replace_data
from pyspedas.tplot_tools import data_quants

def clean_spikes(names, nsmooth=10, thresh=0.3, sub_avg=False,
                 newname=None, suffix=None, overwrite=None):
    """
    Clean spikes from data.

    Parameters
    ----------
    names: str/list of str
        List of pyspedas names (wildcards accepted)
    newname: str/list of str, optional
        List of new names for tplot variables.
        If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply. Default is '-avg'.
    overwrite: bool, optional
        Replace the existing tplot name.
    nsmooth: int, optional
        the number of data points for smoothing
    thresh: float, optional
        threshold value
    sub_avg: bool, optional
        if set, subtract the average value of the data
        prior to checking for spikes

    Returns
    -------
    None.

    """

    old_names = tnames(names)

    if len(old_names) < 1:
        logging.error('clean_spikes: No valid tplot names were provided.')
        return

    if suffix is None:
        suffix = '-despike'

    if overwrite is not None:
        n_names = old_names
    elif newname is None:
        n_names = [s + suffix for s in old_names]
    else:
        n_names = newname

    if isinstance(n_names, str):
        n_names = [n_names]

    if len(n_names) != len(old_names):
        n_names = [s + suffix for s in old_names]

    for old_idx, old in enumerate(old_names):
        new = n_names[old_idx]
        tmp = new + '_tmp_data'

        # Create new
        if old != new:
            tplot_copy(old, new)

        # Perform subtract_average or just copy the values
        if sub_avg:
            subtract_average(new, newname=tmp)
        else:
            tplot_copy(new, tmp)

        # Find spikes
        tmps = tmp + '-s'
        tsmooth(tmp, newname=tmps, width=nsmooth)
        ds0 = get_data(tmps)  # smoothed out values
        ds = ds0[1]
        dor0 = get_data(tmp)  # original values
        d0 = dor0[1]
        dn = d0.copy()  # final values

        dim = dn.shape
        if len(dim) == 1:
            # One dim data.
            for i in range(dim[0]):
                # compare smoothed out values to original values
                if abs(d0[i] - ds[i]) > thresh * abs(ds[i]):
                    dn[i] = np.nan  # for spikes, set to NaN
        else:
            # More than one dim data.
            for j in range(dim[1]):
                for i in range(dim[0]):
                    # compare smoothed out values to original values
                    if abs(d0[i, j] - ds[i, j]) > thresh * abs(ds[i, j]):
                        dn[i, j] = np.nan  # for spikes, set to NaN

        # pyspedas.tplot_tools.data_quants[new] = d
        replace_data(new, dn)

        # remove temp data
        del data_quants[tmp]
        del data_quants[tmps]

        logging.info('clean_spikes was applied to: ' + new)
