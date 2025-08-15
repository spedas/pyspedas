import logging
import numpy as np
import pyspedas
from pyspedas import tinterpol
from pyspedas.tplot_tools import get_data, store_data, tnames
from pyspedas.cotrans_tools.quaternions import qtom, mtoq, qslerp
from pyspedas.cotrans_tools.matrix_array_lib import ctv_verify_mats, ctv_left_mats, ctv_swap_hands
from copy import deepcopy
from .rotmat_get_coords import rotmat_get_coords


def tvector_rotate(mat_var_in, vec_var_in, newname=None):
    """
    Rotates tplot vector data by a set of coordinate ransformation matrices and outputs tplot variables.
    This is designed mainly for use with fac_matrix_make, 
    but can be used for more general purposes.  The input variable containing the
    rotation matrices is automatically interpolated to the timestamps in the vec_var_in variables,
    using the qslerp (Quaternion Spherical Linear intERPolation) routine from the PySPEDAS quaternion
    library.

    Parameters
    -----------
        mat_var_in: str
            Tplot variable containing the transformation matrices

        vec_var_in: str or list of str
            Tplot variables to be transformed

        newname: str or list of str
            Name of the output tplot variables

    Returns
    ---------
        Names of the variables created.

    """

    if tnames(mat_var_in) == []:
        logging.error('Transformation requires the matrix variable to be set to a valid tplot variable.')
        return

    if tnames(vec_var_in) == []:
        logging.error('Transformation requires the vector variables to be set to a valid tplot variable.')
        return

    vec_var_in = tnames(vec_var_in)

    if newname is None:
        newname = [vec_var + '_rot' for vec_var in vec_var_in]

    if not isinstance(newname, list):
        newname = [newname]

    if len(newname) != len(vec_var_in):
        logging.error('Length of newname keyword should match the length of vec_var_in')
        return

    out_names = []

    rot_in_coords, rot_out_coords = rotmat_get_coords(mat_var_in)

    # loop over the vectors
    for vec_var, new_var in zip(vec_var_in, newname):
        vec_data = get_data(vec_var)
        in_vec_metadata = get_data(vec_var, metadata=True)
        out_vec_metadata = deepcopy(in_vec_metadata)
        mat_data = get_data(mat_var_in)
        m_d_y = mat_data.y

        in_vec_coords = pyspedas.get_coords(vec_var)
        if rot_in_coords is not None and (in_vec_coords is None or in_vec_coords.lower() != rot_in_coords.lower()):
            logging.warning(f"Input vector {vec_var} coordinate system {in_vec_coords} does not match rotation matrix {mat_var_in} input coordinate system {rot_in_coords}")


        if not np.array_equal(vec_data.times, mat_data.times) and len(mat_data.times) != 1:
            verify_check = ctv_verify_mats(mat_data.y)

            is_left_mat = ctv_left_mats(mat_data.y)

            # left-handed matrices can mess up qslerping
            if is_left_mat:
                q_in = mtoq(ctv_swap_hands(mat_data.y))
            else:
                q_in = mtoq(mat_data.y)

            # interpolate quaternions
            q_out = qslerp(q_in, mat_data.times, vec_data.times)

            # turn quaternions back into matrices
            m_d_y = qtom(q_out)

            if is_left_mat:
                m_d_y = ctv_swap_hands(m_d_y)


        vec_fac = np.zeros((len(vec_data.times), len(vec_data.y[0, :])))

        for i in range(0, len(vec_data.times)):
            if m_d_y.shape[0] == 1:  # only a single matrix
                matrix = m_d_y[0, :, :]
            else:
                matrix = m_d_y[i, :, :]

            vec_fac[i, :] = matrix @ vec_data.y[i, :]

        saved = store_data(new_var, data={'x': vec_data.times, 'y': vec_fac}, attr_dict=out_vec_metadata)
        if rot_out_coords is not None:
            pyspedas.set_coords(new_var, rot_out_coords)

        if saved:
            out_names.append(new_var)

    return out_names
