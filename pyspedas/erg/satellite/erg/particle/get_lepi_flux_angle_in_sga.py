import numpy as np

from astropy.coordinates import cartesian_to_spherical


def get_lepi_flux_angle_in_sga(looking_dir=False):

    """
    ;; Here, phi is the angles of the flux directions in the SGA Y-Z plane
    ;; as defined to be angles from the +Y axis increasing toward the +Z axis. 
    ;; Please see Asamura+, EPS, 2018 for the details.    
    """

    phi_array = np.array( 
        [ 101.25, 123.75, 146.25, 168.75, 191.25, 213.75, 236.25, 258.75,
          281.25, 303.75, 326.25, 348.75, 33.75, 56.25, 78.75 ]
    )

    #;; Inclination of apertures = 0.0 deg
    theta_array = np.full(shape=(15), fill_value=0.)

    """
    ;; unit vector of looking direction 
    ;;   e_array is a 2-D array [azch, 3(x,y,z)] in SGA/SGI 
    """
    dtor = np.pi / 180.

    e_array = np.array([
     1. * np.sin(theta_array*dtor),
     1. * np.cos(theta_array*dtor) * np.cos(phi_array*dtor),
     1. * np.cos(theta_array*dtor) * np.sin(phi_array*dtor)
     ])

    if looking_dir:
        e_array *= -1.  # ;;Flip the directions to be looking dirs

    spherical_data = cartesian_to_spherical(
        x=e_array[0],
        y=e_array[1],
        z=e_array[2]
    )

    rtod = 180. / np.pi
    elev_array = spherical_data[1].value * rtod
    phi_array = spherical_data[2].value * rtod

    anglarr = np.zeros(shape=(2, 3, 15))  # ;[ elev/phi, min/cnt/max, apd_no ]

    anglarr[0] = elev_array
    anglarr[1] = phi_array

    return anglarr
