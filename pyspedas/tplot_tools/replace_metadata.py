import pyspedas
from pyspedas.tplot_tools import get_y_range
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
        tplot_name = pyspedas.tplot_tools.data_quants[tplot_name].name

    # check if old name is in current dictionary
    if tplot_name not in pyspedas.tplot_tools.data_quants.keys():
        logging.error(f"replace_metadata: {tplot_name} is currently not in pyspedas")
        return

    original_create_time = pyspedas.tplot_tools.data_quants[tplot_name].attrs['plot_options']['create_time']
    original_error = pyspedas.tplot_tools.data_quants[tplot_name].attrs['plot_options']['error']
    original_trange = pyspedas.tplot_tools.data_quants[tplot_name].attrs['plot_options']['trange']
    xaxis_opt = pyspedas.tplot_tools.data_quants[tplot_name].attrs['plot_options']['xaxis_opt']
    yaxis_opt = pyspedas.tplot_tools.data_quants[tplot_name].attrs['plot_options']['yaxis_opt']
    zaxis_opt = pyspedas.tplot_tools.data_quants[tplot_name].attrs['plot_options']['zaxis_opt']
    xaxis_opt['crosshair'] = 'X'
    yaxis_opt['crosshair'] = 'Y'
    zaxis_opt['crosshair'] = 'Z'
    xaxis_opt['x_axis_type'] = 'linear'
    yaxis_opt['y_axis_type'] = 'linear'
    zaxis_opt['z_axis_type'] = 'linear'
    line_opt = {}
    time_bar = []
    extras = dict(panel_size=1, border=True)
    links = {}

    md_copy = deepcopy(new_metadata)
    
    if 'plot_options' not in md_copy.keys():
        md_copy['plot_options'] = {}
        md_copy['plot_options']['xaxis_opt'] = xaxis_opt
        md_copy['plot_options']['yaxis_opt'] = yaxis_opt
        md_copy['plot_options']['zaxis_opt'] = zaxis_opt
        md_copy['plot_options']['line_opt'] = line_opt
        md_copy['plot_options']['trange'] = original_trange
        md_copy['plot_options']['time_bar'] = time_bar
        md_copy['plot_options']['extras'] = extras
        md_copy['plot_options']['create_time'] = original_create_time
        md_copy['plot_options']['links'] = links
        #md_copy['plot_options']['spec_bins_ascending'] = _check_spec_bins_ordering(times, spec_bins)
        md_copy['plot_options']['overplots'] = []
        md_copy['plot_options']['overplots_mpl'] = []
        md_copy['plot_options']['interactive_xaxis_opt'] = {}
        md_copy['plot_options']['interactive_yaxis_opt'] = {}
        md_copy['plot_options']['error'] = original_error

    
    pyspedas.tplot_tools.data_quants[tplot_name].attrs = md_copy
    pyspedas.tplot_tools.data_quants[tplot_name].attrs["plot_options"]["yaxis_opt"]["y_range"] = (
        get_y_range(pyspedas.tplot_tools.data_quants[tplot_name])
    )

    return
