"""
Creates a new tplot variable which is the derivative of the data.

Notes
-----
Similar to deriv_data.pro in IDL SPEDAS.

"""
import logging

import numpy as np

import pyspedas
import pytplot


def deriv_data(names, new_names=None, suffix=None, overwrite=None):
    """
    Compute the derivative.

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


    Returns
    -------
    None.

    """
    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        logging.error('deriv_data error: No pytplot names were provided.')
        return

    if suffix is None:
        suffix = '-der'

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
        data = pytplot.get_data(old, dt=True)
        pytplot.store_data(n_names[i], data={'x': data.times, 'y': np.gradient(data.y)})
        logging.info('deriv_data was applied to: ' + n_names[i])
