import os
import fnmatch
import glob
import re
import logging
import pandas as pd

from pyspedas import time_double
from pyspedas.mms.mms_config import CONFIG

def mms_get_local_state_files(probe='1', level='def', filetype='eph', trange=None):
    """
    Search for local state MMS files in case a list cannot be retrieved from the
    remote server.  Returns a sorted list of file paths.
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
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
    dir_pattern = os.sep.join([CONFIG['local_data_dir'], 'ancillary', 'mms'+probe, level+filetype])
    file_pattern = 'MMS'+probe+'_'+level.upper()+filetype.upper()+'_'+'???????_???????.V??'

    files_in_trange = []
    out_files = []

    files = glob.glob(os.sep.join([dir_pattern, file_pattern]))

    # find the files within the trange
    file_regex = re.compile(os.sep.join([dir_pattern, 'MMS'+probe+'_'+level.upper()+filetype.upper()+'_([0-9]{7})_([0-9]{7}).V[0-9]{2}']))
    for file in files:
        time_match = file_regex.match(file)
        if time_match != None:
            start_time = pd.to_datetime(time_match.group(1), format='%Y%j').timestamp()
            end_time = pd.to_datetime(time_match.group(2), format='%Y%j').timestamp()
            if start_time < time_double(trange[1]) and end_time >= time_double(trange[0]):
                files_in_trange.append(file)

    # ensure only the latest version of each file is loaded
    for file in files_in_trange:
        this_file = file[0:-3] + 'V??'
        versions = fnmatch.filter(files_in_trange, this_file)
        if len(versions) > 1:
            out_files.append(sorted(versions)[-1]) # only grab the latest version
        else:
            out_files.append(versions[0])

    return list(set(out_files))