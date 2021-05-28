"""
Creates a new tplot variable that has spikes removed.

Notes
-----
Similar to clean_spikes.pro in IDL SPEDAS.

"""
import numpy as np
import pyspedas
import pytplot
from pyspedas.analysis.subtract_average import subtract_average
from pyspedas.analysis.tsmooth import tsmooth


def clean_spikes(names, nsmooth=10, thresh=0.3, sub_avg=False,
                 new_names=None, suffix=None, overwrite=None):
    """
    Clean spikes from data.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    new_names: str/list of str, optional
        List of new_names for pytplot variables.
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
    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        print('clean_spikes error: No pytplot names were provided.')
        return

    if suffix is None:
        suffix = '-despike'

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

    for old_idx, old in enumerate(old_names):
        new = n_names[old_idx]
        tmp = new + '_tmp_data'

        # Create new
        if old != new:
            pyspedas.tcopy(old, new)

        # Perform subtract_average or just copy the values
        if sub_avg:
            subtract_average(new, new_names=tmp)
        else:
            pyspedas.tcopy(new, tmp)

        # Find spikes
        tmps = tmp + '-s'
        tsmooth(tmp, new_names=tmps, width=nsmooth)
        ds0 = pytplot.get_data(tmps)  # smoothed out values
        ds = ds0[1]
        dor0 = pytplot.get_data(tmp)  # original values
        d0 = dor0[1]
        dn = d0.copy()  # final values

        dim = dn.shape
        if len(dim) == 1:
            # One dim data.
            for i in range(dim[0]):
                # compare smoothed out values to original values
                if abs(d0[i] - ds[i]) > thresh * abs(ds[i]):
                    dn[i] = np.NaN  # for spikes, set to NaN
        else:
            # More than one dim data.
            for j in range(dim[1]):
                # print("j = ", j)
                for i in range(dim[0]):
                    # compare smoothed out values to original values
                    if abs(d0[i, j] - ds[i, j]) > thresh * abs(ds[i, j]):
                        dn[i, j] = np.NaN  # for spikes, set to NaN

        # pytplot.data_quants[new] = d
        pytplot.replace_data(new, dn)

        # remove temp data
        del pytplot.data_quants[tmp]
        del pytplot.data_quants[tmps]

        print('clean_spikes was applied to: ' + new)
