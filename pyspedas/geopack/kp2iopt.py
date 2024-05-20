import numpy as np
from pytplot import tnames,data_exists
from pyspedas import tinterpol


def kp2iopt(kp, varname=None, plus1=False):
    """
    Convert a tplot or array Kp index variable to iopt values suitable for passing to the T89 field
    modeling or tracing routines.

    Input Kp values will be in the range of 0 to 6, and may have a fractional part indicating an increasing
    or decreasing index. For example, 2.33333 represents 2+, 2.66666 represents 3-. iopt output values
    will be in the range 1 to 7.

    Parameters:
    ----------
    kp : scalar or array-like
        Kp values (e.g. from noaa_load_kp) or name of a tplot variable giving the Kp index values.

    varname : str, optional
        A string specifying a tplot position variable. Required if kp is a tplot variable.
        Output iopt values will be interpolated to the 'varname' times using nearest-neighbor interpolation.

    plus1 : bool, optional
        If specified, overrides the default behavior of rounding iopt to the nearest integer, and
        instead sets iopt to kp+1, preserving any fractional part.

    Returns:
    -------
    array-like
        IOPT values suitable for passing to the GEOPACK T89 tracing and modeling routines. Represented
        as double precision floating point for compatibility with GEOPACK library calling sequences,
        but may or may not be rounded to integer values depending on whether the kp_plus1 keyword is specified.
    """

    # Check if kp is a string
    if isinstance(kp, str):
        # Assume kp is stored in a tplot variable
        if not data_exists(kp):
            raise ValueError(f'kp is of type string but no tplot variable exists with name={kp}')

        # Interpolate kp values
        tinterpol(kp, varname, newname='kp_int_tmp',method="nearest")
        kp_dat = kp

    # Convert kp_dat to iopt values
    if plus1:
        iopt = kp_dat + 1.0
    else:
        iopt = np.floor(kp_dat + 1.5)

    # Force to valid iopt range
    iopt = np.clip(iopt, 1.0, 7.0)

    return iopt