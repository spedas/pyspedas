from pyspedas import store_data, options
import logging
import numpy as np

def make_bss_tplot_var(unix_starts,unix_ends, suffix:str = ''):
    """
    Make a tplot variable like mms_bss_fast from lists of fast survey start and end times

    Parameters
    ----------
    unix_starts:
        Start times of fast survey intervals
    unix_ends:
        End times of fast survey intervals
    suffix:
        Suffix to add to tplot variable name

    Returns
    -------
    None
        No return value, but it creates a tplot variable.
    """

    bar_x = []
    bar_y = []

    for start_time, end_time in zip(unix_starts, unix_ends):
        bar_x.extend([start_time, start_time, end_time, end_time])
        bar_y.extend([np.nan, 0., 0., np.nan])

    varname = 'mms_bss_fast' + suffix
    vars_created = store_data(varname, data={'x': bar_x, 'y': bar_y})

    if not vars_created:
        logging.error('Error creating BSS egment intervals tplot variable')
        return

    varname = 'mms_bss_fast' + suffix
    options(varname, 'panel_size', 0.09)
    options(varname, 'thick', 2)
    options(varname, 'Color', 'green')
    options(varname, 'border', False)
    options(varname, 'yrange', [-0.001, 0.001])
    options(varname, 'legend_names', ['Fast'])
    options(varname, 'ytitle', '')
