
import numpy as np
import pytplot

def data_exists(tvar):
    """
    Checks if a tplot variable exists

    Parameter
    ----------
    tvar: str
        Name of tplot variable to check

    Return
    ----------
    bool:
        Retrun True if tplot variable exists.

    Example
    ----------
        >>> import pytplot
        >>> pytplot.store_data('a', data={'x': range(10), 'y': range(10)})
        >>> pytplot.data_exists('a')

    """
    if tvar in pytplot.data_quants.keys():
        data = pytplot.get_data(tvar, dt=True)
        # multi-dimensional data returns a tuple, NRV variables return an ndarray
        if isinstance(data, tuple) or isinstance(data, np.ndarray) or isinstance(data, str) or isinstance(data, list):
            return True
    return False
