import pyspedas
import logging
from pyspedas.tplot_tools import str_to_float_fuzzy, rgb_color

def timebar_delete(t, varname=None, dim='height'):
    if varname is None:
        for name in pyspedas.tplot_tools.data_quants:
            if isinstance(pyspedas.tplot_tools.data_quants[name], dict):
                # non-record varying variable
                continue
            try:
                list_timebars = pyspedas.tplot_tools.data_quants[name].attrs['plot_options']['time_bar']
            except KeyError:
                continue
            elem_to_delete = []
            for elem in list_timebars:
                for num in t:
                    if (elem['location'] == num) and (elem['dimension'] == dim):
                        elem_to_delete.append(elem)
            for i in elem_to_delete:
                list_timebars.remove(i)
            pyspedas.tplot_tools.data_quants[name].attrs['plot_options']['time_bar'] = list_timebars
    else:
        if not isinstance(varname, list):
            varname = [varname]
        for i in varname:
            if i not in pyspedas.tplot_tools.data_quants.keys():
                logging.info(str(i) + " is currently not in pyspedas.")
                return
            if isinstance(pyspedas.tplot_tools.data_quants[i], dict):
                # non-record varying variable
                continue
            try:
                list_timebars = pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['time_bar']
            except KeyError:
                continue
            elem_to_delete = []
            for elem in list_timebars:
                for num in t:
                    if (elem['location'] == num) and (elem['dimension'] == dim):
                        elem_to_delete.append(elem)
            for j in elem_to_delete:
                list_timebars.remove(j)
            # pyspedas.tplot_tools.data_quants[i].attrs['plot_options']['time_bar']
    return


def timebar(t, varname=None, databar=False, delete=False, color="black", thick=1, dash=False):
    """
    This function will add a vertical bar to all time series plots. This is useful if you
    want to bring attention to a specific time.

    Parameters
    ----------
    t : float or list
        The time in seconds since Jan 01 1970 to place the vertical bar. If a list of numbers are supplied,
        multiple bars will be created. If "databar" is set, then "t" becomes the point on the y axis to
        place a horizontal bar.
    varname : str or list, optional
        The variable(s) to add the vertical bar to. If not set, the default is to add it to all current plots. (wildcards accepted)
    databar : bool, optional
        This will turn the timebar into a horizontal data bar. If this is set True, then variable "t" becomes
        the point on the y axis to place a horizontal bar.
    delete : bool, optional
        If set to True, at least one varname must be supplied. The timebar at point "t" for variable "varname"
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
    >>> pyspedas.timebar(1500249600, color='green')

    >>> # Place a dashed data bar at 5500 on the y axis
    >>> pyspedas.timebar(5500, dash=True, databar=True)

    >>> # Place 3 magenta time bars of thickness 5
    >>> # at [2015-12-26 05:20:01, 2015-12-26 08:06:40, 2015-12-26 08:53:19]
    >>> # for variable 'sgx' plot
    >>> pyspedas.timebar([1451107201,1451117200,1451119999],'sgx',color='m',thick=5)
    """

    # wildcard expansion
    varname = pyspedas.tnames(varname)

    # make sure t entered is a list
    if not isinstance(t, list):
        t = [t]

    # if entries in list not numerical, run str_to_int
    if not isinstance(t[0], (int, float, complex)):
        t1 = []
        for time in t:
            t1.append(str_to_float_fuzzy(time))
        t = t1

    dim = "height"
    if databar is True:
        dim = "width"

    dash_pattern = "solid"
    if dash is True:
        dash_pattern = "dashed"

    if delete is True:
        timebar_delete(t, varname, dim)
        return

    # if no varname specified, add timebars to every plot
    if varname is None:
        num_bars = len(t)
        for i in range(num_bars):
            tbar = {}
            tbar["location"] = t[i]
            tbar["dimension"] = dim
            tbar["line_color"] = rgb_color(color)[0]
            tbar["line_width"] = thick
            tbar["line_dash"] = dash_pattern
            for name in pyspedas.tplot_tools.data_quants:
                temp_data_quants = pyspedas.tplot_tools.data_quants[name]
                if isinstance(temp_data_quants, dict):
                    # non-record varying variable
                    continue
                temp_data_quants.attrs["plot_options"]["time_bar"].append(tbar)
    # if varname specified
    else:
        if not isinstance(varname, list):
            varname = [varname]
        for j in varname:
            if j not in pyspedas.tplot_tools.data_quants.keys():
                logging.info(str(j) + "is currently not in pyspedas")
            else:
                num_bars = len(t)
                for i in range(num_bars):
                    tbar = {}
                    tbar["location"] = t[i]
                    tbar["dimension"] = dim
                    tbar["line_color"] = rgb_color(color)[0]
                    tbar["line_width"] = thick
                    tbar["line_dash"] = dash_pattern
                    temp_data_quants = pyspedas.tplot_tools.data_quants[j]
                    if isinstance(temp_data_quants, dict):
                        # non-record varying variable
                        continue
                    temp_data_quants.attrs["plot_options"]["time_bar"].append(tbar)
    return
