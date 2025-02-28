
import logging
import numpy as np

from pyspedas import tinterpol

from pytplot import tnormalize
from pytplot import tcrossp

from pytplot import get_data, store_data

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def xgse(mag_temp):
    """
    Generates the 'xgse' transformation matrix
    """
    mag_data = get_data(mag_temp)

    # xaxis of this system is X of the gse system. Z is mag field
    x_axis = np.zeros((len(mag_data.times), 3))
    x_axis[:, 0] = 1

    # create orthonormal basis set
    z_basis = tnormalize(mag_temp, return_data=True)
    y_basis = tcrossp(z_basis, x_axis, return_data=True)
    y_basis = tnormalize(y_basis, return_data=True)
    x_basis = tcrossp(y_basis, z_basis, return_data=True)

    return (x_basis, y_basis, z_basis)

def rgeo(mag_var_name, pos_var_name):
    """
    Generates the 'Rgeo' transformation matrix using the radial position vector.
    Rgeo is assumed to be in GEI coordinates (positive radially outwards).
    The transformation sets:
        Z-axis = normalized magnetic field,
        Y-axis = B x Rgeo (eastward),
        X-axis = Y x B.
    """
    # Retrieve and validate the position data.
    pos_data = get_data(pos_var_name)
    if pos_data is None:
        logging.error("Error reading tplot variable: " + pos_var_name)
        return None

    if pos_data.y.ndim != 2 or pos_data.y.shape[1] != 3:
        logging.error("Position data must be an Nx3 array")
        return None

    # Interpolate the position data onto the magnetic field time stamps
    tinterpol(names=pos_var_name, interp_to=mag_var_name, method='linear',
              newname=None, suffix='-itrp')
    pos_interp_var = pos_var_name + '-itrp'
    pos_interp_data = get_data(pos_interp_var)
    if pos_interp_data is None:
        logging.error("Interpolation failed for " + pos_var_name)
        return None

    # Normalize the interpolated position vector (Rgeo)
    rgeo_normalized = pos_interp_data.y
    norms = np.linalg.norm(rgeo_normalized, axis=1, keepdims=True)
    norms[norms == 0] = 1  # avoid division by zero
    rgeo_normalized = rgeo_normalized / norms

    # Retrieve and normalize the magnetic field data (Z-axis)
    z_basis = tnormalize(mag_var_name, return_data=True)
    if z_basis is None:
        logging.error("Failed to normalize magnetic field vector")
        return None

    # Compute Y-axis as the cross product: B x Rgeo
    y_basis = np.cross(z_basis, rgeo_normalized)
    norms_y = np.linalg.norm(y_basis, axis=1, keepdims=True)
    norms_y[norms_y == 0] = 1
    y_basis_normalized = y_basis / norms_y

    # Compute X-axis as the cross product: Y x B
    x_basis = np.cross(y_basis_normalized, z_basis)

    return (x_basis, y_basis_normalized, z_basis)


def fac_matrix_make(mag_var_name, other_dim='Xgse', pos_var_name=None, newname=None):
    """
    Generates a field aligned coordinate transformation matrix
    from an input B vector array(and sometimes a position vector array)
    then stores it in a tplot variable

    Input
    ----------
        mag_var_name: str
            tplot variable containing the B-field data

    Parameters
    ----------
        other_dim: str, optional
            The second axis for the field aligned coordinate system (default: Xgse)

        pos_var_name: str, optional
            tplot variable containing the spacecraft position data

        newname: str, optional
            Name of the output tplot variable containing the FAC transformation matrices

    Returns
    ----------

        Name of the tplot variable created.

    """

    mag_data = get_data(mag_var_name)

    if mag_data is None:
        logging.error('Error reading tplot variable: ' + mag_var_name)
        return

    if newname is None:
        newname = mag_var_name + '_fac_mat'

    other_dim = other_dim.lower()

    if other_dim == 'xgse':
        basis = xgse(mag_var_name)
    elif other_dim == 'rgeo':
        if pos_var_name is None:
            logging.error("pos_var_name must be provided for Rgeo coordinate transformation")
            return None
        basis = rgeo(mag_var_name, pos_var_name)
    else:
        logging.error("Unsupported coordinate transformation: " + other_dim)
        return None

    fac_output = np.zeros((len(mag_data.times), 3, 3))
    fac_output[:, 0, :] = basis[0]
    fac_output[:, 1, :] = basis[1]
    fac_output[:, 2, :] = basis[2]

    store_data(newname, data={'x': mag_data.times, 'y': fac_output})

    return newname


