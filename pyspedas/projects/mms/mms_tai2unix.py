import datetime
import numpy as np
from pyspedas.utilities.leap_seconds import load_leap_table


def mms_tai2unix(values):
    """
    Converts MMS timestamps in TAI to unix timestamps

    Based on Mitsuo Oka's IDL code with the same name.

    Input
    ---------
        values: float, list of floats or np.ndarray
            Time values in TAI

    Returns
    ---------
        Array of time values as unix times

    """
    if not isinstance(values, list) and not isinstance(values, np.ndarray):
        values = [values]
    table = load_leap_table()
    tai_minus_unix = 378691200.0
    juls = np.array(table['juls'])
    values_juls = np.array(values)/86400.0 + datetime.date(1958, 1, 1).toordinal() + 1721424.5
    out = np.zeros(len(values))
    for idx, value in enumerate(values_juls):
        loc_greater = np.argwhere(value > juls).flatten()
        if len(loc_greater) == 0:
            continue
        last_loc = loc_greater[len(loc_greater)-1]
        current_leap = float(table['leaps'][last_loc])
        tinput_1970 = values[idx] - tai_minus_unix
        out[idx] = tinput_1970 - current_leap
    return out

from astropy.time import Time

MMS_TAI_MINUS_UNIX_TAI = 378691200.0

def mms_unix2tai(values):
    """
    Convert UTC/POSIX unix timestamps to MMS TAI seconds since 1958-01-01 TAI.
    """
    scalar = np.isscalar(values)
    arr = np.atleast_1d(values).astype(float)

    t = Time(arr, format="unix", scale="utc")
    out = t.tai.unix_tai + MMS_TAI_MINUS_UNIX_TAI

    return out[0] if scalar else np.asarray(out)