
import numpy as np
from pyspedas import tnames
from pytplot import get_data, store_data

def tvector_rotate(mat_var_in, vec_var_in, newname=None):
    """
    Rotates array data by a set of coordinate
    transformation matrices and outputs tplot variables.
    This is designed mainly for use with fac_matrix_make, 
    but can be used for more general purposes.

    Input
    ------
        mat_var_in: str
            Tplot variable containing the transformation matrices

        vec_var_in: str or list of str
            Tplot variables to be transformed

    Parameters
    ----------
        newname: str or list of str
            Name of the output tplot variables

    Returns
    ---------
        Names of the variables created.

    """

    if tnames(mat_var_in) == []:
        print('Transformation requires the matrix variable to be set to a valid tplot variable.')
        return

    if tnames(vec_var_in) == []:
        print('Transformation requires the vector variables to be set to a valid tplot variable.')
        return

    vec_var_in = tnames(vec_var_in)

    if newname is None:
        newname = [vec_var + '_rot' for vec_var in vec_var_in]

    if not isinstance(newname, list):
        newname = [newname]

    if len(newname) != len(vec_var_in):
        print('Length of newname keyword should match the length of vec_var_in')
        return

    out_names = []

    mat_data = get_data(mat_var_in)

    # loop over the vectors
    for vec_var, new_var in zip(vec_var_in, newname):
        vec_data = get_data(vec_var)
        vec_metadata = get_data(vec_var, metadata=True)

        vec_fac = np.zeros((len(vec_data.times), len(vec_data.y[0, :])))

        for i in range(0, len(vec_data.times)):
            vec_fac[i, :] = mat_data.y[i, :, :] @ vec_data.y[i, :]

        saved = store_data(new_var, data={'x': vec_data.times, 'y': vec_fac}, attr_dict=vec_metadata)

        if saved:
            out_names.append(new_var)

    return out_names
