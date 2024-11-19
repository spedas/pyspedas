"""
Convert Cartesian coordinates to spherical coordinates.

This function is similar to cart2spc.pro in IDL SPEDAS.
"""

import numpy as np


def cart2spc(x, y, z):
    """
    Convert Cartesian coordinates to spherical coordinates.

    Parameters:
    -----------
    x : float
        X coordinate in Cartesian system.
    y : float
        Y coordinate in Cartesian system.
    z : float
        Z coordinate in Cartesian system.

    Returns:
    --------
    r : float
        Radial distance from the origin.
    theta : float
        Polar angle (angle from the positive z-axis to the point) in radians. It ranges from [0, pi].
    phi : float
        Azimuthal angle (angle in the xy-plane from the positive x-axis to the point) in radians. It ranges from [0, 2*pi].

    Notes:
    ------
    - Uses the following equations for conversion:
        r = sqrt(x^2 + y^2 + z^2)
        theta = arccos(z/r)
        phi = 2*pi - arccos(x/sqrt(x^2 + y^2)) if y < 0, otherwise arccos(x/sqrt(x^2 + y^2))
    """

    x, y, z = np.array(x), np.array(y), np.array(z)
    r = np.sqrt(x**2 + y**2 + z**2)

    # Calculate phi
    maskn = np.where(y < 0, 1, 0)
    maskp = np.where(y > 0, 1, 0)
    phi = 2*np.pi - maskn * np.arccos(x/np.sqrt(x**2 + y**2)) + maskp * np.arccos(x/np.sqrt(x**2 + y**2))

    # Calculate theta
    theta = np.arccos(z/r)

    return r, theta, phi
