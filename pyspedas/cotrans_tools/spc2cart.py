'''
Convert spherical coordinates (r, theta, phi) to Cartesian coordinates (x, y, z).

This function is similar to spc2cart.pro in IDL SPEDAS.
'''
import numpy as np


def spc2cart(r, theta, phi):
    """
    Convert spherical coordinates (r, theta, phi) to Cartesian coordinates (x, y, z).

    Parameters:
    -----------
    r : float
        Radial distance from the origin.
    theta : float
        Polar angle (angle from the positive z-axis to the point) in radians. It ranges from [0, pi].
    phi : float
        Azimuthal angle (angle in the xy-plane from the positive x-axis to the point) in radians. It ranges from [0, 2*pi].

    Returns:
    --------
    x : float
        X coordinate in Cartesian system.
    y : float
        Y coordinate in Cartesian system.
    z : float
        Z coordinate in Cartesian system.

    Notes:
    ------
    - Uses the following equations for conversion:
        x = r*sin(theta)*cos(phi)
        y = r*sin(theta)*sin(phi)
        z = r*cos(theta)
    """
    r, theta, phi = np.array(r), np.array(theta), np.array(phi)
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    return x, y, z
