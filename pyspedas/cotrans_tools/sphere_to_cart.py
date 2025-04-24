'''
Convert spherical coordinates (r, theta, phi) to Cartesian coordinates (x, y, z).

This function is similar to sphere_to_cart.pro in IDL SPEDAS.
'''
import numpy as np


def sphere_to_cart(r, theta, phi):
    """
    Convert spherical coordinates in degrees (r, theta, phi) to Cartesian coordinates (x, y, z).

    Parameters:
    -----------
    r : float
        Radial distance from the origin.
    theta : float
        Altitude angle (not co-latitude!) It ranges from -90 to 90 degrees
    phi : float
        Azimuthal angle (angle in the xy-plane from the positive x-axis to the point) in degrees. It ranges from [0, 360].

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
        x = r*cos(theta)*cos(phi)
        y = r*cos(theta)*sin(phi)
        z = r*sin(theta)
    """
    r, theta, phi = np.array(r), np.deg2rad(theta), np.deg2rad(phi)
    c = np.cos(theta)
    x = r * c * np.cos(phi)
    y = r * c * np.sin(phi)
    z = r * np.sin(theta)

    return x, y, z
