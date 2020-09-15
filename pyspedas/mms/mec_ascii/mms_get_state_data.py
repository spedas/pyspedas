

import requests
import os
import logging
import warnings

from shutil import copyfileobj, copy
from tempfile import NamedTemporaryFile

from pyspedas import time_double, time_string
from pyspedas.mms.mms_login_lasp import mms_login_lasp
from pyspedas.mms.mms_config import CONFIG
from pyspedas.mms.mec_ascii.mms_get_local_state_files import mms_get_local_state_files
from pyspedas.mms.mec_ascii.mms_load_eph_tplot import mms_load_eph_tplot
from pyspedas.mms.mec_ascii.mms_load_att_tplot import mms_load_att_tplot

def mms_get_state_data(probe='1', trange=['2015-10-16', '2015-10-17'], 
    datatypes=['pos', 'vel'], level='def', no_download=False, pred_or_def=True, 
    suffix='', always_prompt=False):
    """
    Helper routine for loading state data (ASCII files from the SDC); not meant to be called directly; see pyspedas.mms.state instead
    
    """

    if not isinstance(probe, list): probe = [probe]

    local_data_dir = CONFIG['local_data_dir']
    download_only = CONFIG['download_only']


    start_time = time_double(trange[0])-60*60*24.
    end_time = time_double(trange[1])

    # check if end date is anything other than 00:00:00, if so
    # add a day to the end time to ensure that all data is downloaded
    if type(trange[1]) == str:
        endtime_day = time_double(time_string(time_double(trange[1]), fmt='%Y-%m-%d'))
    else:
        endtime_day = time_double(time_string(trange[1], fmt='%Y-%m-%d'))

    if end_time > endtime_day:
        add_day = 60*60*24.
    else:
        add_day = 0

    start_time_str = time_string(start_time, fmt='%Y-%m-%d')
    end_time_str = time_string(end_time+add_day, fmt='%Y-%m-%d')

    filetypes = []

    if 'pos' in datatypes or 'vel' in datatypes:
        filetypes.append('eph')

    if 'spinras' in datatypes or 'spindec' in datatypes:
        filetypes.append('att')

    user = None
    if not no_download:
        sdc_session, user = mms_login_lasp(always_prompt=always_prompt)

    for probe_id in probe:
        # probe will need to be a string from now on
        probe_id = str(probe_id)

        for filetype in filetypes:
            file_dir = local_data_dir + 'ancillary/' + 'mms' + probe_id + '/' + level + filetype + '/'
            product = level + filetype

            files_in_interval = []
            out_files = []

            out_dir = os.sep.join([local_data_dir, 'ancillary', 'mms'+probe_id, level+filetype])

            if CONFIG['no_download'] != True and no_download != True:
                # predicted doesn't support start_date/end_date
                if level == 'def':
                    dates_for_query = '&start_date='+start_time_str+'&end_date='+end_time_str
                else:
                    dates_for_query = ''

                if user == None:
                    url = 'https://lasp.colorado.edu/mms/sdc/public/files/api/v1/file_info/ancillary?sc_id=mms'+probe_id+'&product='+product+dates_for_query
                else:
                    url = 'https://lasp.colorado.edu/mms/sdc/sitl/files/api/v1/file_info/ancillary?sc_id=mms'+probe_id+'&product='+product+dates_for_query

                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=ResourceWarning)
                    http_request = sdc_session.get(url, verify=True)
                    http_json = http_request.json()

                # since predicted doesn't support start_date/end_date, we'll need to parse the correct dates
                if level != 'def':
                    for file in http_json['files']:
                        # first, remove the dates that start after the end of the trange
                        if time_double(file['start_date']) > endtime_day:
                            continue
                        # now remove files that end before the start of the trange
                        if start_time > time_double(file['end_date']):
                            continue
                        files_in_interval.append(file)
                        break
                else:
                    files_in_interval = http_json['files']

                for file in files_in_interval:
                    out_file = os.sep.join([out_dir, file['file_name']])

                    if os.path.exists(out_file) and str(os.stat(out_file).st_size) == str(file['file_size']):
                        out_files.append(out_file)
                        http_request.close()
                        continue

                    if user == None:
                        download_url = 'https://lasp.colorado.edu/mms/sdc/public/files/api/v1/download/ancillary?file=' + file['file_name']
                    else:
                        download_url = 'https://lasp.colorado.edu/mms/sdc/sitl/files/api/v1/download/ancillary?file=' + file['file_name']

                    logging.info('Downloading ' + file['file_name'] + ' to ' + out_dir)

                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", category=ResourceWarning)
                        fsrc = sdc_session.get(download_url, stream=True, verify=True)

                    ftmp = NamedTemporaryFile(delete=False)

                    with open(ftmp.name, 'wb') as f:
                        copyfileobj(fsrc.raw, f)

                    if not os.path.exists(out_dir):
                        os.makedirs(out_dir)

                    # if the download was successful, copy to data directory
                    copy(ftmp.name, out_file)
                    out_files.append(out_file)
                    fsrc.close()
                    ftmp.close()

            if download_only:
                continue

            # if no files are found remotely, try locally
            if out_files == []:
                out_files = mms_get_local_state_files(probe=probe_id, level=level, filetype=filetype, trange=[start_time_str, end_time_str])

            if filetype == 'eph':
                mms_load_eph_tplot(sorted(out_files), level=level, probe=probe_id, datatypes=datatypes, suffix=suffix, trange=trange)
            elif filetype == 'att':
                mms_load_att_tplot(sorted(out_files), level=level, probe=probe_id, datatypes=datatypes, suffix=suffix, trange=trange)

    if not no_download:
        sdc_session.close()
