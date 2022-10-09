import csv
import logging
import requests
import numpy as np
from pytplot import store_data, options
from pyspedas import time_double, time_string


def get_mms_srois(start_time=None, end_time=None, sc_id=None):
    if start_time is None:
        logging.error('Error, start time not specified')
        return

    if end_time is None:
        logging.error('Error, end time not specified')
        return

    if sc_id is None:
        logging.error('Error, sc_id not specified')
        return

    # public unauthenticated path
    path = 'mms/sdc/public/service/latis/mms_events_view.csv'

    query = '?start_time_utc,end_time_utc,sc_id,start_orbit&event_type=SROI'

    # convert to standard ISO format as accepted by LaTiS
    query += '&start_time_utc>=' + 'T'.join(start_time.split(' '))
    query += '&start_time_utc<' + 'T'.join(end_time.split(' '))
    query += '&sc_id=' + sc_id.lower()

    qreq = requests.get('https://lasp.colorado.edu/' + path + query)

    if qreq.status_code != 200:
        logging.error('Error downloading SRoI segments')
        return

    sroi_data = csv.reader(qreq.content.decode('utf-8').splitlines())

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

    return (np.array(unix_start), np.array(unix_end))


def mms_load_sroi_segments(trange=None, probe=1, suffix=''):
    """
    This function loads the Science Region of Interest (SRoI) segment intervals
    
    Parameters:
        trange: list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str or int
            Spacecraft probe # (default: 1)

        suffix: str
            Suffix to append to the end of the tplot variables
            
    Returns:
        Tuple containing (start_times, end_times)

    """

    if not isinstance(probe, str):
        probe = str(probe)

    if trange is None:
        logging.error('Error; no trange specified.')
        return None

    tr = time_double(trange)

    unix_start, unix_end = get_mms_srois(
        start_time=time_string(tr[0]-2*86400.0, fmt='%Y-%m-%d %H:%M:%S'), 
        end_time=time_string(tr[1]+2*86400.0, fmt='%Y-%m-%d %H:%M:%S'),
        sc_id='mms'+str(probe))

    if len(unix_start) == 0:
        return ([], [])

    times_in_range = (unix_start >= tr[0]-2*86400.0) & (unix_start <= tr[1]+2*86400.0)

    unix_start = unix_start[times_in_range]
    unix_end = unix_end[times_in_range]

    start_out = []
    end_out = []
    bar_x = []
    bar_y = []

    for start_time, end_time in zip(unix_start, unix_end):
        if end_time >= tr[0] and start_time <= tr[1]:
            bar_x.extend([start_time, start_time, end_time, end_time])
            bar_y.extend([np.nan, 0., 0., np.nan])
            start_out.append(start_time)
            end_out.append(end_time)

    vars_created = store_data('mms' + probe + '_bss_sroi'+suffix, data={'x': bar_x, 'y': bar_y})

    if not vars_created:
        logging.error('Error creating SRoI segment intervals tplot variable')
        return None

    options('mms' + probe + '_bss_sroi'+suffix, 'panel_size', 0.09)
    options('mms' + probe + '_bss_sroi'+suffix, 'thick', 2)
    options('mms' + probe + '_bss_sroi'+suffix, 'Color', 'green')
    options('mms' + probe + '_bss_sroi'+suffix, 'border', False)
    options('mms' + probe + '_bss_sroi'+suffix, 'yrange', [-0.001,0.001])
    options('mms' + probe + '_bss_sroi'+suffix, 'legend_names', ['Fast'])
    options('mms' + probe + '_bss_sroi'+suffix, 'ytitle', '')

    return (start_out, end_out)
