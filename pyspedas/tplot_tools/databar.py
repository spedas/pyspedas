
from pyspedas.tplot_tools import timebar
import pyspedas
import logging


def databar(varname, y=0.0, delete=False, color="black", thick=1, dash=False):
    """
    This function will add a horizontal bar at the given value to a plot of a tplot variable.

    Parameters
    ----------
    y : float or list
        The Y-axis value  If a list of numbers are supplied, multiple bars will be created.
    varname : str or list
        The variable(s) to add the vertical bar to. (wildcards accepted)
    delete : bool, optional
        If set to True, at least one varname must be supplied. The timebar at value "y" for variable "varname"
        will be removed.
    color : str
        The color of the bar.
    thick : int
        The thickness of the bar.
    dash : bool
        If set to True, the bar is dashed rather than solid.

    Returns
    -------
    None

    Examples
    --------
    >>> # Place a green time bar at 2017-07-17 00:00:00
    >>> import pyspedas
    >>> pyspedas.databar('*', 0, color='green')

    >>> # Place a dashed data bar at 5500 on the y axis
    >>> pyspedas.databar('*', 5500, dash=True)

    >>> # Place 3 magenta time bars of thickness 5
    >>> # at -100, 0, +100
    >>> # for variable 'sgx' plot
    >>> pyspedas.databar('sgx', [-100, 0, 100],color='m',thick=5)
    """

    # wildcard expansion
    varname = pyspedas.tnames(varname)

    if len(varname) == 0:
        logging.warning("No valid tplot variables specified")
        return

    return timebar(y, varname, databar=True, delete=delete, color=color, thick=thick, dash=dash)
