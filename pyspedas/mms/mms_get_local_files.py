

import os
import re
from .mms_config import CONFIG

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

    days = rrule(DAILY, dtstart=parse(trange[0]), until=parse(trange[1])-timedelta(seconds=1))

    if datatype == '' or datatype == None:
        level_and_dtype = level
    else:
        level_and_dtype = os.sep.join([level, datatype])

    for date in days:
        if data_rate == 'brst':
            local_dir = os.sep.join([CONFIG['local_data_dir'], 'mms', 'mms'+probe, instrument, data_rate, level_and_dtype, date.strftime('%Y'), date.strftime('%m'), date.strftime('%d')])
        else:
            local_dir = os.sep.join([CONFIG['local_data_dir'], 'mms', 'mms'+probe, instrument, data_rate, level_and_dtype, date.strftime('%Y'), date.strftime('%m')])

        full_path = os.sep.join([local_dir, file_name])
        # /Users/eric/data/mms/mms1/fgm/srvy/l2/2015/12/mms1_fgm_srvy_l2_20151215_v4.18.0.cdf

        regex = re.compile(full_path)
        for root, dirs, files in os.walk(os.sep.join([CONFIG['local_data_dir'], 'mms'])):
            for file in files:
                this_file = os.sep.join([root, file])
                #print('--- ' + this_file)
                matches = regex.match(this_file)
                if matches:
                    this_time = parse(matches.groups()[1])
                    if this_time >= parse(trange[0]) and this_time <= parse(trange[1])-timedelta(seconds=1):
                        if this_file not in files_out:
                            files_out.append(this_file)
    return files_out
