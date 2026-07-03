from cdflib import cdfepoch
import numpy as np
import numpy.typing as npt
from numpy.typing import ArrayLike

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
    tai_epoch_const_ns = -1325419167816000000
    # Convert TAI input to nanoseconds and apply TT2000 offset
    tt2000 = np.int64(tinput*1000000000 + tai_epoch_const_ns)
    # Convert the TT@000 value in nanoseconds to Unix time in seconds
    unix = cdfepoch.unixtime(tt2000)
    return unix
