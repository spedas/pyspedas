import logging
import numpy as np


def slice2d_subtract(vectors=None, velocity=None):
    """
    Shift velocities by specified vector
    """

    if vectors is None or velocity is None:
        return

    if vectors.shape[1] != 3 or len(velocity) != 3:
        logging.error('Invalid vector dimensions, cannot subtract velocity')
        return

    if np.sum(~np.isfinite((velocity))):
        logging.error('Invalid bulk velocity data, cannot subtract velocity')
        return

    if not isinstance(velocity, np.ndarray):
        velocity = np.array(velocity)

    v = -velocity

    vectors[:, 0] = vectors[:, 0] + v[0]
    vectors[:, 1] = vectors[:, 1] + v[1]
    vectors[:, 2] = vectors[:, 2] + v[2]

    return vectors
