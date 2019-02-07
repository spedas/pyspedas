#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import requests
import logging
from ..spdtplot.cdf_to_tplot import cdf_to_tplot
from pyspedas import time_double, time_string
from dateutil.parser import parse
from datetime import timedelta, datetime
from urllib.request import urlopen
from shutil import copyfileobj, copy
from tempfile import NamedTemporaryFile
from .mms_config import CONFIG

logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def mms_load_data(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', instrument='fgm', datatype='', prefix='', suffix='', get_support_data=False):
    """
    This function loads MMS data into tplot variables
    """

    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(level, list): level = [level]
    if not isinstance(datatype, list): datatype = [datatype]
    
    start_date = parse(trange[0]).strftime('%Y-%m-%d-%H-%M-%S')
    end_date = parse(time_string(time_double(trange[1])-0.1)).strftime('%Y-%m-%d-%H-%M-%S')

    out_files = []

    for prb in probe:
        for drate in data_rate:
            for lvl in level:
                for dtype in datatype:
                    url = 'https://lasp.colorado.edu/mms/sdc/public/files/api/v1/file_info/science?start_date=' + start_date + '&end_date=' + end_date + '&sc_id=mms' + prb + '&instrument_id=' + instrument + '&data_rate_mode=' + drate + '&data_level=' + lvl

                    if dtype != '':
                        url = url + '&descriptor=' + dtype

                    # query list of available files
                    http_json = requests.get(url).json()

                    for file in http_json['files']:
                        file_date = parse(file['timetag'])
                        out_dir = CONFIG['local_data_dir'] + os.sep.join(['mms', 'mms'+prb, instrument, drate, lvl, file_date.strftime('%Y'), file_date.strftime('%m')])
                        out_file = os.sep.join([out_dir, file['file_name']])

                        if os.path.exists(out_file):
                            logging.info('Loading ' + out_file)
                            out_files.append(out_file)
                            continue

                        download_url = 'https://lasp.colorado.edu/mms/sdc/public/files/api/v1/download/science?file=' + file['file_name']
                        logging.info('Downloading ' + file['file_name'] + ' to ' + out_dir)
                        fsrc = urlopen(download_url)
                        ftmp = NamedTemporaryFile(delete=False)
                        copyfileobj(fsrc, ftmp)

                        if not os.path.exists(out_dir):
                            os.makedirs(out_dir)

                        # if the download was successful, copy to data directory
                        copy(ftmp.name, out_file)
                        out_files.append(out_file)

    out_files = sorted(out_files)

    new_variables = cdf_to_tplot(out_files, merge=True, get_support_data=get_support_data, prefix=prefix, suffix=suffix)

    logging.info('Loaded variables:')
    for new_var in new_variables:
        print(new_var)

    return new_variables

