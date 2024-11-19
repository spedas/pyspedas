import os
import csv
import time
import logging
import pickle
import numpy as np
from pytplot import time_double, time_string
from pyspedas.projects.mms.mms_login_lasp import mms_login_lasp
from pyspedas.utilities.download import download
from pyspedas.projects.mms.mms_config import CONFIG
from pyspedas.projects.mms.mms_tai2unix import mms_tai2unix


def mms_update_brst_intervals():
    """
    This function downloads and caches the current mms_burst_data_segment.csv
    file from the MMS SDC
    """
    # not sure if logging in is still important for these
    # so this code might be unnecessary now; for now it
    # remains to match the IDL functionality
    login = mms_login_lasp()

    if login is None:
        logging.error('Error logging into the LASP SDC.')
        return

    session, user = login

    # grab ~6 months of burst intervals at a time
    start_interval = '2015-03-01'
    end_interval = time_double(start_interval) + 6.*30*24*60*60

    unix_starts = []
    unix_ends = []

    while time_double(start_interval) <= time_double(time.time()):
        start_str = time_string(time_double(start_interval), fmt='%d-%b-%Y')
        end_str = time_string(end_interval, fmt='%d-%b-%Y')

        logging.info(f'Downloading updates for {start_str} - {end_str}')

        remote_path = 'https://lasp.colorado.edu/mms/sdc/public/service/latis/'
        remote_file = f'mms_burst_data_segment.csv?FINISHTIME>={start_str}+&FINISHTIME<{end_str}'

        brst_file = download(remote_path=remote_path, remote_file=remote_file,
                             local_file=os.path.join(CONFIG['local_data_dir'], 'mms_burst_data_segment.csv'),
                             session=session, no_wildcards=True)

        if isinstance(brst_file, list):
            # should only be one file
            brst_file = brst_file[0]

        times = load_csv_file(brst_file)
        if not isinstance(times, tuple) or len(times) != 3:
            logging.error('Error loading the CSV file')
            return

        taistarttime, taiendtime, status = times

        complete_idxs = np.argwhere(status == 'COMPLETE+FINISHED').flatten()
        if len(complete_idxs) != 0:
            tai_starts = taistarttime[complete_idxs]
            tai_ends = taiendtime[complete_idxs]

            unix_starts.extend(mms_tai2unix(tai_starts))
            unix_ends.extend(mms_tai2unix(tai_ends))

        logging.info(f'Done grabbing updates for {start_str}-{end_str}')

        start_interval = end_interval
        end_interval = time_double(start_interval) + 6. * 30 * 24 * 60 * 60

    brst_intervals = {'start_times': unix_starts,
                      'end_times': unix_ends}

    with open(os.path.join(CONFIG['local_data_dir'], 'mms_brst_intervals.pickle'), "wb") as file:
        pickle.dump(brst_intervals, file)

    logging.info(f'Burst intervals updated! Last interval in the file: {time_string(unix_starts[-1])}-{time_string(unix_ends[-1])}')

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
