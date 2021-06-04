
import numpy as np
from pytplot import get_data, store_data

def tnormalize(variable, newname=None, return_data=False):
    """


    """
    metadata_in = {}
    if isinstance(variable, str):
        data_in = get_data(variable)
        metadata_in = get_data(variable, metadata=True)
        data = data_in[1]
        times = data_in[0]
    else:
        data = np.atleast_2d(variable)
        times = np.zeros(data.shape[0])

    n = np.sqrt(np.nansum(data**2, axis=1))

    # to do element-wise division, the magnitude needs to be repeated for each component
    norm_reshaped = np.reshape(n, [len(times), 1])
    norm_mag = np.repeat(norm_reshaped, len(data[0, :]), axis=1)

    data_norm = data/norm_mag

    if return_data:
        return data_norm
    else:
        if newname is None:
            newname = variable + '_normalized'
        store_data(newname, data={'x': times, 'y': data_norm}, attr_dict=metadata_in)
        return newname

