"""
Removes NaNs and other flags.

Notes
----
Allowed wildcards are ? for a single character, * from multiple characters.
Similar to tdeflag.pro in IDL SPEDAS.

"""
import pyspedas
import pytplot
import numpy


def tdeflag(names, method=None, flag=None, new_names=None, suffix=None,
            overwrite=None):
    """
    Remove flag from data.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    method: str, optional
        Method to apply. Default is 'remove_nan.
        Other options 'repeat' (repeat last good value).
    flag: float, optional
        Value to be replaced. Default is NaN.
    new_names: str/list of str, optional
        List of new_names for pytplot variables.
        If '', then pytplot variables are replaced.
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
        print('tdeflag error: No pytplot names were provided.')
        return

    if suffix is None:
        suffix = '-deflag'

    if flag is None:
        flag = float('nan')

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
