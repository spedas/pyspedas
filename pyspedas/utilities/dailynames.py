

import numpy as np
from pyspedas import time_string, time_double
import os

def dailynames(directory='', trange=None, res=24*3600., hour_res=False, file_format='%Y%m%d', prefix='', suffix=''):
    if trange == None:
        print('No trange specified')
        return

    if hour_res == True:
        res = 3600.
        file_format = '%Y%m%d%H'

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