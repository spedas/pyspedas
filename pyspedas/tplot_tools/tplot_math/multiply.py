import pyspedas
from pyspedas.tplot_tools import store_data, tinterp
import copy
import logging


def multiply(tvar1, tvar2, newname=None):
    """
    Multiplies two tplot variables.  Will interpolate if the two are not on the same time cadence.

    Parameters
    ----------
        tvar1 : str
            Name of first tplot variable.
        tvar2 : int/float
            Name of second tplot variable.
        newname : str
            Name of new tplot variable.  If not set, then the data in tvar1 is replaced.

    Returns
    -------
        None

    Examples
    --------
        >>> x1 = [0, 4, 8, 12, 16]
        >>> x2 = [0, 4, 8, 12, 16, 19, 21]
        >>> time1 = [pyspedas.time_float("2020-01-01") + i for i in x1]
        >>> time2 = [pyspedas.time_float("2020-01-01") + i for i in x2]
        >>> pyspedas.store_data("a", data={"x": time1, "y": [1, 2, 3, 4, 5]})
        >>> pyspedas.store_data("c", data={"x": time2, "y": [1, 4, 1, 7, 1, 9, 1]})
        >>> n = pyspedas.multiply("a", "c", newname="a_x_c")
        >>> print('new tplot variable:', n)
        >>> ac = pyspedas.get_data(n)
        >>> print(ac)
    """

    # interpolate tvars
    tv2 = tinterp(tvar1, tvar2)
    # separate and multiply data
    data1 = pyspedas.tplot_tools.data_quants[tvar1].values
    data2 = pyspedas.tplot_tools.data_quants[tv2].values
    data = data1 * data2

    if newname is None:
        pyspedas.tplot_tools.data_quants[tvar1].values = data
        return tvar1

    if "spec_bins" in pyspedas.tplot_tools.data_quants[tvar1].coords:
        store_data(
            newname,
            data={
                "x": pyspedas.tplot_tools.data_quants[tvar1].coords["time"].values,
                "y": data,
                "v": pyspedas.tplot_tools.data_quants[tvar1].coords["spec_bins"].values,
            },
        )
        pyspedas.tplot_tools.data_quants[newname].attrs = copy.deepcopy(
            pyspedas.tplot_tools.data_quants[tvar1].attrs
        )
    else:
       store_data(
            newname,
            data={"x": pyspedas.tplot_tools.data_quants[tvar1].coords["time"].values, "y": data},
        )
       pyspedas.tplot_tools.data_quants[newname].attrs = copy.deepcopy(
            pyspedas.tplot_tools.data_quants[tvar1].attrs
        )
    return newname
