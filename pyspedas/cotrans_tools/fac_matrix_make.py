import logging
import numpy as np

from pyspedas import tinterpol

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
    tinterpol(names=pos_var_name, interp_to=interp_to, method="linear",
              newname=None, suffix="-itrp")
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
    store_data('fac_mat_pos_tmp', data={'x': pos_times, 'y': pos_data})

    # Retrieve the coordinate system mad_var_name
    coord_system = get_coords(mag_var_name)

    cotrans(name_in='fac_mat_pos_tmp', coord_in='gei', coord_out=coord_system.lower())
    pos_data = get_data('fac_mat_pos_tmp')
    del_data('fac_mat_pos_tmp')

    return pos_data.y


def get_z_axis(mag_data):
    return tnormalize(mag_data.y, return_data=True)


def build_fac_axes(z, refv, mode='yxz'):
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


def get_ref_ygsm(N):
    y_axis = np.zeros((N, 3))
    y_axis[:, 1] = 1
    return y_axis


def get_ref_rgeo(pos_data, mag_var_name, sign=1):
    arr = normalize_vectors(pos_data.y * sign)
    arr = pos_cotrans(pos_data.times, arr, mag_var_name)
    return arr


def get_ref_phi(pos_data, mag_var_name, sign=1):
    polar = xyz_to_polar(pos_data.y)
    phi_deg = polar[:, 1]
    arr = np.empty_like(pos_data.y)
    arr[:, 0] = -np.sin(np.radians(phi_deg)) * sign
    arr[:, 1] = np.cos(np.radians(phi_deg)) * sign
    arr[:, 2] = 0.0

    arr = pos_cotrans(pos_data.times, arr, mag_var_name)
    return arr


