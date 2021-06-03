
import numpy as np
from pytplot import get_data, store_data

def tcrossp(v1, v2, newname=None, return_data=False):
    """

    """

    if not isinstance(v1, np.ndarray) and isinstance(v1, str):
        v1_data = get_data(v1)
        v1_name = v1

        if v1_data is not None:
            time1 = v1_data[0]
            data1 = v1_data[1]
    else:
        v1_name = 'var1'
        data1 = v1


    if not isinstance(v2, np.ndarray) and isinstance(v2, str):
        v2_data = get_data(v2)
        v2_name = v2

        if v2_data is not None:
            time2 = v2_data[0]
            data2 = v2_data[1]
    else:
        v2_name = 'var2'
        data2 = v2

    if newname is None:
        newname = v1_name + '_cross_' + v2_name

    cp = np.cross(v1_data, v2_data)

    if return_data:
        return cp
    else:
        store_data(newname, data={'x': v2_data[0], 'y': cp})

