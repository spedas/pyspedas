from pyspedas import time_double
from pyspedas.cotrans.minvar import minvar
from pytplot import get_data, store_data
import numpy as np


def minvar_matrix_make(in_var_name,
                       tstart=None,
                       tstop=None,
                       twindow=None,
                       tslide=None,
                       newname=None):
    """

    """
    data = get_data(in_var_name)

    if tstart is None:
        start_d = data.times[0]
    else:
        start_d = time_double(tstart)

    if tstop is None:
        stop_d = data.times[-1]
    else:
        stop_d = time_double(tstop)

    if twindow is None:
        twindow = stop_d - start_d

    # sets it to something large enough that it will only generate one
    # matrix in the default case
    if tslide is None:
        tslide = twindow / 2.0

    if newname is None:
        newname = in_var_name + '_mva_mat'

    current_d = start_d

    # estimate the number of output matrices to generate temporary storage
    if tslide != 0:
        o_num = (stop_d - start_d) / tslide
    else:
        o_num = 1

    o_num = int(o_num)

    o_times = np.zeros(o_num)
    o_lams = np.zeros((o_num, 3))
    o_eigs = np.zeros((o_num, 3, 3))

    i = 0

    while current_d + twindow <= stop_d + twindow:
        if i >= o_num:
            break
        # output time for the mva matrix is the midpoint time for the interval
        o_times[i] = current_d + twindow / 2.0

        idx = np.argwhere((data.times >= current_d) & (data.times <= (current_d + twindow))).flatten()

        if len(idx) == 0:
            current_d += tslide
            i += 1
            continue

        in_data = data.y[idx, :]

        try:
            out = minvar(in_data)
        except np.linalg.LinAlgError:
            current_d += tslide
            i += 1
            continue

        if out is not None:
            v_rot, o_eig, o_lam = out
            o_lams[i, :] = o_lam
            o_eigs[i, :, :] = o_eig.transpose()

        i += 1
        current_d += tslide

        if tslide == 0:
            break

    if len(data) > 2:
        o_d = {'x': o_times[:-1], 'y': o_eigs[0:-1, :, :], 'v': data.v}
    else:
        o_d = {'x': o_times[:-1], 'y': o_eigs[0:-1, :, :]}

    out_vars = []

    saved = store_data(newname, data=o_d)

    if saved:
        out_vars.append(newname)

    return out_vars
