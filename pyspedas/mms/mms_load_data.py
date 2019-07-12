#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import requests
import logging
import numpy as np
from ..spdtplot.cdf_to_tplot import cdf_to_tplot
from ..analysis.time_clip import time_clip as tclip
from pyspedas import time_double, time_string
from dateutil.parser import parse
from datetime import timedelta, datetime
from shutil import copyfileobj, copy
from tempfile import NamedTemporaryFile
from .mms_config import CONFIG
from .mms_get_local_files import mms_get_local_files
from .mms_files_in_interval import mms_files_in_interval
from .mms_login_lasp import mms_login_lasp

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def mms_load_data(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', 
    instrument='fgm', datatype='', varformat=None, prefix='', suffix='', get_support_data=False, time_clip=False, 
    no_update=False, center_measurement=False, available=False, notplot=False):
    """
    This function loads MMS data into pyTplot variables
    """

    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(level, list): level = [level]
    if not isinstance(datatype, list): datatype = [datatype]
    
    probe = [str(p) for p in probe]

    # allows the user to pass in trange as list of datetime objects
    if type(trange[0]) == datetime and type(trange[1]) == datetime:
        trange = [time_string(trange[0].timestamp()), time_string(trange[1].timestamp())]
        
    start_date = parse(trange[0]).strftime('%Y-%m-%d') # need to request full day, then parse out later
    end_date = parse(time_string(time_double(trange[1])-0.1)).strftime('%Y-%m-%d-%H-%M-%S') # -1 second to avoid getting data for the next day

    download_only = CONFIG['download_only']

    no_download = False
    if no_update or CONFIG['no_download']: no_download = True

    user = None
    if not no_download:
        sdc_session, user = mms_login_lasp()

    out_files = []
    available_files = []

    for prb in probe:
        for drate in data_rate:
            for lvl in level:
                for dtype in datatype:
                    if user is None:
                        url = 'https://lasp.colorado.edu/mms/sdc/public/files/api/v1/file_info/science?start_date=' + start_date + '&end_date=' + end_date + '&sc_id=mms' + prb + '&instrument_id=' + instrument + '&data_rate_mode=' + drate + '&data_level=' + lvl
                    else:
                        url = 'https://lasp.colorado.edu/mms/sdc/sitl/files/api/v1/file_info/science?start_date=' + start_date + '&end_date=' + end_date + '&sc_id=mms' + prb + '&instrument_id=' + instrument + '&data_rate_mode=' + drate + '&data_level=' + lvl
                    
                    if dtype != '':
                        url = url + '&descriptor=' + dtype

                    if CONFIG['debug_mode']: logging.info('Fetching: ' + url)

                    if no_download == False:
                        # query list of available files
                        try:
                            http_json = sdc_session.get(url, verify=True).json()

                            if CONFIG['debug_mode']: logging.info('Filtering the results down to your trange')

                            files_in_interval = mms_files_in_interval(http_json['files'], trange)

                            if available:
                                for file in files_in_interval:
                                    logging.info(file['file_name'] + ' (' + str(np.round(file['file_size']/(1024.*1024), decimals=1)) + ' MB)')
                                    available_files.append(file['file_name'])
                                continue

                            for file in files_in_interval:
                                file_date = parse(file['timetag'])
                                if dtype == '':
                                    out_dir = os.sep.join([CONFIG['local_data_dir'], 'mms'+prb, instrument, drate, lvl, file_date.strftime('%Y'), file_date.strftime('%m')])
                                else:
                                    out_dir = os.sep.join([CONFIG['local_data_dir'], 'mms'+prb, instrument, drate, lvl, dtype, file_date.strftime('%Y'), file_date.strftime('%m')])

                                if drate.lower() == 'brst':
                                    out_dir = os.sep.join([out_dir, file_date.strftime('%d')])

                                out_file = os.sep.join([out_dir, file['file_name']])

                                if CONFIG['debug_mode']: logging.info('File: ' + file['file_name'] + ' / ' + file['timetag'])

                                if os.path.exists(out_file) and str(os.stat(out_file).st_size) == str(file['file_size']):
                                    if not download_only: logging.info('Loading ' + out_file)
                                    out_files.append(out_file)
                                    continue

                                if user is None:
                                    download_url = 'https://lasp.colorado.edu/mms/sdc/public/files/api/v1/download/science?file=' + file['file_name']
                                else:
                                    download_url = 'https://lasp.colorado.edu/mms/sdc/sitl/files/api/v1/download/science?file=' + file['file_name']

                                logging.info('Downloading ' + file['file_name'] + ' to ' + out_dir)

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
                        except requests.exceptions.ConnectionError:
                            # No/bad internet connection; try loading the files locally
                            logging.error('No internet connection!')

                    
                    if out_files == []:
                        if not download_only: logging.info('Searching for local files...')
                        out_files = mms_get_local_files(prb, instrument, drate, lvl, dtype, trange)

    if not no_download:
        sdc_session.close()

    if available:
        return available_files

    if not download_only:
        out_files = sorted(out_files)

        new_variables = cdf_to_tplot(out_files, varformat=varformat, merge=True, get_support_data=get_support_data, prefix=prefix, suffix=suffix, center_measurement=center_measurement, notplot=notplot)

        if notplot:
            return new_variables

        if new_variables == []:
            logging.warning('No data loaded.')
            return

        logging.info('Loaded variables:')
        for new_var in new_variables:
            print(new_var)

            if time_clip:
                tclip(new_var, trange[0], trange[1], suffix='')

        return new_variables
    else:
        return out_files





