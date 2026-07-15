from cdflib import cdfepoch
import numpy as np
from numpy.typing import ArrayLike
from pyspedas import time_string

def tai2unix(tinput:float | ArrayLike)->float|ArrayLike:
    """
    Convert TAI timestamps to Unix timestamps

    Unix timestamps are referenced to epoch 1970-01-01, and do not contain leap seconds.
    TAI timestamps are referenced to epoch 1958-01-01, and include leap seconds

    Input and output units are seconds since epoch,

    Internally, the CDF library is used to manage the TAI-UTC offsets.  Prior to 1972,
    the UTC-TAI offset will not necessarily be an integer number of seconds.

    Parameters
    ----------
    tinput: ArrayLike
        A scalar or array of TAI timestamps

    Returns
    -------
    ArrayLike
        A scalar or array of floating point Unix timestamps

    Examples
    ---------

    >>> from pyspedas import time_string, time_double, tai2unix
    >>> tai_time = 43200.0
    >>> unix_time = tai2unix(tai_time)
    >>> time_string(unix_time)
    '1958-01-01 12:00:00.000000'

    """
    # Offset of TAI epoch from TT2000 epoch, in nanoseconds
    scalar_flag = np.isscalar(tinput)
    if scalar_flag:
        tinput=np.array(tinput)
    elif isinstance(tinput,list):
        tinput=np.array(tinput)

    tai_epoch_const_ns = np.int64(-1325419167816000000)
    # Convert TAI input to nanoseconds and apply TT2000 offset
    tt2000 = np.int64(tinput*1000000000) + tai_epoch_const_ns
    # Convert the TT@000 value in nanoseconds to Unix time in seconds
    # Some values may fail due to a cdflib bug.  We need to iterate through one by one, and
    # catch any failures.
    if scalar_flag:
        tt2000=[tt2000]
    unix = np.zeros(len(tt2000),dtype=np.float64)
    for i in range(len(tt2000)):
        try:
            unix[i] = cdfepoch.unixtime(tt2000[i])
        except ValueError:
            # These failures are usually due to cdflib trying to make a datetime with min=60 or sec=60.
            # If we subtract 1d9 nanoseconds from the input, then add one second back to the converted value,
            # the conversion should be correct.
            unix[i] = cdfepoch.unixtime(tt2000[i]-1000000000)
            unix[i] += 1.0
            print(f"cdflib had trouble converting TT2000 value {tt2000[i]}  to unix, final result {time_string(unix[i])}")
    if scalar_flag:
        return unix[0]
    else:
        return unix
