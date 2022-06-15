import numpy as np


def slice2d_rlog(r, dr):
    """

    """

    # get log of radial boundaries
    rbottom = np.log10(r - 0.5*dr)
    rtop = np.log10(r + 0.5*dr)

    rrange = [np.nanmin(rbottom), np.nanmax(rtop)]
    span = rrange[1] - rrange[0]

    # shrink gap between (0, r_min] and normalize
    rbottom = rbottom - rrange[0]
    rbottom = rbottom/span

    rtop = rtop - rrange[0]
    rtop = rtop/span

    r = (rtop + rbottom)/2.0
    dr = (rtop - rbottom)

    return {'r': r, 'dr': dr}