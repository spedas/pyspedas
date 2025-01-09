import os
import fnmatch
import glob
import logging
import pandas as pd
from pyspedas.projects.mms.mms_config import CONFIG

from pyspedas.utilities.download import is_fsspec_uri
import fsspec

def mms_get_local_state_files(probe='1', level='def', filetype='eph', trange=None):
    """
    Search for local state MMS files in case a list cannot be retrieved from the
    remote server.  Returns a sorted list of file paths.
    
    Parameters:
        trange : list of str
            time range of interest [start time, end time] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str
            probe #, e.g., '4' for MMS4
    
        level: str
            state data level; either 'def' (for definitive) or 'pred' (for predicted)

        filetype: str
            state file type, e.g. 'eph' (for ephemeris) or 'att' (for attitude)

    Returns:
        List of local files found matching the input parameters.

    """
    if trange is None:
        logging.info('No trange specified in mms_get_local_state_files')
        return

    # directory and file name search patterns
    # For now
    # -all ancillary data is in one directory:
    #       mms\ancillary
    # -assume file names are of the form:
    #   SPACECRAFT_FILETYPE_startDate_endDate.version
    #   where SPACECRAFT is [MMS1, MMS2, MMS3, MMS4] in uppercase
    #   and FILETYPE is either DEFATT, PREDATT, DEFEPH, PREDEPH in uppercase
    #   and start/endDate is YYYYDOY
    #   and version is Vnn (.V00, .V01, etc..)
    sep = "/" if is_fsspec_uri(CONFIG["local_data_dir"]) else os.path.sep
    dir_pattern = sep.join([CONFIG['local_data_dir'], 'ancillary', f'mms{probe}', f'{level}{filetype}'])
    file_pattern = f'MMS{probe}_{level.upper()}{filetype.upper()}_???????_???????.V??'

    files_in_trange = []
    out_files = []

    if is_fsspec_uri(dir_pattern):
        protocol, path = dir_pattern.split("://")
        fs = fsspec.filesystem(protocol)

        files = fs.glob(sep.join([dir_pattern, file_pattern]))
        files = [sep.join([protocol+"://", file]) for file in files]
    else:
        files = glob.glob(sep.join([dir_pattern, file_pattern]))

    for file in files:
        filename = os.path.basename(file) if not is_fsspec_uri(dir_pattern) else file.split("/")[-1]
        try:
            date_parts = filename.split('_')
            start_time_str = date_parts[2]
            end_time_str = date_parts[3].split('.')[0]
            
            start_time = pd.to_datetime(start_time_str, format='%Y%j').timestamp()
            end_time = pd.to_datetime(end_time_str, format='%Y%j').timestamp()
            
            if start_time < pd.Timestamp(trange[1]).timestamp() and end_time >= pd.Timestamp(trange[0]).timestamp():
                files_in_trange.append(file)
        except IndexError:
            continue

    # ensure only the latest version of each file is loaded
    for file in files_in_trange:
        this_file = file[0:-3] + 'V??'
        versions = fnmatch.filter(files_in_trange, this_file)
        if len(versions) > 1:
            out_files.append(sorted(versions)[-1]) # only grab the latest version
        else:
            out_files.append(versions[0])

    return list(set(out_files))
