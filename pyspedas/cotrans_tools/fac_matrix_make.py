import logging
import numpy as np
import pyspedas
#from pyspedas import tinterpol, interpol

from pytplot import get_coords
from pytplot import tnormalize
from pytplot import tcrossp

from pytplot import get_data, store_data, del_data

from pyspedas.cotrans_tools.xyz_to_polar import xyz_to_polar
from pyspedas.cotrans_tools.cotrans import cotrans

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


# === Helper Functions ===

def validate_vector_data(var_name, expected_dim=3):
    """
    Retrieve tplot variable and check that the 'y' field is an Nx{expected_dim} array.
    """
    data = get_data(var_name)
    if data is None:
        logging.error(f"Error reading tplot variable: {var_name}")
        return None
    if data.y.ndim != 2 or data.y.shape[1] != expected_dim:
        logging.error(f"{var_name} data must be an Nx{expected_dim} array")
        return None
    return data


def interpolate_position(pos_var_name, interp_to):
    """
    Interpolate position data to the time grid of the magnetic field variable.
    The result is stored as pos_var_name + "-itrp".
    """
    pyspedas.tinterpol(names=pos_var_name, interp_to=interp_to, method="linear",
              newname=None, extrapolate=True, suffix="-itrp")
    interp_var = pos_var_name + "-itrp"
    interp_data = get_data(interp_var)
    if interp_data is None:
        logging.error("Interpolation failed for %s", pos_var_name)
    return interp_data


