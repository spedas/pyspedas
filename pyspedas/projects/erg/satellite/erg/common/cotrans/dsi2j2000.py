import numpy as np
from pyspedas import tinterpol
from pytplot import tcrossp
from pytplot import tnormalize
from pyspedas.cotrans_tools.cotrans import cotrans
from pytplot import time_string
from pytplot import get_data, get_timespan, options, store_data, tplot_names

from ...orb.orb import orb
from .cart_trans_matrix_make import cart_trans_matrix_make
from .erg_interpolate_att import erg_interpolate_att


def dsi2j2000(name_in=None,
              name_out=None,
              no_orb=False,
              J20002DSI=False,
              noload=False):
    """
    This function transform a time series data between the DSI and J2000 coordinate systems

    Parameters:

        name_in : str
            input tplot variable to be transformed

        name_out : str
            Name of the tplot variable in which the transformed data is stored

        J20002DSI : bool
            Set to transform data from J2000 to DSI. If not set, it transforms data from DSI to J2000.

    Returns:
        None

    """
    if (name_in is None) or (name_in not in tplot_names(quiet=True)):
        print('Input of Tplot name is undifiend')
        return

    if name_out is None:
        print('Tplot name for output is undifiend')
        name_out = 'result_of_dsi2j2000'

    # prepare for transformed Tplot Variable
    reload = not noload
    dl_in = get_data(name_in, metadata=True)
    get_data_array = get_data(name_in)
    time_array = get_data_array[0]
    time_length = time_array.shape[0]
    dat = get_data_array[1]

    # Get the SGI axis by interpolating the attitude data
    dsiz_j2000 = erg_interpolate_att(name_in, noload=noload)['sgiz_j2000']

    # Sun direction in J2000
    sundir = np.array([[1., 0., 0.]]*time_length)

    if no_orb:
        store_data('sundir_gse', data={'x': time_array, 'y': sundir})

    else:  # Calculate the sun directions from the instantaneous satellite locations
        if reload:
            tr = get_timespan(name_in)
            orb(trange=time_string([tr[0] - 60., tr[1] + 60.]))
            tinterpol('erg_orb_l2_pos_gse', time_array)
            scpos = get_data('erg_orb_l2_pos_gse-itrp')[1]
            sunpos = np.array([[1.496e+08, 0., 0.]]*time_length)
            sundir = sunpos - scpos
            store_data('sundir_gse', data={'x': time_array, 'y': sundir})
            tnormalize('sundir_gse', newname='sundir_gse')

    # Derive DSI-X and DSI-Y axis vectors in J2000.
    # The elementary vectors below are the definition of DSI. The detailed relationship
    # between the spin phase, sun pulse timing, sun direction, and the actual subsolar point
    # on the spining s/c body should be incorporated into the calculation below.
    if reload:
        cotrans(name_in='sundir_gse', name_out='sundir_j2000',
                coord_in='gse', coord_out='j2000')
    sun_j2000 = get_data('sundir_j2000')
    dsiy = tcrossp(dsiz_j2000['y'], sun_j2000[1], return_data=True)
    dsix = tcrossp(dsiy, dsiz_j2000['y'], return_data=True)
    dsix_j2000 = {'x': time_array, 'y': dsix}
    dsiy_j2000 = {'x': time_array, 'y': dsiy}

    if not J20002DSI:
        print('DSI --> J2000')
        mat = cart_trans_matrix_make(
            dsix_j2000['y'], dsiy_j2000['y'], dsiz_j2000['y'])
        j2000x_in_dsi = np.dot(mat, np.array([1., 0., 0.]))
        j2000y_in_dsi = np.dot(mat, np.array([0., 1., 0.]))
        j2000z_in_dsi = np.dot(mat, np.array([0., 0., 1.]))
        mat = cart_trans_matrix_make(
            j2000x_in_dsi, j2000y_in_dsi, j2000z_in_dsi)
        dat_new = np.einsum("ijk,ik->ij", mat, dat)
    else:
        print('J2000 --> DSI')
        mat = cart_trans_matrix_make(
            dsix_j2000['y'], dsiy_j2000['y'], dsiz_j2000['y'])
        dat_new = np.einsum("ijk,ik->ij", mat, dat)

    store_data(name_out, data={'x': time_array, 'y': dat_new}, attr_dict=dl_in)
    options(name_out, 'ytitle', '\n'.join(name_out.split('_')))
