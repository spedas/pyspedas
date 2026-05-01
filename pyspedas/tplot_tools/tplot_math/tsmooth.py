"""
Smooths a tplot variable.

Uses a boxcar average of the specified width.

Notes
-----
Similar to tsmooth2.pro in IDL SPEDAS.
Also, see: https://www.harrisgeospatial.com/docs/SMOOTH.html

"""
import logging
import math
import numpy as np
import pyspedas
from pyspedas.tplot_tools import tnames, tplot_copy


def smooth(data, width=10, preserve_nans=None):
    """
    Boxcar average.

    Parameters
    ----------
    data : list of floats
        The data should be a one-dim array.
    width : float, optional
        Data window to use for smoothing. The default is 10.
    preserve_nans : bool, optional
        If None, then replace NaNs. The default is None.

    Returns
    -------
    list of float
        Smoothed data.
    
    Example
    -------
        >>> import pyspedas
        >>> import numpy as np
        >>> print(pyspedas.smooth(np.random.random(100)))

    """
    result = data.copy()
    N = len(data)

    if N <= width:
        logging.error("smooth: Not enough points.")
        return result

    for i, d in enumerate(data):
        if (i >= (width-1)/2) and (i <= N-(width+1)/2):
            if (preserve_nans is not None) and data[i] is np.nan:
                continue
            tsum = 0
            count = 0
            for j in range(int(width)):
                idx = math.ceil(i+j-width/2)
                if data[idx] is not np.nan:
                    tsum += data[idx]
                    count += 1
            if count > 0:  # otherwise, all NaN
                result[i] = (1/width) * tsum
    return result


def tsmooth(names, width=10, median=None, preserve_nans=None,
            newname=None, suffix=None, overwrite=None):
    """
    Smooths a tplot variable.

    Parameters
    ----------
    names: str/list of str
        List of tplot variable names to be smoothed (wildcards accepted)
    width: int, optional
        Data window to use for smoothing. The default is 10.
    median: bool, optional
        Apply the median as well. The default is None.
    preserve_nans: bool, optional
        If None, then replace NaNs. The default is None.
    newname: str/list of str, optional
        List of new names for tplot variables.
        If not given, then a suffix is applied. 
        The default is None.
    suffix: str, optional
        A suffix to apply. Default is '-s'.
        The default is None.
    overwrite: bool, optional
        Replace the existing tplot name.
        The default is None.

    Returns
    -------
    list of str
        Returns list of tplot variables created or changed

    Example
    -------
        >>> import pyspedas
        >>> import numpy as np
        >>> pyspedas.store_data('a', data={'x': range(100), 'y': np.random.random(100)})
        >>> pyspedas.tsmooth('a')

    """
    old_names = tnames(names)

    if len(old_names) < 1:
        logging.error('tsmooth: No valid tplot variable names were provided.')
        return

    if suffix is None:
        suffix = '-s'

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
        new = n_names[i]

        if new != old:
            tplot_copy(old, new)

        data = pyspedas.tplot_tools.data_quants[new].values

        dim = data.shape
        if len(dim) == 1:
            data = smooth(data, width=width, preserve_nans=preserve_nans)
        else:
            for k in range(dim[1]):
                data[:, k] = smooth(data[:, k], width=width,
                                    preserve_nans=preserve_nans)

        pyspedas.tplot_tools.data_quants[new].values = data

        logging.info('tsmooth was applied to: ' + new)

    return n_names