def normalize_vectors(vectors):
    """Normalize an array of vectors along the last axis."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1  # avoid division by zero
    return vectors / norms


def pos_cotrans(pos_times, pos_data, mag_var_name):
    """Coordinate transformation of position"""
    store_data('fac_mat_pos_tmp', data={'x': pos_times, 'y': pos_data})

    # Retrieve the coordinate system mad_var_name
    coord_system = get_coords(mag_var_name)

    cotrans(name_in='fac_mat_pos_tmp', coord_in='gei', coord_out=coord_system.lower())
    newname = 'fac_mat_pos_tmp_' + coord_system.lower()
    pos_data = get_data(newname)
    del_data(newname)

    return pos_data.y


def get_z_axis(mag_data):
    """Normalized magnetic field vector"""
    return tnormalize(mag_data.y, return_data=True)


def build_fac_axes(z, refv, mode='yxz'):
    """Construct FAC axes based on defined mode"""
    if mode == 'yxz':
        y = tcrossp(z, refv, return_data=True)
        y = normalize_vectors(y)
        x = tcrossp(y, z, return_data=True)
        return x, y, z
    elif mode == 'xyz':
        x = tcrossp(refv, z, return_data=True)
        x = normalize_vectors(x)
        y = tcrossp(z, x, return_data=True)
        y = normalize_vectors(y)
        return x, y, z
    else:
        logging.error("Bad cross order: " + mode)
        return None, None, None


def get_ref_xgse(N):
    x_axis = np.zeros((N, 3))
    x_axis[:, 0] = 1
    return x_axis


def get_ref_ygsm(pos_data, mag):
    magdat = get_data(mag)
    y_axis = np.zeros((len(magdat.times), 3))
    y_axis[:, 1] = 1
    mag_coord = get_coords(mag).lower()
    arr = cotrans(data_in=y_axis, time_in = magdat.times, coord_in='gsm', coord_out=mag_coord)
    return arr


def get_ref_rgeo(pos_data, mag_var_name, sign=1):
    arr = normalize_vectors(pos_data.y * sign)
    arr = pos_cotrans(pos_data.times, arr, mag_var_name)
    return arr


def get_ref_phi(pos_data, mag_var_name, sign=1):
    polar = xyz_to_polar(pos_data.y)
    phi_deg = polar[:, 2]
    arr = np.empty_like(pos_data.y)
    arr[:, 0] = -np.sin(np.radians(phi_deg)) * sign
    arr[:, 1] = np.cos(np.radians(phi_deg)) * sign
    arr[:, 2] = 0.0
    arr = pos_cotrans(pos_data.times, arr, mag_var_name)
    return arr

def get_ref_phi_sm(pos_data, mag_var_name, sign=1):
    polar = xyz_to_polar(pos_data.y)
    phi_deg = polar[:, 2]
    arr = np.empty_like(pos_data.y)
    arr[:, 0] = -np.sin(np.radians(phi_deg)) * sign
    arr[:, 1] = np.cos(np.radians(phi_deg)) * sign
    arr[:, 2] = 0.0
    arr_gei = cotrans(data_in=arr, time_in=pos_data.times, coord_in='sm', coord_out='gei')
    arr = pos_cotrans(pos_data.times, arr_gei, mag_var_name)
    return arr

# === Dictionary Mapping Option Strings to Functions ===
COORD_FUNCTIONS = {
    "xgse": {"mode": "yxz", "ref": lambda mag, pos: get_ref_xgse(len(get_data(mag).times))},
    "rgeo": {"mode": "yxz", "ref": lambda mag, pos: get_ref_rgeo(pos, mag, 1)},
    "mrgeo": {"mode": "yxz", "ref": lambda mag, pos: get_ref_rgeo(pos, mag, -1)},
    "phigeo": {"mode": "xyz", "ref": lambda mag, pos: get_ref_phi(pos, mag,  1)},
    "mphigeo": {"mode": "xyz", "ref": lambda mag, pos: get_ref_phi(pos, mag, -1)},
    "phism": {"mode": "xyz", "ref": lambda mag, pos: get_ref_phi_sm(pos, mag,  1)},
    "mphism": {"mode": "xyz", "ref": lambda mag, pos: get_ref_phi_sm(pos, mag, -1)},
    "ygsm": {"mode": "xyz", "ref": lambda mag, pos: get_ref_ygsm(pos, mag)}
}

# === Main Interface ===
def fac_matrix_make(mag_var_name, other_dim='Xgse', pos_var_name=None, newname=None):
    """
    Generate a field-aligned coordinate (FAC) transformation matrix from the given magnetic
    field B and (if required) position data, and store it in a tplot variable.

    Parameters
    ----------
    mag_var_name : str
        tplot variable containing the magnetic field data.
    other_dim : str, optional
        The coordinate system option. Must be one of:
        ['xgse','rgeo','phigeo', 'mrgeo','mphigeo','phism','mphism','ygsm','zdsl'].
        (Default is "xgse".)
    pos_var_name : str, optional
        tplot variable containing the spacecraft position data.
        Required for all options except "xgse" (and "zdsl", in development).
    newname : str, optional
        Name of the output tplot variable. Defaults to mag_var_name + "_fac_mat".

    Returns
    -------
    str or None
        The name of the output tplot variable containing the FAC matrix,
        or None if an error occurs.
    """

    mag_data = validate_vector_data(mag_var_name)

    if mag_data is None:
        logging.error('Error reading tplot variable: %s', mag_var_name)
        return

    if newname is None:
        newname = mag_var_name + '_fac_mat'

    # Standardize coordinate option.
    coord_option = other_dim.lower()

    if coord_option not in COORD_FUNCTIONS:
        logging.error("Unsupported transform %s", other_dim)
        return None

    # For certain coordinate systems, a position variable is required.
    required_pos = ["rgeo", "mrgeo", "phigeo", "mphigeo", "phism", "mphism"]
    if coord_option in required_pos and pos_var_name is None:
        logging.error("Need pos_var_name for %s", other_dim)
        return None

    if coord_option in required_pos:
        # All routines assume the position data is originally in GEI.
        if get_coords(pos_var_name).lower() != 'gei':
            logging.error("Position must be in GEI coordinates for tplot variable %s.", pos_var_name)
            return None

        if coord_option in ["phism", "mphism"]:
            # Convert position to sm
            cotrans(name_in=pos_var_name, name_out=pos_var_name + '-sm', coord_out='sm')
            pos_var_name = pos_var_name + '-sm'

        # Interpolate position data onto the magnetic field's time grid.
        interp_pos_data = interpolate_position(pos_var_name, mag_var_name)
        if interp_pos_data is None:
            return None
    else:
        interp_pos_data = None

    # Retrieve the normalized magnetic field vector (FAC Z-axis).
    fac_z_axis = get_z_axis(mag_data)
    if fac_z_axis is None:
        return None

    # Get the reference vector using the transform's reference function.
    ref_vector = COORD_FUNCTIONS[coord_option]["ref"](mag_var_name, interp_pos_data)
    if ref_vector is None:
        return None

    # Build the FAC axes (x, y, z) using the normalized magnetic field and the reference vector.
    x_axis, y_axis, z_axis = build_fac_axes(fac_z_axis, ref_vector, mode=COORD_FUNCTIONS[coord_option]["mode"])
    if x_axis is None:
        return None

    # Construct the FAC matrix.
    num_points = len(mag_data.times)
    fac_mat = np.zeros((num_points, 3, 3))
    fac_mat[:, 0, :] = x_axis
    fac_mat[:, 1, :] = y_axis
    fac_mat[:, 2, :] = z_axis

    # Store the computed FAC matrix into a new tplot variable.
    store_data(newname, data={'x': mag_data.times, 'y': fac_mat})

    return newname
