
import logging
import pandas as pd
import numpy as np

from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import store_data, options

def mms_load_eph_tplot(filenames, level='def', probe='1', datatypes=['pos', 'vel'], suffix='', trange=None):
    """
    Helper routine for loading state data (ASCII files from the SDC); not meant to be called directly; see pyspedas.mms.state instead
    
    """
    prefix = 'mms' + probe

    time_values = []
    date_values = []
    x_values = []
    y_values = []
    z_values = []
    vx_values = []
    vy_values = []
    vz_values = []

    for file in filenames:
        logging.info('Loading ' + file)
        rows = pd.read_csv(file, delim_whitespace=True, header=None, skiprows=14)
        times = rows.shape[0]-1
        for time_idx in range(0, times):
            # these files can overlap, so avoid duplicates
            if rows[0][time_idx] in date_values:
                continue
            time_values.append(pd.to_datetime(rows[0][time_idx], format='%Y-%j/%H:%M:%S.%f').timestamp())
            x_values.append(rows[2][time_idx])
            y_values.append(rows[3][time_idx])
            z_values.append(rows[4][time_idx])
            vx_values.append(rows[5][time_idx])
            vy_values.append(rows[6][time_idx])
            vz_values.append(rows[7][time_idx])
            date_values.append(rows[0][time_idx])

    if 'pos' in datatypes:
        store_data(prefix + '_' + level + 'eph_pos' + suffix, data={'x': time_values, 'y': np.transpose(np.array([x_values, y_values, z_values]))})
        tclip(prefix + '_' + level + 'eph_pos' + suffix, trange[0], trange[1], suffix='')
        options(prefix + '_' + level + 'eph_pos' + suffix, 'ytitle', 'MMS'+str(probe)+' position')
        options(prefix + '_' + level + 'eph_pos' + suffix, 'ysubtitle', '[km]')
        options(prefix + '_' + level + 'eph_pos' + suffix, 'legend_names', ['X ECI', 'Y ECI', 'Z ECI'])
        options(prefix + '_' + level + 'eph_pos' + suffix, 'color', ['b', 'g', 'r'])

    if 'vel' in datatypes:
        store_data(prefix + '_' + level + 'eph_vel' + suffix, data={'x': time_values, 'y': np.transpose(np.array([vx_values, vy_values, vz_values]))})
        tclip(prefix + '_' + level + 'eph_vel' + suffix, trange[0], trange[1], suffix='')
        options(prefix + '_' + level + 'eph_vel' + suffix, 'ytitle', 'MMS'+str(probe)+' velocity')
        options(prefix + '_' + level + 'eph_vel' + suffix, 'ysubtitle', '[km/s]')
        options(prefix + '_' + level + 'eph_vel' + suffix, 'legend_names', ['Vx ECI', 'Vy ECI', 'Vz ECI'])
        options(prefix + '_' + level + 'eph_vel' + suffix, 'color', ['b', 'g', 'r'])

