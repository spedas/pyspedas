import os
import logging
import numpy as np
import pandas as pd
from pyspedas import time_string, time_double
from pyspedas.projects.mms.mms_tai2unix import mms_tai2unix
from pyspedas.utilities.download import download
from pyspedas.projects.mms.mms_config import CONFIG


def mms_brst_events(trange=None, reload=False):
    """
    Prints a list of burst mode segment selections from the MMS data segment database

    Parameters
    -----------
        trange: list of str or list of float
            Time range to list burst mode events

        reload:
            Re-download the burst mode events database
    """
    if trange is None:
        logging.error('Time range not specified. ')
        return

    remote_path = 'https://lasp.colorado.edu/mms/sdc/public/service/latis/'
    remote_file = 'mms_burst_data_segment.csv'

    if reload or not os.path.exists(os.path.join(CONFIG['local_data_dir'], remote_file)):
        brst_file = download(remote_path=remote_path, remote_file=remote_file, local_path=CONFIG['local_data_dir'])
        if len(brst_file) > 0:
            brst_file = brst_file[0]
    else:
        brst_file = os.path.join(CONFIG['local_data_dir'], remote_file)

    table = load_csv_file(brst_file)

    descriptions = table['DISCUSSION'].to_numpy()
    authors = table['SOURCEID'].to_numpy()
    start_tai = np.float64(table['TAISTARTTIME'].to_numpy())
    end_tai = np.float64(table['TAIENDTIME'].to_numpy())

    start_unix = mms_tai2unix(start_tai)
    end_unix = mms_tai2unix(end_tai)

    # sort based on start time
    sorted_indices = np.argsort(start_unix)
    descriptions = descriptions[sorted_indices]
    authors = authors[sorted_indices]
    start_unix = start_unix[sorted_indices]
    end_unix = end_unix[sorted_indices]

    trange = time_double(trange)
    idxs = ((start_unix >= trange[0]) & (start_unix <= trange[1])) & ((end_unix <= trange[1]) & (end_unix >= trange[0]))
    indices = np.argwhere(idxs).flatten()
    descriptions = descriptions[indices]
    authors = authors[indices]
    start_times = start_unix[indices]
    end_times = end_unix[indices]

    for desc, author, start_time, end_time in zip(descriptions, authors, start_times, end_times):
        print(time_string(start_time, fmt='%Y-%m-%d/%H:%M:%S') + ' - ' + time_string(end_time, fmt='%Y-%m-%d/%H:%M:%S') + ': ' + str(desc) + ' (' + str(author) + ')')


def load_csv_file(filename, cols=None):
    """
    Loads the burst segment CSV file into a pandas data frame
    """
    if cols is None:
        cols = ['DATASEGMENTID', 'TAISTARTTIME', 'TAIENDTIME', 'PARAMETERSETID', 'FOM', 'ISPENDING', 'INPLAYLIST', 'STATUS', 'NUMEVALCYCLES', 'SOURCEID', 'CREATETIME', 'FINISHTIME', 'OBS1NUMBUFS', 'OBS2NUMBUFS', 'OBS3NUMBUFS', 'OBS4NUMBUFS', 'OBS1ALLOCBUFS', 'OBS2ALLOCBUFS', 'OBS3ALLOCBUFS', 'OBS4ALLOCBUFS', 'OBS1REMFILES', 'OBS2REMFILES', 'OBS3REMFILES', 'OBS4REMFILES', 'DISCUSSION', 'empty1', 'empty2']
    df = pd.read_csv(filename, dtype=str, names=cols, on_bad_lines='skip', skiprows=1)
    return df
