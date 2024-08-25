import logging
import numpy as np
from fnmatch import fnmatch
from pytplot import get_data, store_data, options
from pytplot import time_datetime


def mms_fpi_make_compressionlossbars(tname, lossy=False):
    """
    Creates FPI's compressionloss flag bars

    Parameters
    -----------
        tname: str
            Tplot variable name of DIS or DES compressionloss data

        lossy: bool
            The value for lossy compression (use this keyword only for special case)

    Flag
    -----------
        0: Lossless compression
        1: Lossy compression
      In old files (v2.1.0 or older until the end of Phase 1A)
        1: Lossless compression
        3: Lossy compression

    Notes
    -----------
        In cases when data had been lossy compressed, some artifacts may appear in the data due to the compression.
        Since all of fast survey data are lossy compressed, it is not necessary to make this bar for fast survey data.

    Returns
    ------------
        List of the tplot variables created.

    """
    if fnmatch(tname, 'mms?_dis*'):
        instrument = 'DIS'
    elif fnmatch(tname, 'mms?_des*'):
        instrument = 'DES'
    else:
        logging.error('Unable to determine instrument from variable name.')
        return

    if instrument == 'DES':
        colors = 'red'
    else:
        colors = 'blue'

    if fnmatch(tname, '*_fast*'):
        logging.info('All fast survey data are lossy compressed, so there is no need to create this bar.')
        return
    elif fnmatch(tname, '*_brst*'):
        data_rate = 'Brst'
    else:
        logging.error('Unable to determine data rate from variable name.')
        return

    data = get_data(tname, dt=True)
    metadata = get_data(tname, metadata=True)

    if data is None:
        logging.error('Problem reading the variable: ' + tname)
        return

    flagline = np.zeros(len(data.times))

    if not lossy:
        file_id = metadata['CDF']['GATT']['Logical_file_id']
        if isinstance(file_id, list):  # Workaround for cdflib bug in globalattsget
            file_id = file_id[0]
        version = file_id.split('_v')[1].split('.')
        if version[0] == '2':
            if version[1] == '1':
                if data.times[0] < time_datetime('2016-04-01'):
                    lossy = 3
                else:
                    lossy = 1
            else:
                if float(version[1]) > 1:
                    lossy = 1
                else:
                    lossy = 3
        else:
            if float(version[0]) > 2:
                lossy = 1
            else:
                lossy = 3

        for j in range(len(data.times)):
            if data.y[j] != lossy:
                flagline[j] = np.nan
            else:
                flagline[j] = 0.5

        store_data(tname + '_flagbars', data={'x': data.times, 'y': flagline})
        options(tname + '_flagbars', 'yrange', [0, 1])
        options(tname + '_flagbars', 'panel_size', 0.2)
        options(tname + '_flagbars', 'symbols', True)
        options(tname + '_flagbars', 'markers', 's')
        options(tname + '_flagbars', 'thick', 4)
        options(tname + '_flagbars', 'border', False)

        return [tname + '_flagbars']
