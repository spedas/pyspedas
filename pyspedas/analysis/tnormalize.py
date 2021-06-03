
from pytplot import get_data, store_data

def tnormalize(variable, newname=None, return_data=False):
    """


    """
    data_in = get_data(variable)
    metadata_in = get_data(variable, metadata=True)

    n = np.sqrt(np.nansum(data_in[1]**2, axis=1))

    # to do element-wise division, the magnitude needs to be repeated for each component
    norm_reshaped = np.reshape(n, [len(data_in[0]), 1])
    norm_mag = np.repeat(norm_reshaped, len(data_in[1][0, :]), axis=1)

    data_norm = data_in[1]/norm_mag

    if newname is None:
        newname = variable + '_normalized'

    store_data(newname, data={'x': data_in[0], 'y': data_norm}, attr_dict=metadata_in)

    if return_data:
        return data_norm
    else:
        return newname

