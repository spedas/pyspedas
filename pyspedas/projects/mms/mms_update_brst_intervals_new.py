import os
import csv
import logging
import numpy as np

from pyspedas.tplot_tools import time_double, time_string
from pyspedas.projects.mms.mms_login_lasp import mms_login_lasp
from pyspedas.utilities.download import download
from pyspedas.projects.mms.mms_config import CONFIG
from pyspedas.projects.mms.mms_tai2unix import mms_tai2unix, mms_unix2tai


def mms_update_brst_intervals(trange, padding:float = 300.0):
    """
    This function downloads and caches the current mms_burst_data_segment.csv
    file from the MMS SDC

    Parameters
    ==========
    trange : list of str
        Start and end times to search
    padding: float
        Padding (in seconds) applied to trange boundaries to expand input time range
    """
    tr = time_double(trange)
    tr_tai = mms_unix2tai(tr)

    start_str = time_string(tr[0])
    end_str = time_string(tr[1])

    duration = tr[1] - tr[0]

    if duration > 30*86400:
        logging.error(f'Time range [{start_str}, {end_str}] is longer than 30 days.' )
        return {}

    # not sure if logging in is still important for these
    # so this code might be unnecessary now; for now it
    # remains to match the IDL functionality
    login = mms_login_lasp()

    if login is None:
        logging.error('Error logging into the LASP SDC.')
        return

    session, user = login

    unix_starts = []
    unix_ends = []

    logging.info(f'Downloading burst time intervals for {start_str} - {end_str}')

    remote_path = 'https://lasp.colorado.edu/mms/sdc/public/service/latis/'
    #remote_file = f'mms_burst_data_segment.csv?FINISHTIME>={start_str}+&FINISHTIME<{end_str}'

    remote_file = (
        "mms_burst_data_segment.csv?"
        f"TAIENDTIME%3E={tr_tai[0]-padding:.0f}&"
        f"TAISTARTTIME%3C{tr_tai[1]+padding:.0f}"
    )

    brst_file = download(remote_path=remote_path, remote_file=remote_file,
                            local_file=os.path.join(CONFIG['local_data_dir'], 'mms_burst_data_segment.csv'),
                            session=session, no_wildcards=True)

    if isinstance(brst_file, list):
        # should only be one file
        brst_file = brst_file[0]

    try:
        times = load_csv_file(brst_file)
        if not isinstance(times, tuple) or len(times) != 3:
            logging.error(f'Error loading the CSV file {brst_file}')
            return {}

        taistarttime, taiendtime, status = times

        complete_idxs = np.argwhere(status == 'COMPLETE+FINISHED').flatten()
        if len(complete_idxs) != 0:
            tai_starts = taistarttime[complete_idxs]
            tai_ends = taiendtime[complete_idxs]

            unix_starts.extend(mms_tai2unix(tai_starts))
            unix_ends.extend(mms_tai2unix(tai_ends))

        logging.info(f'Done grabbing updates for {start_str}-{end_str}')
    except IndexError:
        logging.error(f'Error reading CSV file for {start_str}-{end_str}, possible empty file?')


    brst_intervals = {'start_times': unix_starts,
                      'end_times': unix_ends}

    return brst_intervals


def load_csv_file(filename):
    taistarttime = []
    taiendtime = []
    status = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip the header row
        for row in reader:
            taistarttime.append(int(row[1]))
            taiendtime.append(int(row[2]))
            status.append(row[7])
    return np.array(taistarttime), np.array(taiendtime), np.array(status)
