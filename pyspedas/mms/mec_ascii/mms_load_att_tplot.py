
import logging
import pandas as pd
import numpy as np

from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import store_data, options

def mms_load_att_tplot(filenames, level='def', probe='1', datatypes=['spinras', 'spindec'], suffix='', trange=None):
    """
    Helper routine for loading state data (ASCII files from the SDC); not meant to be called directly; see pyspedas.mms.state instead
    
    """
    prefix = 'mms' + probe

    file_times = []
    file_lras = []
    file_ldecs = []
    tvalues = {}

    for file in filenames:
        rows = pd.read_csv(file, delim_whitespace=True, header=None, skiprows=49)

        times = rows.shape[0]-1
        time_values = np.empty(times)
        lra_values = np.empty(times)
        ldec_values = np.empty(times)

        for time_idx in range(0, times):
            # these files can overlap, so avoid duplicates
            if tvalues.get(time_values[time_idx]):
                continue
            time_values[time_idx] = pd.to_datetime(rows[0][time_idx], format='%Y-%jT%H:%M:%S.%f').timestamp()
            tvalues[time_values[time_idx]] = 1
            lra_values[time_idx] = rows[13][time_idx]
            ldec_values[time_idx] = rows[14][time_idx]

        file_times.append(time_values)
        file_lras.append(lra_values)
        file_ldecs.append(ldec_values)

    if 'spinras' in datatypes:
        store_data(prefix + '_' + level + 'att_spinras' + suffix, data={'x': np.concatenate(file_times), 'y': np.concatenate(file_lras)})
        tclip(prefix + '_' + level + 'att_spinras' + suffix, trange[0], trange[1], suffix='')

    if 'spindec' in datatypes:
        store_data(prefix + '_' + level + 'att_spindec' + suffix, data={'x': np.concatenate(file_times), 'y': np.concatenate(file_ldecs)})
        tclip(prefix + '_' + level + 'att_spindec' + suffix, trange[0], trange[1], suffix='')

