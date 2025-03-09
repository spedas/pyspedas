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


def deriv_data(names, newname=None, new_names=None, suffix=None, overwrite=None, edge_order=1):
    """
    Compute the derivative.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    newname: str/list of str, optional
        List of new names for tplot variables.
        If not given, then a suffix is applied.
    new_names: str/list of str, optional (Deprecated)
        List of new names for tplot variables.
        If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply. Default is '-avg'.
    overwrite: bool, optional
        Replace the existing tplot name.
    edge_order: int, optional
        A value passed to np.gradient that specifies how boundaries are treated

    Returns
    -------
    None.

    """

    # new_tvar is deprecated in favor of newname
    if new_names is not None:
        logging.info("deriv_data: The new_names parameter is deprecated. Please use newname instead.")
        newname = new_names

    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        logging.error('deriv_data: No valid tplot names were provided.')
        return

    if suffix is None:
        suffix = '-der'

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

    for i, old in enumerate(old_names):
        data = pytplot.get_data(old)
        data_grad = np.gradient(data.y, data.times, axis = 0, edge_order=edge_order)
        pytplot.store_data(n_names[i], data={'x': data.times, 'y': data_grad})
        logging.info('deriv_data was applied to: ' + n_names[i])

    return n_names