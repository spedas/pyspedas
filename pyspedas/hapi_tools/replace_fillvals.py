import logging
import numpy as np

def replace_fillvals(data_array, fillval, varname, param_type):
    """
    Replace fill values in data_array with NaNs.  If fillval is an array, each entry applies to the correspondiing data_array elements.

    Parameters
    ----------
    data_array: ndarray
        Input data
    fillval: int or float or list or ndarray
        Fill values to replace with NaN in corresponding elements of data_array.
    varname: str
        The variable currently being processed (for log messages)
    param_type: str
        Data type as returned by hapi server.  Integer data is 0-filled, while floating point data is nan-filled.

    Returns
    -------
    None

    Notes
    -----
    If fillval is an array, its shape must match that of the data array values (after removing the leading dimension for
    the timestamps.  Each element of fillval is searched for and replaced independently, in the correspondina array positions of the data array.

    """

    if param_type == 'integer':
        replacement = 0
    else:
        replacement = np.nan

    if np.isscalar(fillval):
        # Scalar fillval, replace scalar fillval everywhere
        idx = np.where(data_array == fillval)
        data_array[idx] = replacement
    else:
        logging.warning(f'replace_fillvals: Fillval for {varname} is a array-valued, which may not be standard-compliant.')
        # Array fillval, check that shapes match, and replace data_array values matching corresponding fillvals
        npfillval=np.array(fillval)
        npfillval_shape = npfillval.shape
        data_array_shape = data_array.shape

        if npfillval_shape != data_array[0].shape:
            logging.error(f'replace_fillvals: Fillval shape {str(npfillval_shape)} not compatible with data_array shape {str(data_array_shape)}')
            return
        npfillval_reshaped = npfillval.reshape(-1)
        data_reshaped = data_array.reshape(data_array_shape[0],-1)
        for i in range(len(npfillval_reshaped)):
            idx = np.where(data_reshaped[:,i] == npfillval_reshaped[i])
            data_reshaped[idx,i] = replacement




