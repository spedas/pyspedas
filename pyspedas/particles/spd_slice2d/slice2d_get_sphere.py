from copy import deepcopy
import numpy as np

from .slice2d_get_ebounds import slice2d_get_ebounds


def slice2d_get_sphere(dist, energy=False):
    """
    Calculates the center and width of all bins in spherical coordinates.

    Input
    ------
        dist: dict
            3D particle data structure

    Parameters
    -----------
        energy: bool
            Specifies that the user requested energy instead of velocity

    Returns
    --------
        Hash table containing center and width of all bins in spherical coordinates
    """
    n = dist['data'].shape[0]
    c = 299792458.0  # m/s

    # determine gapless energy boundaries.
    ebounds = slice2d_get_ebounds(dist)

    # calculate radial values
    if energy:
        rbounds = ebounds
    else:
        # convert mass from eV/(km/s)^2 to eV/c^2
        erest = dist['mass']*c**2/1e6

        # velocity in km/s (relativistic calc for high energy electrons)
        rbounds = c*np.sqrt(1-1/((ebounds/erest + 1)**2))/1000.0
    
    # get radial centers
    rad = (rbounds[0:n, :, :] + rbounds[1:n+1, :, :])/2.0
    phi = dist['phi'][:, :, :]
    theta = dist['theta'][:, :, :]

    # get bin widths (mainly for geometric method)
    dr = np.abs(rbounds[1:n+1, :, :] - rbounds[0:n, :, :])
    dp = dist['dphi'][:, :, :]
    dt = dist['dtheta'][:, :, :]

    return {'rad': rad,
            'phi': phi,
            'theta': theta,
            'dr': dr,
            'dp': dp,
            'dt': dt}
