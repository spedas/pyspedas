from copy import deepcopy
import numpy as np


def qtom(qi):
    """
    Transforms quaternions into rotation matrices. Returns the transpose of the rotation matrix.

    This routine is based on the IDL version by Patrick Cruce
    """

    e00 = qi[:, 0] * qi[:, 0]
    e11 = qi[:, 1] * qi[:, 1]
    e22 = qi[:, 2] * qi[:, 2]
    e33 = qi[:, 3] * qi[:, 3]
    e01 = 2 * qi[:, 0] * qi[:, 1]
    e02 = 2 * qi[:, 0] * qi[:, 2]
    e03 = 2 * qi[:, 0] * qi[:, 3]
    e12 = 2 * qi[:, 1] * qi[:, 2]
    e13 = 2 * qi[:, 1] * qi[:, 3]
    e23 = 2 * qi[:, 2] * qi[:, 3]

    mout = np.zeros((len(e00), 3, 3))

    mout[:, 0, 0] = e00 + e11 - e22 - e33
    mout[:, 1, 0] = e12 + e03
    mout[:, 2, 0] = e13 - e02
    mout[:, 0, 1] = e12 - e03
    mout[:, 1, 1] = e00 - e11 + e22 - e33
    mout[:, 2, 1] = e23 + e01
    mout[:, 1, 2] = e23 - e01
    mout[:, 0, 2] = e13 + e02
    mout[:, 2, 2] = e00 - e11 - e22 + e33

    return mout


def qcompose(vec, theta, free=True):
    """
    Compose quaternions from vectors and angles

    This routine is based on the IDL version by Patrick Cruce
    """

    # Constant indicating where sin(theta) is close enough to theta
    epsilon = 1.0e-20

    vi = deepcopy(vec)
    thi = deepcopy(theta)

    # this next block of code moves angles into the range [0,PI)
    if not free:
        thi = thi % np.pi

        idx = np.argwhere(thi < 0)

        if len(idx) > 1:
            thi[idx] += np.pi

    # calculate the vector norm
    norm = np.sqrt(np.nansum(vi*vi, axis=1))

    # decide which quaternions become identity vectors
    idx1 = np.argwhere(norm < epsilon).flatten()
    idx2 = np.argwhere(norm >= epsilon).flatten()

    out_arr = np.zeros((len(norm), 4))

    if len(idx1) > 0:
        out_arr[idx1, 0] = 1.0
        out_arr[idx1, 1:4] = 0.0

    if len(idx2) > 0:
        out_arr[idx2, 0] = np.cos(thi[idx2]/2.0)

        stheta2 = np.sin(thi[idx2]/2.0)

        out_arr[idx2, 1] = (stheta2 * vi[idx2, 0])/norm[idx2]
        out_arr[idx2, 2] = (stheta2 * vi[idx2, 1])/norm[idx2]
        out_arr[idx2, 3] = (stheta2 * vi[idx2, 2])/norm[idx2]

    return out_arr
