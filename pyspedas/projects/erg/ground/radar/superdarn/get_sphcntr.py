
import numpy as np

from astropy.coordinates import cartesian_to_spherical

def get_sphcntr(latarr, lonarr):
    if latarr.size != lonarr.size:
        print('get_sphcntr: Array size does not match!')
        return np.array([np.nan, np.nan])
    deg_to_rad = np.pi / 180.
    phiarr = lonarr * deg_to_rad
    thearr = (90. - latarr) * deg_to_rad
    x_array = np.sin(thearr) * np.cos(phiarr)
    y_array = np.sin(thearr) * np.sin(phiarr)
    z_array = np.cos(thearr)
    sum_x = np.nansum(x_array)
    sum_y = np.nansum(y_array)
    sum_z = np.nansum(z_array)
    r_value, theta_value, phi_value = cartesian_to_spherical(sum_x, sum_y, sum_z)
    return [theta_value.value / deg_to_rad , phi_value.value / deg_to_rad]

