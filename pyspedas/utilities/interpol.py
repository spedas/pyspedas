import numpy as np
from scipy import interpolate

def interpol(data, data_times, out_times):
    '''
    Simple wrapper around scipy's interp1d that allows you to linearly interpolate data from 
    one set of times to another set of times

    '''

    if isinstance(data, list):
        data = np.array(data)

    if len(data.shape) == 2:
        out = np.empty((len(out_times), len(data[0, :])))
        for data_idx in np.arange(len(data[0, :])):
            interpfunc = interpolate.interp1d(data_times, data[:, data_idx], kind='linear', bounds_error=False, fill_value='extrapolate')
            out[:, data_idx] = interpfunc(out_times)
        return out
    else:
        interpfunc = interpolate.interp1d(data_times, data, kind='linear', bounds_error=False, fill_value='extrapolate')
        return interpfunc(out_times)