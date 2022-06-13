import numpy as np


def slice2d_intrange(dists, trange):
    """

    """
    out = []
    for idx, dist in enumerate(dists):
        time = dist['start_time'] + (dist['end_time']-dist['start_time'])/2.0
        if trange[0] <= time <= trange[1]:
            out.append(idx)
    return np.array(out)
