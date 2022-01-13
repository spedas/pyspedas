import numpy as np
from pyspedas.analysis.tnormalize import tnormalize


def cart_trans_matrix_make(x, y, z):

    ndim = x.ndim

    if ndim == 2:
        ex = tnormalize(x, return_data=True)
        ey = tnormalize(y, return_data=True)
        ez = tnormalize(z, return_data=True)
        mat_out = np.concatenate([ex, ey, ez], 1).reshape(x.shape[0], 3, 3)

    elif ndim == 1:
        ex = x/np.sqrt((x*x).sum())
        ey = y/np.sqrt((y*y).sum())
        ez = z/np.sqrt((z*z).sum())
        mat_out = np.array([ex, ey, ez]).T

    return mat_out
