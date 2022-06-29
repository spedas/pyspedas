import numpy as np


def slice2d_checkbins(dist1, dist2):
    """
    Checks if two particle distribution structures have identical
    energy, phi, theta, and mass values.

    Input
    ------
        dist1: 3D particle data structure
            First particle data structure

        dist2: 3D particle data structure
            Second particle data structure

    Output
    -------
        Returns 1 if all fields match and 0 otherwise
    """

    if dist2 is None:
        return 1

    if not np.array_equal(dist1['phi'], dist2['phi']) or \
       not np.array_equal(dist1['theta'], dist2['theta']) or \
       not np.array_equal(dist1['energy'], dist2['energy']) or \
       dist1['mass'] != dist2['mass']:
        return 0

    return 1
