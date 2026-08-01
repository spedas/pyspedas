import logging
import numpy as np
from pyspedas.tplot_tools import time_double
from pyspedas.projects.mms.mms_update_brst_intervals import mms_update_brst_intervals


def mms_load_brst_segments(trange=None,
                           no_download=False):
    """
    This function loads the burst segment intervals
    
    Parameters
    -----------
        trange : list of str
            time range of interest [start time, end time] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        no_download: bool
            If True, use cached files rather than downloading from MMS SDC. Default: False

    Returns
    ---------
        Tuple containing (start_times, end_times)
    """

    if trange is None:
        logging.error('Error; no trange specified.')
        return None

    tr = time_double(trange)

    intervals = mms_update_brst_intervals(tr, no_download=no_download)

    if intervals:
        unix_start = np.array(intervals['start_times'])
        unix_end = np.array(intervals['end_times'])
    else:
        logging.error('Error downloading latest burst intervals file.')
        return

    sorted_idxs = np.argsort(unix_start)
    unix_start = unix_start[sorted_idxs]
    unix_end = unix_end[sorted_idxs]

    times_in_range = (unix_start >= tr[0]-300.0) & (unix_start <= tr[1]+300.0)

    unix_start = unix_start[times_in_range]
    unix_end = unix_end[times_in_range]

    if len(unix_start) == 0:
        logging.error('No burst intervals found in the time range.')
        return None

    # +10 second offset added; there appears to be an extra 10
    # seconds of data, consistently, not included in the range here
    unix_end = np.array([end_time+10.0 for end_time in unix_end])

    return unix_start, unix_end
