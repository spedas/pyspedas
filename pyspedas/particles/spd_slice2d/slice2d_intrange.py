import numpy as np


def slice2d_intrange(dists, trange):
    """
    Retrieves the indices of all samples in the specified time range from a particle distribution list.

    Input
    ------
        dists: list of particle distributions

        trange: array of float
            Time range to find distributions in; must be in unix time

    Returns
    -------
        numpy array containing the indices that fall within the specified trange
    """
    out = []

    for idx, dist in enumerate(dists):
        time = dist['start_time'] + (dist['end_time']-dist['start_time'])/2.0
        if trange[0] <= time <= trange[1]:
            out.append(idx)

    return np.array(out)
