
import numpy as np
from astropy.coordinates import spherical_to_cartesian, cartesian_to_spherical


def spd_pgs_do_fac(data_in, mat):
    """
    Applies field aligned coordinate transformation to input data

    Input:
        data_in: dict
            Particle data structure to be rotated

        mat: numpy.ndarray
            The 3x3 field-aligned rotation matrix to apply to the data

    Returns:
        Rotated particle data structure
    """

    data_out = data_in.copy()
    rvals = np.ones(data_in['data'].shape)
    cart_data = spherical_to_cartesian(rvals, data_in['theta']*np.pi/180.0, data_in['phi']*np.pi/180.0)

    x = mat[0, 0]*cart_data[0] + mat[0, 1]*cart_data[1] + mat[0, 2]*cart_data[2]
    y = mat[1, 0]*cart_data[0] + mat[1, 1]*cart_data[1] + mat[1, 2]*cart_data[2]
    z = mat[2, 0]*cart_data[0] + mat[2, 1]*cart_data[1] + mat[2, 2]*cart_data[2]

    sphere_data = cartesian_to_spherical(x, y, z)

    data_out['theta'] = sphere_data[1].value*180.0/np.pi
    data_out['phi'] = sphere_data[2].value*180.0/np.pi

    return data_out
