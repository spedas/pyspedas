import pytplot
import numpy as np
from pytplot import tplot_utilities as utilities
import logging


def replace_data(tplot_name, new_data):
    """
    This function will replace all of the data in a tplot variable.

    Parameters
    ----------
    tplot_name : str
        The name of the tplot variable.
    new_data : array_like
        The new data to replace the existing data.
        This can be any object that can be converted into an np.array.

    Returns
    -------
    None

    Examples
    --------
    >>> # Replace data into an existing variable
    >>> import pytplot
    >>> pytplot.store_data("v1", data={'x':[1,2,3,4],'y':[1,2,3,4]})
    >>> print(pytplot.get_data('v1'))
    >>> pytplot.replace_data("v1",[5,6,7,8])
    >>> print(pytplot.get_data('v1'))
    """

    # if old name input is a number, convert to corresponding name
    if isinstance(tplot_name, int):
        tplot_name = pytplot.data_quants[tplot_name].name

    # check if old name is in current dictionary
    if tplot_name not in pytplot.data_quants.keys():
        logging.info(f"{tplot_name} is currently not in pytplot")
        return

    new_data_np = np.asarray(new_data)
    shape_old = pytplot.data_quants[tplot_name].values.shape
    shape_new = new_data_np.shape
    if shape_old != shape_new:
        logging.info(
            f"Dimensions do not match for replace data. {shape_new} does not equal {shape_old}.  Returning..."
        )
        return

    pytplot.data_quants[tplot_name].values = new_data_np

    pytplot.data_quants[tplot_name].attrs["plot_options"]["yaxis_opt"]["y_range"] = (
        utilities.get_y_range(pytplot.data_quants[tplot_name])
    )

    return
