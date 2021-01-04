

import numpy as np
from pyspedas import time_string, time_double
import os
from datetime import datetime

def dailynames(directory='', trange=None, res=24*3600., hour_res=False, file_format='%Y%m%d', prefix='', suffix=''):
    '''
    Creates a list of file names using a time range, resoution and file format
    Based on Davin Larson's file_dailynames in IDL SPEDAS

    Parameters:
        directory: str
            String containing the directory for the generated file names

        trange: list of str, list of datetime or list of floats
            Two-element list containing the start and end times for the file names

        res: float
            File name resolution in seconds (default: 24*3600., i.e., daily)

        file_format: str
            Format of the file names using strftime directives; for reference: https://strftime.org
            (default: %Y%m%d, i.e., daily)

        prefix: str
            file name prefix

        suffix: str
            file name suffix

    Returns:
        List containing filenames

    '''
    if trange == None:
        print('No trange specified')
        return

    if hour_res == True:
        res = 3600.
        file_format = '%Y%m%d%H'

    # allows the user to pass in trange as list of datetime objects
    if type(trange[0]) == datetime and type(trange[1]) == datetime:
        trange = [time_string(trange[0].timestamp()), time_string(trange[1].timestamp())]

    tr = [trange[0], trange[1]]
    
    if isinstance(trange[0], str):
        tr[0] = time_double(trange[0])
    if isinstance(trange[1], str):
        tr[1] = time_double(trange[1])

    # Davin's magic heisted from file_dailynames in IDL
    mmtr = [np.floor(tr[0]/res), np.ceil(tr[1]/res)]

    if mmtr[1]-mmtr[0] < 1:
        n = 1
    else:
        n = int(mmtr[1]-mmtr[0])

    times = [(float(num)+mmtr[0])*res for num in range(n)]

    dates = []
    files = []
        
    for time in times:
        if time_string(time, fmt=file_format) not in dates:
            dates.append(time_string(time, fmt=file_format))
            
    for date in dates:
        files.append(directory + prefix + date + suffix)

    return files