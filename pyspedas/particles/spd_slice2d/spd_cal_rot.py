import numpy as np


def spd_cal_rot(v1, v2):
    """
    Returns a rotation matrix that rotates v1,v2 to the x-y plane;
    v1 is rotated to the x-axis and v2 into the x-y plane

    Input
    ------
        v1: array of float
            3 component vector

        v2: array of float
            3 component vector

    Returns
    --------
        Rotation matrix that rotates v1,v2 to the x-y plane
    """

    v1 = np.array(v1)
    v2 = np.array(v2)
    a = v1/(np.nansum(v1**2))**(0.5)
    d = v2/(np.nansum(v2**2))**(0.5)
    c = np.cross(a, d)
    c = c/(np.nansum(c**2))**(0.5)
    b = -np.cross(a, c)
    b = b/(np.nansum(b**2))**(0.5)

    rotinv = np.zeros([3, 3])
    rotinv[0, :] = a
    rotinv[1, :] = b
    rotinv[2, :] = c

    return np.linalg.inv(rotinv)
