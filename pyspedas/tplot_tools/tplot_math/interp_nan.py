import pyspedas
import copy
import logging


def interp_nan(tvar, newname=None, s_limit=None):
    """
    Interpolates the tplot variable through NaNs in the data. This is basically just a wrapper for xarray's interpolate_na function.

    .. note::
        This analysis routine assumes the data is no more than 2 dimensions. If there are more, they may become flattened!

    Parameters
    ----------
    tvar : str
        Name of tplot variable.
    newname : str
        Name of new tvar for added data. If not set, then the original tvar is replaced.
    s_limit : int or float, optional
        The maximum size of the gap in seconds to not interpolate over. I.e. if there are too many NaNs in a row, leave them there.

    Returns
    -------
    None

    Examples
    --------
    >>> import pyspedas
    >>> import numpy as np
    >>> pyspedas.store_data('e', data={'x':[2,5,8,11,14,17,21], 'y':[[np.nan,1,1],[np.nan,2,3],[4,np.nan,47],[4,np.nan,5],[5,5,99],[6,6,25],[7,np.nan,-5]]})
    >>> pyspedas.interp_nan('e','e_nonan',s_limit=5)

    """

    x = pyspedas.tplot_tools.data_quants[tvar].interpolate_na(dim="time", limit=s_limit)
    x.attrs = copy.deepcopy(pyspedas.tplot_tools.data_quants[tvar].attrs)

    if newname is None:
        pyspedas.tplot_tools.data_quants[tvar] = x
        x.name = tvar
    else:
        pyspedas.tplot_tools.data_quants[newname] = x
        pyspedas.tplot_tools.data_quants[newname].name = newname
