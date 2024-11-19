import numpy as np
from pytplot import get_data, options, store_data, tplot_names

from .cart_trans_matrix_make import cart_trans_matrix_make
from .erg_interpolate_att import erg_interpolate_att


def sga2sgi(name_in=None,
            name_out=None,
            SGI2SGA=False,
            noload=False):
    """
    This transform a time series data between the SGA and SGI coordinate systems.

    Parameters:

        name_in : str
            input tplot variable to be transformed

        name_out : str
            Name of the tplot variable in which the transformed data is stored

        SGI2SGA : bool
              Set to transform data from SGI to SGA. If not set, it transforms data from SGA to SGI.

    Returns:
        None

    """
    if (name_in is None) or (name_in not in tplot_names(quiet=True)):
        print('Input of Tplot name is undifiend')
        return

    if name_out is None:
        print('Tplot name for output is undifiend')
        name_out = 'result_of_sga2sgi'

    get_data_vars = get_data(name_in)
    dl_in = get_data(name_in, metadata=True)
    time_array = get_data_vars[0]
    time_length = time_array.shape[0]
    dat = get_data_vars[1]

    # Get the SGA and SGI axes by interpolating the attitude data
    interpolated_values = erg_interpolate_att(name_in, noload=noload)
    sgix = interpolated_values['sgix_j2000']['y']
    sgiy = interpolated_values['sgiy_j2000']['y']
    sgiz = interpolated_values['sgiz_j2000']['y']
    sgax = interpolated_values['sgax_j2000']['y']
    sgay = interpolated_values['sgay_j2000']['y']
    sgaz = interpolated_values['sgaz_j2000']['y']

    if not SGI2SGA:
        print('SGA --> SGI')
        coord_out = 'sgi'

        # Transform SGI-X,Y,Z axis unit vectors in J2000 to those in SGA
        mat = cart_trans_matrix_make(sgax, sgay, sgaz)
        sgix_in_sga = np.einsum("ijk,ik->ij", mat, sgix)
        sgiy_in_sga = np.einsum("ijk,ik->ij", mat, sgiy)
        sgiz_in_sga = np.einsum("ijk,ik->ij", mat, sgiz)

        # Now transform the given vector in SGA to those in SGI
        mat = cart_trans_matrix_make(sgix_in_sga, sgiy_in_sga, sgiz_in_sga)
        dat_new = np.einsum("ijk,ik->ij", mat, dat)

    else:
        print('SGI --> SGA')
        coord_out = 'sga'

        # Transform SGA-X,Y,Z axis unit vectors in J2000 to those in SGI
        mat = cart_trans_matrix_make(sgix, sgiy, sgiz)
        sgax_in_sgi = np.einsum("ijk,ik->ij", mat, sgax)
        sgay_in_sgi = np.einsum("ijk,ik->ij", mat, sgay)
        sgaz_in_sgi = np.einsum("ijk,ik->ij", mat, sgaz)

        # Now transform the given vector in SGI to those in SGA
        mat = cart_trans_matrix_make(sgax_in_sgi, sgay_in_sgi, sgaz_in_sgi)
        dat_new = np.einsum("ijk,ik->ij", mat, dat)

    # Store the converted data in a tplot variable
    store_data(name_out, data={'x': time_array, 'y': dat_new}, attr_dict=dl_in)
    options(name_out, 'ytitle', '\n'.join(name_out.split('_')))
