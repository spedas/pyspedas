"""
Python implementation of IDL roundsig function.

Rounds numbers to a specified number of significant figures.
"""

import numpy as np


def roundsig(x, sigfig=None, uncertainty=None):
    """
    Round numbers to a specified number of significant figures.

    Python translation of IDL roundsig function.

    Parameters
    ----------
    x : array_like
        Input values to round.
    sigfig : int, optional
        Number of significant figures (default=1).
    uncertainty : float, optional
        If provided, rounds to nearest multiple of uncertainty.

    Returns
    -------
    ndarray
        Rounded values.
    """
    x = np.asarray(x, dtype=float)

    # Handle uncertainty case (IDL keyword_set(unc))
    if uncertainty is not None:
        return uncertainty * np.round(x / uncertainty)

    # Default sigfig to 1 if not provided
    if sigfig is None:
        sigfig = 1

    # Work with copy to avoid modifying input
    lx = x.copy()

    # Track negative values
    neg = lx < 0

    # Track zero values
    wz = lx == 0
    if np.any(wz):
        lx[wz] = 1.0

    # Take log10 of absolute values
    lx = np.log10(np.abs(lx))

    # Calculate exponent and fractional parts
    e = np.floor(lx - sigfig)
    f = lx - e

    # Calculate mantissa
    man = np.round(10**f)

    # Reconstruct the rounded value
    rx = man * (10.0**e)

    # Restore negative signs
    if np.any(neg):
        rx[neg] = -rx[neg]

    # Restore zeros
    if np.any(wz):
        rx[wz] = 0

    return rx
