import datetime
import numpy as np
from typing import Any

def is_timezone_aware(dt:Any)->bool:
    """
    Return True if input is a timezone-aware datetime object.

    Parameters:
    ----------
    dt: Any
    An object, or list or Numpy array of objects to be checked.
    If dt is a list or array, the first element is checked.

    Returns
    -------
    bool
    True if input is a timezone-aware datetime object, false otherwise.

    """
    if isinstance(dt, list) or isinstance(dt,np.ndarray):
        obj = dt[0]
    else:
        obj = dt

    if isinstance(obj,datetime.datetime):
        return obj.tzinfo is not None and obj.tzinfo.utcoffset(obj) is not None
    else:
        return False
