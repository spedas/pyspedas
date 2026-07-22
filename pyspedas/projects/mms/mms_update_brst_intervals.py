import os
import csv
import logging
import numpy as np

from pyspedas.tplot_tools import time_double, time_string
from pyspedas.projects.mms.mms_login_lasp import mms_login_lasp
from pyspedas.utilities.download import download
from pyspedas.projects.mms.mms_config import CONFIG
from pyspedas.projects.mms.mms_tai2unix import mms_tai2unix, mms_unix2tai
from pyspedas.utilities.month_intervals import month_intervals

def mms_download_brst_intervals(trange):
    tr = time_double(trange)
    # not sure if logging in is still important for these
    # so this code might be unnecessary now; for now it
    # remains to match the IDL functionality
    login = mms_login_lasp()

    if login is None:
        logging.error('Error logging into the LASP SDC.')
        return

    session, user = login

    months = month_intervals(trange[0],trange[1])
    for month_start, month_end in months:
        tr_month = [month_start, month_end]
        tr_tai = mms_unix2tai(tr_month)

        start_str = time_string(tr_month[0])
        end_str = time_string(tr_month[1])

        unix_starts = []
        unix_ends = []

        logging.info(f'Downloading burst time intervals for {start_str} - {end_str}')

        remote_path = 'https://lasp.colorado.edu/mms/sdc/public/service/latis/'
        #remote_file = f'mms_burst_data_segment.csv?FINISHTIME>={start_str}+&FINISHTIME<{end_str}'

        # Here we want only the intervals with TAI start times in the exact time range (not just overlapping)

        remote_file = (
            "mms_burst_data_segment.csv?"
            f"TAISTARTTIME%3E={tr_tai[0]:.0f}&"
            f"TAISTARTTIME%3C{tr_tai[1]:.0f}"
        )

        month_string = time_string(tr_month[0],fmt='%Y_%m')
        monthly_name = 'burst_intervals_'+month_string+'.csv'
        local_file=os.path.join(CONFIG['local_data_dir'],'mms','burst_intervals', monthly_name)
        brst_file = download(remote_path=remote_path, remote_file=remote_file,
                                local_file=local_file,
                                session=session, no_wildcards=True)


def mms_update_brst_intervals(trange, padding:float = 300.0, no_download=False):
    """
    This function downloads and caches the current mms_burst_data_segment.csv
    file from the MMS SDC

    Parameters
    ==========
    trange : list of str
        Start and end times to search
    padding: float
        Padding (in seconds) applied to trange boundaries to expand input time range
    no_download: bool
        If True, use cached files rather than downloading from MMS SDC


    Returns
    =======
    list
        List of burst interval time ranges (start, end) found
    """

    tr = time_double(trange)
    tr_padded = [tr[0]-padding, tr[1]+padding]

    if not no_download:
        mms_download_brst_intervals(tr_padded)

    intervals = month_intervals(tr_padded[0], tr_padded[1])
    unix_starts=[]
    unix_ends=[]
    for month_start,month_end in intervals:
        month_string = time_string(month_start,fmt='%Y_%m')
        monthly_name = 'burst_intervals_' + month_string + '.csv'
        local_file = os.path.join(CONFIG['local_data_dir'], 'mms', 'burst_intervals', monthly_name)

        try:
            times = load_csv_file(local_file)
            if not isinstance(times, tuple) or len(times) != 3:
                logging.error(f'Error loading the CSV file {local_file}')
                continue

            taistarttime, taiendtime, status = times

            complete_idxs = np.argwhere(status == 'COMPLETE+FINISHED').flatten()
            if len(complete_idxs) != 0:
                tai_starts = taistarttime[complete_idxs]
                tai_ends = taiendtime[complete_idxs]

                unix_starts.extend(mms_tai2unix(tai_starts))
                unix_ends.extend(mms_tai2unix(tai_ends))

            logging.info(f'Done grabbing updates for {month_string}')
        except IndexError:
            logging.error(f'Error reading CSV file {local_file}, possible empty file?')
            continue

    # The caller is responsible for any time clipping to remove padding

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
