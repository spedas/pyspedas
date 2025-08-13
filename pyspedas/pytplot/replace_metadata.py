import pyspedas
from pyspedas.pytplot import get_y_range
from copy import deepcopy
import logging


def replace_metadata(tplot_name, new_metadata):
    """
    This function will replace all the metadata in a tplot variable.

    Parameters
    ----------
    tplot_name : str
        The name of the tplot variable.
    new_metadata : dict
        A dictionary with metadata values. A deep copy will be performed so that
        no references to new_metadata are retained.

    Returns
    -------
    None

    Examples
    --------
    >>> # Copy Variable 1 metadata into Variable 2, which must already exist
    >>> import pyspedas
    >>> meta = pyspedas.get_data('Variable1', metadata=True)
    >>> pyspedas.replace_metadata("Variable2", meta)
    """

    # if old name input is a number, convert to corresponding name
    if isinstance(tplot_name, int):
        tplot_name = pyspedas.pytplot.data_quants[tplot_name].name

    # check if old name is in current dictionary
    if tplot_name not in pyspedas.pytplot.data_quants.keys():
        logging.error(f"{tplot_name} is currently not in pytplot")
        return

    pyspedas.pytplot.data_quants[tplot_name].attrs = deepcopy(new_metadata)
    pyspedas.pytplot.data_quants[tplot_name].attrs["plot_options"]["yaxis_opt"]["y_range"] = (
        get_y_range(pyspedas.pytplot.data_quants[tplot_name])
    )

    return
