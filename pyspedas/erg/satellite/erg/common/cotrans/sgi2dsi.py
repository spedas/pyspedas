import numpy as np
from pytplot import get_data, options, store_data, tplot_names

from .erg_interpolate_att import erg_interpolate_att
from .vector_rotate import vector_rotate


def sgi2dsi(name_in=None,
            name_out=None,
            DSI2SGI=False,
            noload=False):
    """
    This transform a time series data between the SGI and DSI coordinate systems.

    Parameters:

        name_in : str
            input tplot variable to be transformed

        name_out : str
            Name of the tplot variable in which the transformed data is stored

        DSI2SGI : bool
             Set to transform data from DSI to SGI (despun coord --> spinning coord).
             If not set, it transforms data from SGI to DSI (spinning coord --> despun coord).

    Returns:
        None

    """
    if (name_in is None) or (name_in not in tplot_names(quiet=True)):
        print('Input of Tplot name is undifiend')
        return

    if name_out is None:
        print('Tplot name for output is undifiend')
        name_out = 'result_of_sgi2dsi'

    # prepare for transformed Tplot Variable
    reload = not noload
    dl_in = get_data(name_in, metadata=True)
    get_data_array = get_data(name_in)
    time_array = get_data_array[0]
    time_length = time_array.shape[0]
    dat = get_data_array[1]

    # Get the SGA and SGI axes by interpolating the attitude data
    interpolated_values = erg_interpolate_att(name_in, noload=noload)
    sgix2ssix_angle = interpolated_values['sgiz_j2000']['y'][:, 0]
    # [deg] Now the constant angle is used, which is not correct, though
    sgix2ssix_angle[:] = 90. + 21.6

    spperiod = interpolated_values['spinperiod']['y']
    spphase = interpolated_values['spinphase']['y']
    rot_axis = np.array([[0., 0., 1.]]*time_length)

    # SGI --> DSI (despin)
    if not DSI2SGI:
        print('SGI --> DSI')
        coor_out = 'dsi'
        rotated_vector = vector_rotate(x0=dat[:, 0], y0=dat[:, 1], z0=dat[:, 2],
                                       nx=rot_axis[:, 0], ny=rot_axis[:, 1], nz=rot_axis[:, 2],
                                       theta=-sgix2ssix_angle + spphase)
    else:  # DSI --> SGI (spin)
        print('DSI --> SGI')
        coord_out = 'sgi'
        rotated_vector = vector_rotate(x0=dat[:, 0], y0=dat[:, 1], z0=dat[:, 2],
                                       nx=rot_axis[:, 0], ny=rot_axis[:,1], nz=rot_axis[:, 2],
                                       theta=-1.*(-sgix2ssix_angle + spphase))

    store_data(name_out, data={'x': time_array,
               'y': rotated_vector}, attr_dict=dl_in)
    options(name_out, 'ytitle', '\n'.join(name_out.split('_')))
