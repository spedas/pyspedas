import numpy as np
from scipy import interpolate

def interpol(
    data,
    data_times,
    out_times,
    fill_value="extrapolate"):

    """
    Interpolate data.

    Parameters
    ----------
    data: list of float
        Data array.
    data_times: list of float
        Time array.
    out_times: list of float
        Time array to interpolate to
    fill_value: str, optional
        Default: "extrapolate"

    Returns
    -------
    Interpolated data

    Examples
    --------
        import pyspedas
        >>> import pyspedas
        >>> x1 = [0, 4, 8, 12]
        >>> time1 = [pyspedas.time_float("2020-01-01") + i for i in x1]
        >>> x2=[0, 2, 4, 6, 8, 10, 12]
        >>> y1=[10, 20, 30, 40]
        >>> time2 = [pyspedas.time_float("2020-01-01") + i for i in x2]
        >>> pyspedas.interpol(y1, time1, time2)
    """
    if isinstance(data, list):
        data = np.array(data)

    if len(data.shape) == 2:
        out = np.empty((len(out_times), len(data[0, :])))
        for data_idx in np.arange(len(data[0, :])):
            interpfunc = interpolate.interp1d(data_times, data[:, data_idx], kind='linear', bounds_error=False, fill_value=fill_value)
            out[:, data_idx] = interpfunc(out_times)
        return out
    else:
        interpfunc = interpolate.interp1d(data_times, data, kind='linear', bounds_error=False, fill_value=fill_value)
        return interpfunc(out_times)
