

import os
import re
from .mms_config import CONFIG
from .mms_files_in_interval import mms_files_in_interval

from dateutil.rrule import rrule, DAILY
from dateutil.parser import parse

from datetime import timedelta

def mms_get_local_files(probe, instrument, data_rate, level, datatype, trange):
# directory and file name search patterns
#   -assume directories are of the form:
#      (srvy, SITL): spacecraft/instrument/rate/level[/datatype]/year/month/
#      (brst): spacecraft/instrument/rate/level[/datatype]/year/month/day/
#   -assume file names are of the form:
#      spacecraft_instrument_rate_level[_datatype]_YYYYMMDD[hhmmss]_version.cdf

    files_out = []

    file_name = 'mms'+probe+'_'+instrument+'_'+data_rate+'_'+level+'(_)?.*_([0-9]{8,14})_v(\d+).(\d+).(\d+).cdf'

    days = rrule(DAILY, dtstart=parse(parse(trange[0]).strftime('%Y-%m-%d')), until=parse(trange[1])-timedelta(seconds=1))

    if datatype == '' or datatype == None:
        level_and_dtype = level
    else:
        level_and_dtype = os.sep.join([level, datatype])

    for date in days:
        if data_rate == 'brst':
            local_dir = os.sep.join([CONFIG['local_data_dir'], 'mms', 'mms'+probe, instrument, data_rate, level_and_dtype, date.strftime('%Y'), date.strftime('%m'), date.strftime('%d')])
        else:
            local_dir = os.sep.join([CONFIG['local_data_dir'], 'mms', 'mms'+probe, instrument, data_rate, level_and_dtype, date.strftime('%Y'), date.strftime('%m')])

        if os.name == 'nt':
            full_path = os.sep.join([re.escape(local_dir)+os.sep, file_name])
        else:
            full_path = os.sep.join([re.escape(local_dir), file_name])

        regex = re.compile(full_path)
        for root, dirs, files in os.walk(os.sep.join([CONFIG['local_data_dir'], 'mms'])):
            for file in files:
                this_file = os.sep.join([root, file])
                
                #print('--- ' + this_file)
                matches = regex.match(this_file)
                if matches:
                    this_time = parse(matches.groups()[1])
                    if this_time >= parse(parse(trange[0]).strftime('%Y-%m-%d')) and this_time <= parse(trange[1])-timedelta(seconds=1):
                        if this_file not in files_out:
                            files_out.append({'file_name': file, 'timetag': '', 'full_name': this_file})

    files_in_interval = mms_files_in_interval(files_out, trange)

    local_files = []

    file_names = [f['file_name'] for f in files_in_interval]

    for file in files_out:
        if file['file_name'] in file_names:
            local_files.append(file['full_name'])

    return local_files