# # === Previous Implementation === #
# def xgse(mag_var_name):
#     """
#     Generates the 'xgse' transformation matrix
#     """
#     mag_data = validate_vector_data(mag_var_name)
#     if mag_data is None:
#         return None
#
#     # xaxis of this system is X of the gse system. Z is mag field
#     N = len(mag_data.times)
#     x_axis = np.zeros((N, 3))
#     x_axis[:, 0] = 1
#
#     # create orthonormal basis set
#     z_basis = tnormalize(mag_var_name, return_data=True)
#     if z_basis is None:
#         return None
#
#     y_basis = tcrossp(z_basis, x_axis, return_data=True)
#     y_basis = tnormalize(y_basis, return_data=True)
#     x_basis = tcrossp(y_basis, z_basis, return_data=True)
#
#     return (x_basis, y_basis, z_basis)
#
# def rgeo(mag_var_name, pos_var_name):
#     """
#     Build FAC basis for the 'rgeo' option.
#     Rgeo is the normalized (interpolated) position vector.
#     Z-axis = normalized magnetic field.
#     Y-axis = B x Rgeo.
#     X-axis = Y x B.
#     """
#     pos_data = validate_vector_data(pos_var_name)
#     if pos_data is None:
#         return None
#
#     # Interpolate position data onto the magnetic field's time grid.
#     interp_pos_data = interpolate_position(pos_var_name, mag_var_name)
#     if interp_pos_data is None:
#         return None
#
#     # Normalize the interpolated position vector.
#     rgeo_norm = normalize_vectors(interp_pos_data.y)
#
#     # Z-axis: normalized magnetic field.
#     z_basis = tnormalize(mag_var_name, return_data=True)
#     if z_basis is None:
#         return None
#
#     # Y-axis: cross(B, Rgeo)
#     y_basis = tcrossp(z_basis, rgeo_norm, return_data=True)
#     y_basis = normalize_vectors(y_basis)
#
#     # X-axis: cross(Y, B)
#     x_basis = tcrossp(y_basis, z_basis, return_data=True)
#     return (x_basis, y_basis, z_basis)
#
# def phigeo(mag_var_name, pos_var_name, probe=None, sign=1):
#     """
#     Phigeo transformation (using azimuthal GEI phi vector).
#       - Interpolate position data and compute phi = arctan2(y, x) in degrees.
#       - Define phi_vector = [-sin(phi), cos(phi), 0], multiplied by sign.
#       - Transform phi_vector into the magnetic field coordinate system:
#           if mag system is 'gse' or 'gsm', use cotrans; if 'dsl', use thm_cotrans.
#       - Z-axis: normalized magnetic field.
#       - X-axis: computed as (phi_vector) x Z.
#       - Y-axis: computed as Z x X.
#     """
#     pos_data = validate_vector_data(pos_var_name)
#     if pos_data is None:
#         return None
#
#     interp_data = interpolate_position(pos_var_name, mag_var_name)
#     if interp_data is None:
#         return None
#
#     # Use xyz_to_polar function to convert Cartesian coordinates to polar.
#     # This function returns (r, theta, phi) where phi is in degrees.
#     res = xyz_to_polar(interp_data.y)
#     phi_deg = res[:, 1]
#
#     phi_vector = np.empty_like(interp_data.y)
#     phi_vector[:, 0] = -np.sin(np.radians(phi_deg)) * sign
#     phi_vector[:, 1] = np.cos(np.radians(phi_deg)) * sign
#     phi_vector[:, 2] = 0.0
#
#     mag_data = get_data(mag_var_name)
#
#     # TODO: This block of code is not yet correct
#     mag_coord_sys = "gei"
#     if hasattr(mag_data, "dlimits") and mag_data.dlimits is not None:
#         mag_coord_sys = mag_data.dlimits.get("data_att", {}).get("coord_sys", "gei").lower()
#
#     if mag_coord_sys == "gse":
#         phi_vector = cotrans(data_in=phi_vector, coord_in="gei", coord_out="gse")
#     elif mag_coord_sys == "gsm":
#         phi_vector = cotrans(phi_vector, coord_in="gei", coord_out="gsm")
#     elif mag_coord_sys == "dsl":
#         # TODO: implement dsl
#         # phi_vector = thm_cotrans(phi_vector, in_coord="gei", out_coord="dsl", probe=probe)
#         logging.error("dsl coordinate is not supported for phigeo yet")
#     else:
#         logging.error("Unsupported magnetic field coordinate system for phigeo")
#         return None
#
#     z_basis = tnormalize(mag_var_name, return_data=True)
#     if z_basis is None:
#         return None
#
#     x_basis = tcrossp(phi_vector, z_basis, return_data=True)
#     x_basis = normalize_vectors(x_basis)
#     y_basis = tcrossp(z_basis, x_basis, return_data=True)
#     y_basis = normalize_vectors(y_basis)
#     return (x_basis, y_basis, z_basis)
# # === End of Previous Implementation === #

# === Dictionary Mapping Option Strings to Functions ===
COORD_FUNCTIONS = {
    "xgse": {"mode": "yxz", "ref": lambda mag, pos: get_ref_xgse(len(get_data(mag).times))},
    "rgeo": {"mode": "yxz", "ref": lambda mag, pos: get_ref_rgeo(pos, mag, 1)},
    "mrgeo": {"mode": "yxz", "ref": lambda mag, pos: get_ref_rgeo(pos, mag, -1)},
    "phigeo": {"mode": "xyz", "ref": lambda mag, pos: get_ref_phi(pos, mag,  1)},
    "mphigeo": {"mode": "xyz", "ref": lambda mag, pos: get_ref_phi(pos, mag, -1)},
    "phism": {"mode": "xyz", "ref": lambda mag, pos: get_ref_phi(pos, mag,  1)},
    "mphism": {"mode": "xyz", "ref": lambda mag, pos: get_ref_phi(pos, mag, -1)},
    "ygsm": {"mode": "xyz", "ref": lambda mag, pos: get_ref_ygsm(len(get_data(mag).times))}
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
        logging.error("Need pos_var for %s", other_dim)
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
