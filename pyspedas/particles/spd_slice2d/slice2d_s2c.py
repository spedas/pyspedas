import numpy as np


def slice2d_s2c(r, theta, phi):
    """
    Converts spherical coordinates to cartesian

    Input
    ------
        r: array of float
            Radial values

        theta: array of float
            Theta values

        phi: array of float
            Phi values

    Returns
    -------
        Nx3 array of cartesian values (x, y, z)
    """
    rd = np.pi/180.0
    a = np.cos(rd*theta)
    vec = np.array((a*np.cos(rd*phi)*r,
                    a*np.sin(rd*phi)*r,
                    np.sin(rd*theta)*r))
    return vec.T
