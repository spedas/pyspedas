"""
Convert Cartesian coordinates to spherical coordinates.

This function is similar to cart_to_sphere.pro in IDL SPEDAS.
"""

import numpy as np


def cart_to_sphere(x, y, z):
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
        Altitude angle (not co-latitude!) from XY plane to point, in degrees. It ranges from -90 to 90 degrees
    phi : float
        Azimuthal angle (angle in the xy-plane from the positive x-axis to the point) in radians. It ranges from 0 to 360 degrees.

    Notes:
    ------
    - Uses the following equations for conversion:
        r = sqrt(x^2 + y^2 + z^2)
        theta = arcsin(z/r)
        phi = 2*pi - arccos(x/sqrt(x^2 + y^2)) if y < 0, otherwise arccos(x/sqrt(x^2 + y^2))
    """

    x, y, z = np.array(x), np.array(y), np.array(z)
    r = np.sqrt(x**2 + y**2 + z**2)

    # Calculate phi
    maskn = np.where(y < 0, 1, 0)
    maskp = np.where(y > 0, 1, 0)
    phi = 2*np.pi - maskn * np.arccos(x/np.sqrt(x**2 + y**2)) + maskp * np.arccos(x/np.sqrt(x**2 + y**2))

    # Calculate theta
    theta = np.arcsin(z/r)

    return r, np.rad2deg(theta), np.rad2deg(phi)
