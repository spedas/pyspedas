import os
import logging
import numpy as np
from scipy.io import readsav
from pytplot import store_data, options

from pyspedas import time_double
from pyspedas.utilities.download import download
from pyspedas.mms.mms_config import CONFIG


def mms_load_fast_segments(trange=None, suffix=''):
    '''
    This function loads the fast segment intervals
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        suffix: str
            Suffix to append to the end of the tplot variables
            
    Returns:
        Tuple containing (start_times, end_times)

    '''

    if trange is None:
        logging.error('Error; no trange specified.')
        return None

    tr = time_double(trange)

    save_file = os.path.join(CONFIG['local_data_dir'], 'mms_fast_intervals.sav')
    fast_file = download(remote_file='http://www.spedas.org/mms/mms_fast_intervals.sav',
        local_file=save_file)

    if len(fast_file) == 0:
        logging.error('Error downloading fast intervals sav file')
        return None

    try:
        intervals = readsav(save_file)
    except FileNotFoundError:
        logging.error('Error loading fast intervals sav file: ' + save_file)
        return None

    unix_start = np.flip(intervals['fast_intervals'].start_times[0])
    unix_end = np.flip(intervals['fast_intervals'].end_times[0])

    times_in_range = (unix_start >= tr[0]-2*86400.0) & (unix_start <= tr[1]+2*86400.0)

    unix_start = unix_start[times_in_range]
    unix_end = unix_end[times_in_range]

    bar_x = []
    bar_y = []

    for start_time, end_time in zip(unix_start, unix_end):
        if end_time >= tr[0] and start_time <= tr[1]:
            bar_x.extend([start_time, start_time, end_time, end_time])
            bar_y.extend([np.nan, 0., 0., np.nan])

    vars_created = store_data('mms_bss_fast'+suffix, data={'x': bar_x, 'y': bar_y})

    if not vars_created:
        logging.error('Error creating fast segment intervals tplot variable')
        return None

    options('mms_bss_fast'+suffix, 'panel_size', 0.09)
    options('mms_bss_fast'+suffix, 'thick', 2)
    options('mms_bss_fast'+suffix, 'Color', 'red')
    options('mms_bss_fast'+suffix, 'border', False)
    options('mms_bss_fast'+suffix, 'yrange', [-0.001,0.001])
    options('mms_bss_fast'+suffix, 'legend_names', ['Fast'])
    options('mms_bss_fast'+suffix, 'ytitle', '')

    return (unix_start, unix_end)
