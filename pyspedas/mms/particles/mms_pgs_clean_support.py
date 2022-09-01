from pyspedas import tinterpol
from pytplot import get_data


def mms_pgs_clean_support(times, mag_name=None, vel_name=None, sc_pot_name=None):
    """
	Transform and/or interpolate support data to match the particle data

	Parameters
    ----------
		mag_name: str
			Tplot variable containing magnetic field data

		vel_name: str
			Tplot variable containing bulk velocity data

		sc_pot_name: str
			Tplot variable containing spacecraft potential data

	Returns
    ----------
		Tuple containing interpolated (magnetic field, velocity, spacecraft potential)
	"""

    out_mag = None
    out_vel = None
    out_scpot = None

    if mag_name is not None:
        mag_temp = mag_name + '_pgs_temp'
        tinterpol(mag_name, times, newname=mag_temp)
        interpolated_bfield = get_data(mag_temp)
        if interpolated_bfield is not None:
            out_mag = interpolated_bfield.y

    if vel_name is not None:
        vel_temp = vel_name + '_pgs_temp'
        tinterpol(vel_name, times, newname=vel_temp)
        interpolated_vel = get_data(vel_temp)
        if interpolated_vel is not None:
            out_vel = interpolated_vel.y

    if sc_pot_name is not None:
        scpot_temp = sc_pot_name + '_pgs_temp'
        tinterpol(sc_pot_name, times, newname=scpot_temp)
        interpolated_scpot = get_data(scpot_temp)
        if interpolated_scpot is not None:
            out_scpot = interpolated_scpot.y

    return (out_mag, out_vel, out_scpot)
