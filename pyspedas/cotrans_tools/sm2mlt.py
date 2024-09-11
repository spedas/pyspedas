'''
Convert Solar Magnetic (SM) coordinates to Magnetic Local Time (MLT).

This function is similar to sm2mlt.pro in IDL SPEDAS.
'''
import numpy as np
from pyspedas import cart2spc


def sm2mlt(x_sm, y_sm, z_sm):
    """
    Convert Solar Magnetic (SM) coordinates to Magnetic Local Time (MLT).

    Parameters:
    -----------
    x_sm : float
        X coordinate in Solar Magnetic system.
    y_sm : float
        Y coordinate in Solar Magnetic system.
    z_sm : float
        Z coordinate in Solar Magnetic system.

    Returns:
    --------
    mlt_0 : float
        Magnetic Local Time.

    Notes:
    ------
    - First, the SM coordinates are converted to spherical coordinates.
    - The azimuthal angle from the conversion (phi) is then used to calculate MLT.
    - If the resulting MLT is greater than 24, it is corrected by subtracting 24.
    """

    # Convert to spherical coordinates
    r, theta, phi = cart2spc(x_sm, y_sm, z_sm)

    # Calculate initial MLT
    mlt_0 = 12.0 + phi * 24.0 / (2.0 * np.pi)

    # Fix MLTs greater than 24
    mlt_0[mlt_0 > 24.0] -= 24.0

    return mlt_0
