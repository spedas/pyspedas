
def spd_pgs_limit_range(data, phi=None, theta=None, energy=None):
    """
    Applies phi, theta, and energy limits to data structure(s) by
    turning off the corresponding bin flags.

    Parameters
    ----------
        data: dict
            Particle data structure

        phi: np.ndarray
            Minimum and maximum values for phi

        theta: np.ndarray
            Minimum and maximum values for theta

        energy: np.ndarray
            Minimum and maximum values for energy

    Returns
    -------
    dict
        Data structure with limits applied (to the bins array)
    """

    # if no limits are set, return the input data
    if energy is None and theta is None and phi is None:
        return data

    # apply the phi limits
    if phi is not None:
        # get min/max phi values for all bins
        phi_min = data['phi'] - 0.5*data['dphi']
        phi_max = data['phi'] + 0.5*data['dphi'] % 360

        # wrap negative values
        phi_min[phi_min < 0.0] += 360

        # the code below and the phi spectrogram code 
        # assume maximums at 360 are not wrapped to 0
        phi_max[phi_max == 0.0] = 360.0

        # find which bins were wrapped back into [0, 360]
        wrapped = phi_min > phi_max

        # determine which bins intersect the specified range
        if phi[0] > phi[1]:
            in_range = phi_min < phi[1] or phi_max > phi[0] or wrapped
        else:
            in_range = ((phi_min < phi[1]) & (phi_max > phi[0])) | (wrapped & ((phi_min < phi[1]) | (phi_max > phi[0])))

        data['bins'][in_range == False] = 0

    # apply the theta limits
    if theta is not None:
        lower_theta = min(theta)
        upper_theta = max(theta)

        # get min/max angle theta values for all bins
        theta_min = data['theta'] - 0.5*data['dtheta']
        theta_max = data['theta'] + 0.5*data['dtheta']
        
        in_range = (theta_min < upper_theta) & (theta_max > lower_theta)
        data['bins'][in_range == False] = 0

    # apply the energy limits
    if energy is not None:
        data['bins'][data['energy'] < energy[0]] = 0
        data['bins'][data['energy'] > energy[1]] = 0

    return data
