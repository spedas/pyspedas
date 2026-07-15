import os
import logging
import numpy as np
from scipy.io import readsav

from pyspedas.tplot_tools import time_double, time_string
from pyspedas.projects.mms.mms_login_lasp import mms_login_lasp
from pyspedas.utilities.download import download
from pyspedas.projects.mms.mms_config import CONFIG
from pyspedas.projects.mms.mms_tai2unix import mms_tai2unix, mms_unix2tai
from pyspedas import tai2unix, unix2tai

def get_mms_abs_selections(start_time=None, end_time=None, session=None):
    if start_time is None:
        logging.error('Error, start time not specified')
        return

    if end_time is None:
        logging.error('Error, end time not specified')
        return

    sdc_session = session

    # sitl path
    path = 'mms/sdc/sitl/files/api/v1/file_names/abs_selections'

    query = f'?start_date={start_time}&end_date={end_time}'

    qreq = sdc_session.get('https://lasp.colorado.edu/' + path + query)

    if qreq.status_code != 200:
        logging.error(f'Error {qreq.status_code} downloading abs_selections')
        return

    response=qreq.text

    file_list = response.split(',')
    return file_list


def mms_update_fast_intervals(trange, padding:float = 86400.0, always_prompt=False, headers=False):
    """
    This function downloads and caches the current mms_burst_data_segment.csv
    file from the MMS SDC

    Parameters
    ==========
    trange : list of str
        Start and end times to search
    padding: float
        Padding (in seconds) applied to trange boundaries to expand input time range

    Returns
    =======
    list
        List of fast survey intervals (start, end) found
    """

    tr = time_double(trange)
    tr_tai = mms_unix2tai(tr)

    start_str = time_string(tr[0]-padding,fmt='%Y-%m-%d')
    end_str = time_string(tr[1]+padding, fmt='%Y-%m-%d')

    duration = tr[1] - tr[0]

    # not sure if logging in is still important for these
    # so this code might be unnecessary now; for now it
    # remains to match the IDL functionality
    login = mms_login_lasp(always_prompt=always_prompt, headers=headers)

    if login is None:
        logging.error('Error logging into the LASP SDC.')
        return

    session, user = login

    abs_results=get_mms_abs_selections(start_str, end_str, session)

    # The files seem to come out in reverse chronological order, so we'll sort them
    abs_results_sorted = abs_results.sort()
    unix_starts = []
    unix_ends = []

    if len(abs_results) < 1:
        logging.warning(f"No intervals found in interval {start_str} - {end_str}")
        return None

    # Download all the files that were found
    remote_path = 'https://lasp.colorado.edu/mms/sdc/sitl/files/api/v1/download/abs_selections'
    abs_local_files = []

    for abs in abs_results:
        logging.info(f'Downloading {abs}')
        remote_file = f"?file={os.path.basename(abs)}"

        abs_file = download(remote_path=remote_path, remote_file=remote_file,
                            local_file=os.path.join(CONFIG['local_data_dir'],'mms', 'abs_selections',os.path.basename(abs)),
                            session=session, no_wildcards=True)
        if abs_file is not None:
            abs_local_files.extend(abs_file)

    # Now loop through the sav files, restore each one, and get the segment start/end times
    for abs_local_file in abs_local_files:
        this_result = readsav(abs_local_file)
        fomstr = this_result.fomstr
        ts0 = fomstr.TIMESTAMPS
        # Un-nest the timestamp array we want to get at
        ts1 = ts0[0]
        # First and last times in the array are the start/end of the fast survey interval
        tai_start = ts1[0]
        tai_end = ts1[-1]
        # Times are in TAI seconds...they come out of the sav file as unsigned integers; we convert to signed here to avoid problems
        # in the tai to unix conversion
        unix_start = tai2unix(np.int64(tai_start))
        unix_end = tai2unix(np.int64(tai_end))
        # Some intervals may not intersect the desired time range due to padding
        if (unix_start <= tr[1] and unix_end >= tr[0]):
            # print(f"In-range interval found: {time_string(unix_start)} - {time_string(unix_end)}" )
            unix_starts.append(unix_start)
            unix_ends.append(unix_end)
        else:
            # print(f"Out-of-range interval found: {time_string(unix_start)} - {time_string(unix_end)}" )
            pass

    if len(unix_starts) < 1:
        logging.warning("No fast survey intervals found in requested time range!")


    return unix_starts, unix_ends