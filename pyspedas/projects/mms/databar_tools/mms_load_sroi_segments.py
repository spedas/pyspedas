import csv
import logging
import numpy as np
from pyspedas.tplot_tools import time_double, time_string
from pyspedas import month_intervals
from pyspedas.projects.mms.mms_config import CONFIG
from pyspedas.utilities.download import download

def read_mms_srois_csv(filename):
    with open(filename) as f:
        sroi_data = csv.reader(f)

        count = 0
        unix_start = []
        unix_end = []

        for line in sroi_data:
            if count == 0:
                # ignore the first line
                count += 1
                continue

            if len(line) != 4:
                continue

            unix_start.append(time_double(line[0]))
            unix_end.append(time_double(line[1]))

            count += 1
        return unix_start, unix_end


def download_mms_srois(start_time=None, end_time=None, sc_id=None):
    if start_time is None:
        logging.error('Error, start time not specified')
        return

    if end_time is None:
        logging.error('Error, end time not specified')
        return

    if sc_id is None:
        logging.error('Error, sc_id not specified')
        return

    # Download data in chunks of one calendar month each
    l=month_intervals(time_double(start_time), time_double(end_time))
    for t0, t1 in l:
        t0_string = time_string(t0,fmt='%Y-%m-%dT%H:%M:%S')
        t1_string = time_string(t1,fmt='%Y-%m-%dT%H:%M:%S')
        month_string = time_string(t0,fmt='%Y_%m')+'.csv'

        # public unauthenticated path
        path = 'mms/sdc/public/service/latis/mms_events_view.csv'
        query = '?start_time_utc,end_time_utc,sc_id,start_orbit&event_type=SROI'

        # convert to standard ISO format as accepted by LaTiS
        query += '&start_time_utc>=' + t0_string
        query += '&start_time_utc<' + t1_string
        query += '&sc_id=' + sc_id.lower()

        remote_path = 'https://lasp.colorado.edu/' + path
        local_file = CONFIG['local_data_dir']+'/mms/'+sc_id+'/srois/monthly_'+month_string
        downloaded = download(remote_path = remote_path, remote_file = query, local_file=local_file, no_wildcards=True,force_download=True),
        if downloaded is None:
            logging.warning(f"No data returned for {local_file} ")

def mms_load_sroi_segments(trange=None,
                           probe=1,
                           padding = 2*86400,
                           no_download=False):
    """
    This function loads the Science Region of Interest (SRoI) segment intervals
    
    Parameters
    ------------
        trange: list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str or int
            Spacecraft probe # (default: 1)

        padding: float
            Padding (in seconds) to apply to start and end of input time range

        no_download: bool
            If True, use cached files rather than downloading from MMS SDC. Default: False
            
    Returns
    ---------
        Tuple containing (start_times, end_times)

    """
    if not isinstance(probe, str):
        probe = str(probe)

    if trange is None:
        logging.error('Error; no trange specified.')
        return None

    tr = time_double(trange)
    tr_padded = [tr[0] - padding, tr[1]+padding]

    if not no_download:
        download_mms_srois(
            start_time=time_string(tr_padded[0], fmt='%Y-%m-%d %H:%M:%S'),
            end_time=time_string(tr_padded[1], fmt='%Y-%m-%d %H:%M:%S'),
            sc_id='mms'+str(probe))

    unix_start=[]
    unix_end=[]
    l=month_intervals(tr_padded[0], tr_padded[1])
    this_unix_start = []
    this_unix_end = []
    for month_start, month_end in l:
        month_string = time_string(month_start,fmt='%Y_%m.csv')
        sc_id = 'mms'+str(probe)
        local_file = CONFIG['local_data_dir']+'/mms/'+sc_id+'/srois/monthly_'+month_string
        logging.info(f"Loading {local_file}")
        this_unix_start, this_unix_end = read_mms_srois_csv(local_file)
        unix_start.extend(this_unix_start)
        unix_end.extend(this_unix_end)

    if len(unix_start) == 0:
        return ([], [])

    unix_start = np.array(unix_start)
    unix_end = np.array(unix_end)
    times_in_range = (unix_start <= tr[1]) & (unix_end >= tr[0])

    unix_start = unix_start[times_in_range]
    unix_end = unix_end[times_in_range]

    return unix_start, unix_end
