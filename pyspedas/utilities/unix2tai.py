import numpy as np
from cdflib import cdfepoch
from numpy.typing import ArrayLike

def unix2tai(tinput:float | ArrayLike)->float|ArrayLike:
    """
    Convert Unix timestamps to TAI timestamps

    Unix timestamps are referenced to epoch 1970-01-01, and do not contain leap seconds.
    TAI timestamps are referenced to epoch 1958-01-01, and include leap seconds.

    Input and output units are seconds since epoch,

    Internally, the CDF library is used to manage the TAI-UTC offsets.  Prior to 1972,
    the UTC-TAI offset will not necessarily be an integer number of seconds.

    Parameters
    ----------
    tinput: ArrayLike
        A scalar or array of Unix timestamps

    Returns
    -------
    ArrayLike
        A scalar or array of floating point TAI timestamps

    Examples
    ---------

    >>> from pyspedas import time_string, time_double, unix2tai
    >>> unix_time = time_double('1970-01-01/12:00:00')
    >>> tai_time = unix2tai(unix_time)
    >>> print(tai_time)
    378734408.001378

    """

    # Offset of TAI epoch from TT2000 epoch, in nanoseconds
    tai_epoch_const_ns = -1325419167816000000
    # Convert the Unix time to a TT2000 value in nanoseconds
    tt2000_nsec = cdfepoch.timestamp_to_tt2000(tinput)
    # Apply the offset from TT2000 to TAI
    tai_ns = tt2000_nsec - tai_epoch_const_ns
    # Convert to seconds
    tai_sec = tai_ns/1000000000.0
    # Return a scalar if the input was scalar, otherwise return an array
    if np.isscalar(tinput):
        return tai_sec[0]
    return tai_sec
