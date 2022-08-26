import numpy as np


def erg_pgs_limit_range(data_in, phi=None, theta=None, energy=None,
                        no_ang_weighting=False):

    """
    Applies phi, theta, and energy limits to data structure(s) by
    turning off the corresponding bin flags.

    Input:
        data: dict
            Particle data structure

    Parameters:
        phi: np.ndarray
            Minimum and maximum values for phi

        theta: np.ndarray
            Minimum and maximum values for theta

        energy: np.ndarray
            Minimum and maximum values for energy

    Returns:
        Data structure with limits applied (to the bins array)
    """

    # Apply phi limits

    if phi is not None:

        # phi can be in any order
        phi_in = phi

        # get min/max phi values for all bins
        if not no_ang_weighting:
            phi_min = data_in['phi'] - 0.5 * data_in['dphi']
            phi_max = np.fmod(data_in['phi'] + 0.5 * data_in['dphi'], 360.)
        else:
            phi_min = data_in['phi'] - 0.
            phi_max = np.fmod(data_in['phi'] + 0., 360.)

        # ;wrap negative values
        phi_min[phi_min < 0.0] += 360.

        """
        ;the code below and the phi spectrogram code
        ;assume maximums at 360 are not wrapped to 0
        """
        phi_max[phi_max == 0.0] = 360.0

        # ;find which bins were wrapped back into [0,360]
        wrapped = phi_min > phi_max

        # determine which bins intersect the specified range
        if phi_in[0] > phi_in[1]:
            in_range = phi_min < phi_in[1] or phi_max > phi_in[0] or wrapped
        else:
            in_range = ((phi_min < phi_in[1]) & (phi_max > phi_in[0]))\
                        | (wrapped & ((phi_min < phi_in[1]) | (phi_max > phi_in[0])))

        data_in['bins'][in_range == False] = 0

    # ;Apply theta limits
    if theta is not None:

        input_theta_array = np.array(theta)
        theta_min_max = np.array([np.nanmin(input_theta_array),
                                  np.nanmax(input_theta_array)])
        if not no_ang_weighting:
            theta_min = data_in['theta'] - 0.5 * data_in['dtheta']
            theta_max = data_in['theta'] + 0.5 * data_in['dtheta']
        else:
            theta_min = data_in['theta'] - 0.
            theta_max = data_in['theta'] + 0.

        # ;determine which bins intersect the specified range
        in_range = ((theta_min < theta_min_max[1]) \
                    & (theta_max > theta_min_max[0]))
        data_in['bins'][in_range == False] = 0

    # ;Apply energy limits
    if energy is not None:
        data_in['bins'][data_in['energy'] < energy[0]] = 0
        data_in['bins'][data_in['energy'] > energy[1]] = 0

    return data_in
