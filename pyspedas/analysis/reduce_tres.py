"""
Python implementation of IDL reduce_tres function.

Uses pyspedas rebin function.
"""
import numpy as np
from pyspedas.analysis.rebin import rebin


def reduce_tres(dat, n):
    """
    Rebin arrays by a specified factor.

    Python translation of IDL reduce_tres.pro function.

    Parameters
    ----------
    dat : array_like
        Input data array to be rebinned
    n : int
        Rebinning factor. If n <= 1, returns original data unchanged.

    Returns
    -------
    array_like
        Rebinned array with reduced time resolution, or original data if n <= 1
    """
    if n <= 1:
        return dat

    dat = np.asarray(dat)
    dim = dat.shape

    # Calculate how many elements to truncate to make divisible by n
    m = dim[0] % n
    l = dim[0] - m - 1

    # Handle different dimensionalities
    if dat.ndim == 1:
        # IDL: return,rebin(dat[0:l],dim[0]/n)
        truncated = dat[: l + 1]
        new_dim = len(truncated) // n
        return rebin(truncated, new_dim)

    elif dat.ndim == 2:
        # IDL: return,rebin(dat[0:l,*],dim[0]/n,dim[1])
        truncated = dat[: l + 1, :]
        new_dim0 = truncated.shape[0] // n
        new_dim1 = dim[1]
        return rebin(truncated, (new_dim0, new_dim1))

    elif dat.ndim == 3:
        # IDL: return,rebin(dat[0:l,*,*],dim[0]/n,dim[1],dim[2])
        truncated = dat[: l + 1, :, :]
        new_dim0 = truncated.shape[0] // n
        new_dim1 = dim[1]
        new_dim2 = dim[2]
        return rebin(truncated, (new_dim0, new_dim1, new_dim2))

    else:
        # For higher dimensions, return 0 (matching IDL behavior)
        return 0
