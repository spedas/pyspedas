
import numpy as np
from pytplot import get_data

def data_exists(tvar):
    data = get_data(tvar)
    # multi-dimensional data returns a tuple, NRV variables return an ndarray
    if isinstance(data, tuple) or isinstance(data, np.ndarray):
        return True
    return False
