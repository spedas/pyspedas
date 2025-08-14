
import numpy as np
import pyspedas
from pyspedas.tplot_tools import get_data
import logging

def is_pseudovariable(tvar):
    """
    Checks if a tplot variable is a pseudovariable

    Parameter
    ----------
    tvar: str
        Name of tplot variable to check

    Return
    ----------
    bool:
        Return True if tplot variable is a pseudovariable.

    Example
    ----------
        >>> import pyspedas
        >>> pyspedas.store_data('a', data={'x': range(10), 'y': range(10)})
        >>> pyspedas.store_data('b', data={'x': range(10), 'y': range(10)})
        >>> pyspedas.store_data('pseudovar', data=['a','b'])
        >>> pyspedas.is_pseudovariable('a')  # False
        >>> pyspedas.is_pseudovariable('pseudo') # True

    """
    pseudo_var = False
    if tvar in pyspedas.tplot_tools.data_quants.keys():
        var_quants = pyspedas.tplot_tools.data_quants[tvar]

        if not isinstance(var_quants, dict):
            overplot_list = var_quants.attrs['plot_options'].get('overplots_mpl')
            if overplot_list is not None and len(overplot_list) > 0:
                pseudo_var = True

        var_data = get_data(tvar, dt=True)

        if isinstance(var_data, list) or isinstance(var_data, str) or pseudo_var:
            return True
    else:
        logging.warning("The name %s is not in pyspedas.",tvar)

    return False
