import numpy as np

def bshock_2(xsh=None, *, short=False, xsh_max=14.3, return_west=False):
    """
    Compute location of bow shock, ported from the IDL SPEDAS bshock_2 utility

    Parameters
    ----------
    xsh : array-like or None
        If None or empty, generate xsh from xsh_min to xsh_max with npoints.
    short : bool
        If False (IDL default), return the full curve with east branch + mirrored west branch.
        If True, return only the east branch.
    xsh_max : float
        Maximum xsh used when generating xsh (IDL default 14.3).
    return_west : bool
        If True, also return ysh_west (on the original xsh grid, not mirrored/concatenated).

    Returns
    -------
    xsh_out : ndarray
    ysh_out : ndarray
    (optional) ysh_west : ndarray
    """
    # IDL defaults / constants
    xsh_min = -300.0
    npoints = 1000
    aberangle = 4.5  # present in IDL but unused in this routine

    # IDL: if n_elements(xsh) eq 0 then generate
    if xsh is None:
        xsh_arr = np.linspace(xsh_min, xsh_max, npoints, dtype=float)
    else:
        xsh_arr = np.asarray(xsh, dtype=float)
        if xsh_arr.size == 0:
            xsh_arr = np.linspace(xsh_min, xsh_max, npoints, dtype=float)

    # coefficients
    a1 = 0.2164
    b1 = -0.0986
    c1 = -4.26
    d1 = 44.916
    e1 = -623.77

    beta = a1 * xsh_arr + c1
    gamma = b1 * (xsh_arr ** 2) + d1 * xsh_arr + e1
    delta = beta**2 - 4.0 * gamma

    # Match IDL: sqrt(delta) (IDL would yield NaN/complex depending on settings;
    # NumPy will produce nan for negative delta with real dtype)
    sqrt_delta = np.sqrt(delta)

    ysh_east = (-beta - sqrt_delta) / 2.0
    ysh_west = (-beta + sqrt_delta) / 2.0

    if not short:
        # IDL:
        # ireverse = n_elements(xsh) - indgen(n_elements(xsh)) - 1
        # xsh = [xsh, xsh(ireverse)]
        # ysh = [ysh_east, ysh_west(ireverse)]
        x_rev = xsh_arr[::-1]
        y_out = np.concatenate([ysh_east, ysh_west[::-1]])
        x_out = np.concatenate([xsh_arr, x_rev])
    else:
        x_out = xsh_arr
        y_out = ysh_east

    if return_west:
        return x_out, y_out, ysh_west
    return x_out, y_out
