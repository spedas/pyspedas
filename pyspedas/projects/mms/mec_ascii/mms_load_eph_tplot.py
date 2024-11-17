import logging
import pandas as pd
import numpy as np
from pytplot import time_clip as tclip
from pytplot import store_data, options


def mms_load_eph_tplot(filenames, level='def', probe='1', datatypes=['pos', 'vel'], suffix='', trange=None):
    """
    Helper routine for loading state data (ASCII files from the SDC); not meant to be called directly; see pyspedas.projects.mms.state instead
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
        rows = pd.read_csv(file, sep=r'\s+', header=None, skiprows=14)
        times = rows.shape[0]
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

    return_vars = []
    if 'pos' in datatypes:
        posvar = prefix + '_' + level + 'eph_pos' + suffix
        store_data(posvar, data={'x': time_values, 'y': np.transpose(np.array([x_values, y_values, z_values]))})
        tclip(posvar, trange[0], trange[1], suffix='')
        options(posvar, 'ytitle', 'MMS'+str(probe)+' position')
        options(posvar, 'ysubtitle', '[km]')
        options(posvar, 'legend_names', ['X ECI', 'Y ECI', 'Z ECI'])
        return_vars.append(posvar)

    if 'vel' in datatypes:
        velvar = prefix + '_'  + level + 'eph_vel' + suffix
        store_data(velvar, data={'x': time_values, 'y': np.transpose(np.array([vx_values, vy_values, vz_values]))})
        tclip(velvar, trange[0], trange[1], suffix='')
        options(velvar, 'ytitle', 'MMS'+str(probe)+' velocity')
        options(velvar, 'ysubtitle', '[km/s]')
        options(velvar, 'legend_names', ['Vx ECI', 'Vy ECI', 'Vz ECI'])
        return_vars.append(velvar)

    return return_vars
