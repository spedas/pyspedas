
import numpy as np
import pytplot

def data_exists(tvar):
    """
    Checks if a tplot variable exists
    """
    if tvar in pytplot.data_quants.keys():
        data = pytplot.get_data(tvar)
        # multi-dimensional data returns a tuple, NRV variables return an ndarray
        if isinstance(data, tuple) or isinstance(data, np.ndarray) or isinstance(data, str) or isinstance(data, list):
            return True
    return False
