import numpy as np


def slice2d_s2c(r, theta, phi):
    """

    """
    rd = np.pi/180.0
    a = np.cos(rd*theta)
    vec = np.array((a*np.cos(rd*phi)*r,
                    a*np.sin(rd*phi)*r,
                np.sin(rd*theta)*r))
    return vec.T
