import logging
import pandas as pd
import numpy as np
from pytplot import time_clip as tclip
from pytplot import store_data, options


def mms_load_qf_tplot(filenames, suffix='', trange=None):
    """
    Helper routine for loading tetrahedron quality factor data (ASCII files from the SDC); not meant to be called directly
    """
    prefix = 'mms'

    time_values = []
    date_values = []
    qf_values = []

    for file in filenames:
        logging.info('Loading ' + file)
        rows = pd.read_csv(file, sep=r'\s+', header=None, skiprows=11)
        times = rows.shape[0]
        for time_idx in range(0, times):
            # these files can overlap, so avoid duplicates
            if rows[0][time_idx] in date_values:
                continue
            time_values.append(pd.to_datetime(rows[0][time_idx], format='%Y-%j/%H:%M:%S.%f').timestamp())
            qf_values.append(rows[2][time_idx])
            date_values.append(rows[0][time_idx])

    tp_name=prefix + '_' + 'tetrahedron_qf' + suffix
    store_data(tp_name, data={'x': np.array(time_values), 'y': np.array(qf_values)})
    tclip(tp_name, trange[0], trange[1], suffix='')
    options(tp_name, 'ytitle', 'MMS Tetrahedron Quality Factor')
    options(tp_name, 'legend_names', 'qf')
    return [tp_name]

