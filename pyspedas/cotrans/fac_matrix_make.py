
import logging
import numpy as np

from pyspedas.analysis.tnormalize import tnormalize
from pyspedas.analysis.tcrossp import tcrossp

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

    fac_output = np.zeros((len(mag_data.times), 3, 3))
    fac_output[:, 0, :] = basis[0]
    fac_output[:, 1, :] = basis[1]
    fac_output[:, 2, :] = basis[2]

    store_data(newname, data={'x': mag_data.times, 'y': fac_output})

    return newname


