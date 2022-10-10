import numpy as np
from pytplot import get_data, store_data


def tcrossp(v1, v2, newname=None, return_data=False):
    """
    Calculates the cross product of two tplot varibles

    Input
    -------
        v1: str
            First tplot variable

        v2: str
            Second tplot variable

    Parameters
    -----------
        newname: str
            Name of the output variable

        return_data: bool
            Returns the data as an ndarray instead of creating a tplot variable

    Returns
    --------
        Name of the tplot variable
    """

    v1_data = None
    v2_data = None

    if not isinstance(v1, np.ndarray) and isinstance(v1, str):
        v1_data = get_data(v1)
        v1_name = v1

        if v1_data is not None:
            data1 = v1_data[1]
    else:
        v1_name = 'var1'
        data1 = v1

    if not isinstance(v2, np.ndarray) and isinstance(v2, str):
        v2_data = get_data(v2)
        v2_name = v2

        if v2_data is not None:
            data2 = v2_data[1]
    else:
        v2_name = 'var2'
        data2 = v2

    if newname is None:
        newname = v1_name + '_cross_' + v2_name

    cp = np.cross(data1, data2)

    if return_data:
        return cp
    else:
        out = cp
        if v2_data is None:
            if len(cp.shape) == 1:
                out = np.atleast_2d(cp)
            times = np.zeros(out.shape[0])
        else:
            times = v2_data[0]
        store_data(newname, data={'x': times, 'y': out})
        return newname
