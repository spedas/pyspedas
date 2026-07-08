import numpy as np
from pyspedas.utilities.tai2unix import tai2unix
from pyspedas.utilities.unix2tai import unix2tai


def _as_float_array(values):
    return np.atleast_1d(np.asarray(values, dtype=float))


def mms_tai2unix(values):
    """
    Converts MMS timestamps in TAI to unix timestamps.

    This MMS-specific function preserves the historical return shape while
    delegating leap-second handling to the generic PySPEDAS converter.

    Input
    ---------
        values: float, list of floats or np.ndarray
            Time values in TAI

    Returns
    ---------
        Array of time values as unix times

    """
    return np.asarray(tai2unix(_as_float_array(values)))


def mms_unix2tai(values):
    """
    Convert UTC/POSIX unix timestamps to MMS TAI seconds since 1958-01-01 TAI.
    """
    scalar = np.isscalar(values)
    out = np.asarray(unix2tai(_as_float_array(values)))

    return out[0] if scalar else np.asarray(out)
