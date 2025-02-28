import logging
import numpy as np

from pyspedas import tinterpol

from pytplot import tnormalize
from pytplot import tcrossp

from pytplot import get_data, store_data

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
        logging.error(f"Interpolation failed for {pos_var_name}")
    return interp_data

def normalize_vectors(vectors):
    """Normalize an array of vectors along the last axis."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1  # avoid division by zero
    return vectors / norms

def xgse(mag_var_name):
    """
    Generates the 'xgse' transformation matrix
    """
    mag_data = get_data(mag_var_name)
    if mag_data is None:
        return None

    # xaxis of this system is X of the gse system. Z is mag field
    N = len(mag_data.times)
    x_axis = np.zeros((N, 3))
    x_axis[:, 0] = 1

    # create orthonormal basis set
    z_basis = tnormalize(mag_var_name, return_data=True)
    if z_basis is None:
        return None

    y_basis = tcrossp(z_basis, x_axis, return_data=True)
    y_basis = tnormalize(y_basis, return_data=True)
    x_basis = tcrossp(y_basis, z_basis, return_data=True)

    return (x_basis, y_basis, z_basis)

def rgeo(mag_var_name, pos_var_name):
    """
    Build FAC basis for the 'rgeo' option.
    Rgeo is the normalized (interpolated) position vector.
    Z-axis = normalized magnetic field.
    Y-axis = B x Rgeo.
    X-axis = Y x B.
    """
    pos_data = validate_vector_data(pos_var_name)
    if pos_data is None:
        return None

    # Interpolate position data onto the magnetic field's time grid.
    interp_pos_data = interpolate_position(pos_var_name, mag_var_name)
    if interp_pos_data is None:
        return None

    # Normalize the interpolated position vector.
    rgeo_norm = normalize_vectors(interp_pos_data.y)

    # Z-axis: normalized magnetic field.
    z_basis = tnormalize(mag_var_name, return_data=True)
    if z_basis is None:
        return None

    # Y-axis: cross(B, Rgeo)
    y_basis = tcrossp(z_basis, rgeo_norm, return_data=True)
    y_basis = normalize_vectors(y_basis)

    # X-axis: cross(Y, B)
    x_basis = tcrossp(y_basis, z_basis, return_data=True)
    return (x_basis, y_basis, z_basis)

# === Dictionary Mapping Option Strings to Functions ===

# COORD_FUNCTIONS = {
#     "xgse": xgse,
#     "rgeo": rgeo,
#     "mrgeo": lambda mag, pos, probe=None: rgeo(mag, pos, sign=-1),
#     "phigeo": phigeo,
#     "mphigeo": lambda mag, pos, probe=None: phigeo(mag, pos, probe, sign=-1),
#     "phism": phism,
#     "mphism": lambda mag, pos, probe=None: phism(mag, pos, probe, sign=-1),
#     "ygsm": ygsm,
#     "zdsl": zdsl,
# }

COORD_FUNCTIONS = {
    "xgse": xgse,
    "rgeo": rgeo,
    "mrgeo": lambda mag, pos, probe=None: rgeo(mag, pos, sign=-1)
}


# === Main Interface ===
def fac_matrix_make(mag_var_name, other_dim='Xgse', pos_var_name=None, newname=None, probe=None):
    """
    Generate a field-aligned coordinate (FAC) transformation matrix from the given magnetic
    field B and (if required) position data, and store it in a tplot variable.

    Parameters
    ----------
    mag_var_name : str
        tplot variable containing the magnetic field data.
    other_dim : str, optional
        The coordinate system option. Must be one of:
        ['xgse','rgeo','mrgeo','phigeo','mphigeo','phism','mphism','ygsm','zdsl'].
        (Default is "xgse".)
    pos_var_name : str, optional
        tplot variable containing the spacecraft position data.
        Required for all options except "xgse" and "zdsl".
    newname : str, optional
        Name of the output tplot variable. Defaults to mag_var_name + "_fac_mat".
    probe : str, optional
        Probe identifier for coordinate conversions when needed.

    Returns
    -------
    str or None
        The name of the output tplot variable containing the FAC matrix,
        or None if an error occurs.
    """

    mag_data = get_data(mag_var_name)

    if mag_data is None:
        logging.error('Error reading tplot variable: ' + mag_var_name)
        return

    if newname is None:
        newname = mag_var_name + '_fac_mat'

    other_dim = other_dim.lower()

    basis_fn = COORD_FUNCTIONS.get(other_dim)
    if basis_fn is None:
        logging.error(f"Unsupported coordinate transformation: {other_dim}")
        return None

    if other_dim in ["rgeo", "mrgeo", "phigeo", "mphigeo", "phism", "mphism", "ygsm"] and pos_var_name is None:
        logging.error(f"pos_var_name must be provided for {other_dim} coordinate transformation")
        return None

    # Call the corresponding basis function.
    if other_dim in ["phigeo", "mphigeo", "phism", "mphism", "ygsm"]:
        basis = basis_fn(mag_var_name, pos_var_name, probe=probe)
    elif other_dim in ["rgeo", "mrgeo"]:
        basis = basis_fn(mag_var_name, pos_var_name)
    else:
        basis = basis_fn(mag_var_name)

    if basis is None:
        return None

    N = len(mag_data.times)
    fac_matrix = np.zeros((N, 3, 3))
    fac_matrix[:, 0, :] = basis[0]
    fac_matrix[:, 1, :] = basis[1]
    fac_matrix[:, 2, :] = basis[2]


    store_data(newname, data={'x': mag_data.times, 'y': fac_matrix})

    return newname


