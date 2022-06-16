import numpy as np


def slice2d_get_ebounds(dist):
    """
    Returns an array of gapless energy boundaries.  The number of
    elements returned will always be N+1 for N energy levels.

    Input
    ------
        dist: dict
            3D particle data structure

    Returns
    --------
        Array of energy bin boundaries (# energy bins + 1)
    """
    n = dist['energy'].shape[0]+1
    energies = np.zeros((n, dist['energy'][:, :, :].shape[1], dist['energy'][:, :, :].shape[2]))

    # use midpoints
    energies[1:n-1, :, :] = (dist['energy'][0:n-2, :, :] + dist['energy'][1:n-1, :, :])/2.0

    # top/bottom energies
    energies[0, :, :] = dist['energy'][0, :, :] + (dist['energy'][0, :, :] - energies[1, :, :])
    energies[n-1, :, :] = dist['energy'][n-2, :, :] + (dist['energy'][n-2, :, :] - energies[n-2, :, :])

    return energies
