import numpy as np

from astropy.coordinates import cartesian_to_spherical


def get_mepi_flux_angle_in_sga(looking_dir=False):

    #;; --- starts from -Z(SGI) axis and increases toward -Y(SGI) axis.
    azi_0 = 11.25  # ;;[deg] offset of channel 0 (anode 00) from -Z(SGI) axis
    d_azi = 22.5   # ;;[deg] angula interval between the centers of neighboring ch

    phi_array = azi_0 + (np.arange(16)) * d_azi

    #;; Inclination of apertures, based on visual inspection
    theta_array = np.full(shape=(16), fill_value=1.6)

    """
    ;; unit vector of looking direction 
    ;;   e_array is a 2-D array [azch, 3(x,y,z)] in SGA/SGI 
    """
    dtor = np.pi / 180.

    e_array = np.array([
     -1 * np.sin(theta_array*dtor),
     -1 * np.cos(theta_array*dtor) * np.sin(phi_array*dtor),
     -1 * np.cos(theta_array*dtor) * np.cos(phi_array*dtor)
     ])

    if not looking_dir:
        e_array *= -1.  # ;;Flip the directions to be flux dirs

    spherical_data = cartesian_to_spherical(
        x=e_array[0],
        y=e_array[1],
        z=e_array[2]
    )

    rtod = 180. / np.pi
    elev_array = spherical_data[1].value * rtod
    phi_array = spherical_data[2].value * rtod

    anglarr = np.zeros(shape=(2, 3, 16))  # ;[ elev/phi, min/cnt/max, apd_no ]

    anglarr[0] = elev_array
    anglarr[1] = phi_array

    return anglarr
