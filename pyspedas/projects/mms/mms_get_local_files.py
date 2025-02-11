import logging
import os
import re
import shutil
from .mms_config import CONFIG
from .mms_files_in_interval import mms_files_in_interval
from dateutil.rrule import rrule, DAILY
from dateutil.parser import parse
from datetime import timedelta

from pyspedas.utilities.download import is_fsspec_uri
import fsspec

def mms_get_local_files(probe, instrument, data_rate, level, datatype, trange, mirror=False):
    """
    Search for local MMS files in case a list cannot be retrieved from the
    remote server.  
    
    Parameters
    ------------
        probe: str
            probe #, e.g., '4' for MMS4

        instrument: str
            instrument name, e.g., 'fpi' or 'fgm'

        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst'

        level: str
            data level, e.g., 'l2'

        datatype: str
            'electron' or 'ion'

        trange: list of str
            two-element array containing the start and end date/times

        mirror: bool
            if True, copy files from network mirror to local data directory

    Returns
    ---------
        List of file paths.
    """
    files_out = []

    if mirror:
        if CONFIG.get('mirror_data_dir') is not None:
            data_dir = CONFIG['mirror_data_dir']
        else:
            return []
    else:
        data_dir = CONFIG['local_data_dir']

    sep = "/" if is_fsspec_uri(data_dir) else os.path.sep

    # directory and file name search patterns
    #   -assume directories are of the form:
    #      (srvy, SITL): spacecraft/instrument/rate/level[/datatype]/year/month/
    #      (brst): spacecraft/instrument/rate/level[/datatype]/year/month/day/
    #   -assume file names are of the form:
    #      spacecraft_instrument_rate_level[_datatype]_YYYYMMDD[hhmmss]_version.cdf

    file_name = 'mms'+probe+'_'+instrument+'_'+data_rate+'_'+level+r'(_)?.*_([0-9]{8,14})_v(\d+).(\d+).(\d+).cdf'

    days = rrule(DAILY, dtstart=parse(parse(trange[0]).strftime('%Y-%m-%d')), until=parse(trange[1])-timedelta(seconds=1))

    if datatype == '' or datatype is None:
        level_and_dtype = level
    else:
        level_and_dtype = sep.join([level, datatype])

    for date in days:
        if data_rate == 'brst':
            local_dir = sep.join([data_dir, 'mms'+probe, instrument, data_rate, level_and_dtype, date.strftime('%Y'), date.strftime('%m'), date.strftime('%d')])
        else:
            local_dir = sep.join([data_dir, 'mms'+probe, instrument, data_rate, level_and_dtype, date.strftime('%Y'), date.strftime('%m')])

        if os.name == 'nt':
            full_path = sep.join([re.escape(local_dir)+os.sep, file_name])
        else:
            full_path = sep.join([re.escape(local_dir), file_name])

        # check for extra /'s in the path
        if '//' in full_path:
            full_path = full_path.replace('//', '/')
        if is_fsspec_uri(data_dir):
            # Cloud Awareness: the replacement above removes the expected :// URI pattern
            full_path = full_path.replace(":/", "://")

            protocol, path = data_dir.split("://")
            fs = fsspec.filesystem(protocol)

            walk = fs.walk(data_dir)
        else:
            walk = os.walk(data_dir)

        regex = re.compile(full_path)
        for root, dirs, files in walk:
            for file in files:
                this_file = sep.join([root, file])
                if is_fsspec_uri(data_dir):
                    this_file = protocol + "://" + this_file
                if CONFIG['debug_mode']: logging.info('Checking ' + this_file)
                if CONFIG['debug_mode']: logging.info('against: ' + full_path)
                
                matches = regex.match(this_file)
                if matches:
                    this_time = parse(matches.groups()[1])
                    if this_time >= parse(parse(trange[0]).strftime('%Y-%m-%d')) and this_time <= parse(trange[1])-timedelta(seconds=1):
                        if not any(this_file == f['full_name'] for f in files_out):
                            files_out.append({'file_name': file, 'timetag': '', 'full_name': this_file, 'file_size': ''})

    files_in_interval = mms_files_in_interval(files_out, trange)

    local_files = []

    file_names = [f['file_name'] for f in files_in_interval]

    for file in files_out:
        if file['file_name'] in file_names:
            local_files.append(file['full_name'])

    if mirror:
        mirror_dir = CONFIG['mirror_data_dir']
        local_dir = CONFIG['local_data_dir']
        local_files_copied = []
        # need to copy files from network mirror to local data directory
        for file in local_files:
            local_file = file.replace(mirror_dir, local_dir)
            if CONFIG['debug_mode']:
                logging.info('Copying ' + file + ' to ' + local_file)
            if is_fsspec_uri(local_dir):
                protocol, path = local_dir.split("://")
                fs.fsspec.filesystem(protocol)

                fs.put_file(file, local_file)
            else:
                shutil.copyfile(file, local_file)
            local_files_copied.append(local_file)
        local_files = local_files_copied

    for file in local_files:
        logging.info('Loading: ' + file)

    return local_files
