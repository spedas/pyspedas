from pyspedas.cotrans_tools.minvar import minvar
from pytplot import get_data, store_data, time_double, time_string
import numpy as np


def minvar_matrix_make(in_var_name,
                       tstart=None,
                       tstop=None,
                       twindow=None,
                       tslide=None,
                       newname=None,
                       evname=None,
                       tminname=None,
                       tmidname=None,
                       tmaxname=None):
    """
    Use an input variable to make rotation matrices to rotate vectors into a minimum variance coordinate system.

    Parameters
    ----------
    in_var_name : str
        Name of the input variable that defines the coordinate system
    tstart: str
        Start time of the interval for which MVA matrices will be created.
    tend: str
        End time of the interval for which MVA matrices will be created.
    twindow: float
        Duration (in seconds) of the window used to produce each matrix. Defaults to
        entire time series.
    tslide: float
        Offset time (in seconds) between each successive window start time. Defaults to twindow/2.
        Set to 0 to produce only a single matrix.
    newname: str
        Name of the tplot variable to receive the MVA rotation matrices.
    evname: str
        Name of the tplot variable to receive the eigenvalues at each window.
    tminname: str
         Name of the tplot variable to receive the basis vectors for the minimum variance direction.
    tmidname: str
         Name of the tplot variable to receive the basis vectors for the intermediate variance direction.
    tmaxname: str
         Name of the tplot variable to receive the basis vectors for the maximum variance direction.

    Returns
    -------
    list of str
        The list of tplot variables produced.

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

    if (twindow is None) or (twindow > (stop_d - start_d)):
        twindow = stop_d - start_d

    # sets it to something large enough that it will only generate one
    # matrix in the default case
    if (tslide is None) or (tslide <= 0) :
        tslide = twindow / 2.0

    if newname is None:
        newname = in_var_name + '_mva_mat'

    current_d = start_d

    # Exact number of windows: always at least one, plus however many tslides fit in the space after the first window
    o_num = 1 + int((stop_d - start_d - twindow)/tslide)

    o_times = np.zeros(o_num)
    o_lams = np.zeros((o_num, 3))
    o_eigs = np.zeros((o_num, 3, 3))

    i = 0

    while current_d + twindow <= stop_d:
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

    o_d = {'x': o_times, 'y': o_eigs}

    out_vars = []

    saved = store_data(newname, data=o_d)

    if saved:
        out_vars.append(newname)

    if evname is not None:
        store_data(evname, data={'x': o_times, 'y': o_lams})
        out_vars.append(evname)

    if tminname is not None:
        store_data(tminname, data={'x': o_times, 'y': o_eigs[:, 2, :]})
        out_vars.append(tminname)

    if tmidname is not None:
        store_data(tmidname, data={'x': o_times, 'y': o_eigs[:, 1, :]})
        out_vars.append(tmidname)

    if tmaxname is not None:
        store_data(tmaxname, data={'x': o_times, 'y': o_eigs[:, 0, :]})
        out_vars.append(tmaxname)

    return out_vars
