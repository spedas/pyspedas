import os
import logging
import numpy as np
from scipy.io import readsav
from pathlib import Path, PosixPath
import time

from pyspedas.tplot_tools import time_double, time_string
from pyspedas.projects.mms.mms_login_lasp import mms_login_lasp
from pyspedas.utilities.download import download
from pyspedas.projects.mms.mms_config import CONFIG
from pyspedas.projects.mms.mms_tai2unix import mms_tai2unix, mms_unix2tai
from pyspedas import tai2unix, unix2tai, store_data, options
from .make_bss_tplot_var import make_bss_tplot_var

def abs_selection_file_timestamp(pathobj: PosixPath):
    basename=pathobj.name
    # abs_selections_YYYY_MM_DD_HH_mm_ss.sav
    yyyy=basename[15:19]
    mon=basename[20:22]
    day=basename[23:25]
    hr=basename[26:28]
    mm=basename[29:31]
    sec=basename[32:34]
    timestamp_str=f"{yyyy}-{mon}-{day}/{hr}:{mm}:{sec}"
    timestamp_dbl = time_double(timestamp_str)
    return timestamp_dbl

def abs_selection_file_start_end(filename):
    this_result = readsav(filename)
    fomstr = this_result.fomstr
    # It is possible that some files will not have a TIMESTAMPS entry.
    try:
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
    except AttributeError as e:
        logging.warning(f"File {filename} contained no timestamps")
        unix_start = None
        unix_end = None
    return unix_start, unix_end

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

def download_abs_selections(start_str,
                            end_str,
                            always_prompt=False,
                            headers=False):
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
                            local_file=os.path.join(CONFIG['local_data_dir'],'mms', 'abs',os.path.basename(abs)),
                            session=session, no_wildcards=True)
        if abs_file is not None:
            abs_local_files.extend(abs_file)
            # Throttle the requests a bit since these are very small files
            time.sleep(1)

    return abs_local_files

def mms_update_fast_intervals(trange,
                              # Two days of padding should be more than enough for times before the cutover to SROI data
                              padding:float = 2*86400.0,
                              always_prompt=False,
                              headers=False,
                              suffix:str = '',
                              no_download=True,
                              make_tplot_var = True,
                              ):
    """
    This function downloads and caches the current mms_burst_data_segment.csv
    file from the MMS SDC

    Parameters
    ==========
    trange : list of str
        Start and end times to search
    padding: float
        Padding (in seconds) applied to trange boundaries to expand input time range
    always_prompt: bool
        Do not use cached MMS SDC credentials, but prompt the user to enter them.  Default: false
    headers: bool
        Passed through to mms_login_lasp
    suffix: str
        A string to add to the end of the tplot variable created. Default: ''
    no_download: bool
        If True, use cached files rather than downloading from the MMS SDC. Default: False
    make_tplot_var: bool
        If True, make a tplot variable from the loaded fast survey time intervals. Default: True

    Returns
    =======
    list
        List of fast survey intervals (start, end) found
    """

    tr = time_double(trange)
    tr_padded = [tr[0]-padding, tr[1]+padding]
    tr_tai = mms_unix2tai(tr)

    start_str = time_string(tr[0]-padding,fmt='%Y-%m-%d')
    end_str = time_string(tr[1]+padding, fmt='%Y-%m-%d')

    duration = tr[1] - tr[0]

    if not no_download:
        abs_local_files = download_abs_selections(start_str, end_str, always_prompt=always_prompt, headers=headers)
        abs_local_paths = [PosixPath(fn) for fn in abs_local_files]
    else:
        abs_dir = Path(os.path.join(CONFIG['local_data_dir'],'mms', 'abs'))
        abs_local_paths = sorted(abs_dir.glob('abs_selections_*.sav'))
        pass

    unix_starts = []
    unix_ends = []

    dt_start = []
    dt_end = []
    ft = []
    # Now loop through the sav files, restore each one, and get the segment start/end times
    first_seg = True
    last_start = -1.0
    last_end = -1.0
    for abs_local_path in abs_local_paths:
        file_timestamp = abs_selection_file_timestamp(abs_local_path)
        if file_timestamp < tr_padded[0]:
            # Skip this file
            continue
        logging.info(f"Loading {abs_local_path}")
        unix_start, unix_end = abs_selection_file_start_end(abs_local_path)
        if unix_start is None or unix_end is None:
            # If timestamps not found, skip this file
            continue

        #print(f"start: {time_string(unix_start)} end: {time_string(unix_end)} file: {time_string(file_timestamp)}")
        #print(f" file-start: {file_timestamp-unix_start}  file end: {file_timestamp - unix_end}")
        duration = unix_end - unix_start
        if duration > 100000:
            # Warn, but don't skip this interval (yet)
            logging.warning(f"Long duration: {duration} sec")
        if not first_seg and unix_start == last_start:
            logging.warning(f"Duplicate segment start times {time_string(unix_start)} ignored")
            # Skip duplicate or out-of-order segments
            continue
        elif not first_seg and unix_end == last_end:
            logging.warning(f"Duplicate segment end times {time_string(unix_end)} ignored")
            # Skip duplicate or out-of-order segments
            continue
        elif not first_seg and (unix_start < last_start):
            logging.warning(f"Out-of-order segment start times ignored (current: {time_string(unix_start)} previous: {time_string(last_start)})")
            # Skip duplicate or out-of-order segments
            continue
        elif not first_seg and (unix_end < last_end):
            logging.warning(f"Out-of-order segment end times ignored (current: {time_string(unix_end)} previous: {time_string(last_end)})")
            # Skip duplicate or out-of-order segments
            continue
        if not first_seg:
            # Check for gaps (after checking for duplicate segments)
            gap = unix_start - last_end
            if gap < 0.0:
                logging.warning(f"Negative gap: last end: {time_string(last_end)} this_start: {time_string(unix_start)}")
            elif gap > 86000:
                logging.warning(f"Long gap ({gap/86400.0} days): last end: {time_string(last_end)} this_start: {time_string(unix_start)}")

        else:
            dt_start.append(file_timestamp - unix_start)
            dt_end.append(file_timestamp - unix_end)
            ft.append(file_timestamp)
        last_start=unix_start
        last_end=unix_end
        first_seg=False

        # Some intervals may not intersect the desired time range due to padding
        if (unix_start <= tr[1] and unix_end >= tr[0]):
            # print(f"In-range interval found: {time_string(unix_start)} - {time_string(unix_end)}" )
            unix_starts.append(unix_start)
            unix_ends.append(unix_end)
        else:
            # print(f"Out-of-range interval found: {time_string(unix_start)} - {time_string(unix_end)}" )
            pass
        if unix_start > tr[1]:
            logging.info("Start time of this file is after the requested time range, quitting search")
            break

    if len(unix_starts) < 1:
        logging.warning("mms_update_fast_intervals: No ABS fast survey intervals found in requested time range!")

    if make_tplot_var:
        make_bss_tplot_var(unix_starts,unix_ends, suffix=suffix)

    return unix_starts, unix_ends