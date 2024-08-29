
import numpy as np
import pytplot
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
        >>> import pytplot
        >>> pytplot.store_data('a', data={'x': range(10), 'y': range(10)})
        >>> pytplot.store_data('b', data={'x': range(10), 'y': range(10)})
        >>> pytplot.store_data('pseudovar', data=['a','b'])
        >>> pytplot.is_pseudovariable('a')  # False
        >>> pytplot.is_pseudovariable('pseudo') # True

    """
    pseudo_var = False
    if tvar in pytplot.data_quants.keys():
        var_quants = pytplot.data_quants[tvar]

        if not isinstance(var_quants, dict):
            overplot_list = var_quants.attrs['plot_options'].get('overplots_mpl')
            if overplot_list is not None and len(overplot_list) > 0:
                pseudo_var = True

        var_data = pytplot.get_data(tvar, dt=True)

        if isinstance(var_data, list) or isinstance(var_data, str) or pseudo_var:
            return True
    else:
        logging.warning("The name %s is not in pytplot.",tvar)

    return False
