import numpy as np
from pytplot import store_data, options
from pytplot import time_double
from pyspedas.cotrans_tools.xyz_to_polar import xyz_to_polar
from .load_csv_file import load_csv_file


# This routine was originally in akebono/__init__.py.  If you need to see the history of this routine before
# it was moved to its own file, please check the history for __init__.py.

def orb_postprocessing(files, prefix='', suffix=''):
    """
    Load the orbit CSV files and create the tplot variables

    Parameters
    ----------
    files: list of str
        List of CSV files to convert to tplot variables
    prefix: str
         A prefix to be added to the tplot variables created. Default: ''
    suffix: str
        A suffix to be added to the tplot variables created. Default: ''

    Returns
    -------
    list of str
        List of tplot variables created.
    """

    if prefix is None:
        user_prefix = ''
    else:
        user_prefix = prefix

    if suffix is None:
        suffix = ''

    prefix_project = 'akb_'
    prefix_descriptor = 'orb_'
    prefix = user_prefix + prefix_project + prefix_descriptor

    cols = ['pass','ut', 'ksc_azm', 'ksc_elv', 'ksc_dis', 'ksc_ang', 'syo_azm', 'syo_elv', 'syo_dis', 'syo_ang',
            'pra_azm', 'pra_elv', 'pra_dis', 'pra_ang', 'esr_azm', 'esr_elv', 'esr_dis', 'esr_ang', 'gclat','gclon',
            'inv', 'fmlat', 'mlat', 'mlt', 'bmdl_x', 'bmdl_y', 'bmdl_z', 'xxlon_sc', 'xxlat_sc', 'aheight','lsun',
            's_direc_x', 's_direc_y', 's_direc_z', 'sc_pos_x', 'sc_pos_y', 'sc_pos_z', 'sc_vel_x', 'sc_vel_y', 'sc_vel_z']

    try:
        data = load_csv_file(files, cols=cols)
    except UnicodeDecodeError:
        data = load_csv_file(files, cols=cols, gz=True)
    values = data.to_numpy()
    unix_times = time_double([date[2:4] + '-' + date[4:6] + '-' + date[0:2] + '/' + date[6:8] + ':' + date[8:10] + ':' + date[10:12] for date in data['ut']])

    km_in_re = 6374.4

    xyz = np.array([[data['sc_pos_x']], [data['sc_pos_y']], [data['sc_pos_z']]]).transpose([2, 0, 1]).squeeze()
    xyz = np.float64(xyz)
    xyz_re = xyz/km_in_re
    r_theta_phi = xyz_to_polar(xyz)
    rr = r_theta_phi[:, 0]
    th = r_theta_phi[:, 1]
    ph = r_theta_phi[:, 2]
    store_data(prefix + 'geo' + suffix, data={'x': unix_times, 'y': xyz_re})
    store_data(prefix + 'gdlat' + suffix, data={'x': unix_times, 'y': np.float64(data['gclat'])})
    store_data(prefix + 'gdlon' + suffix, data={'x': unix_times, 'y': np.float64(data['gclon'])})
    store_data(prefix + 'inv' +  suffix, data={'x': unix_times, 'y': np.float64(data['inv'])})
    store_data(prefix + 'fmlat' + suffix, data={'x': unix_times, 'y': np.float64(data['fmlat'])})
    store_data(prefix + 'MLT' + suffix, data={'x': unix_times, 'y': np.float64(data['mlt'])})
    store_data(prefix + 'gcalt' + suffix, data={'x': unix_times, 'y': rr / km_in_re})
    store_data(prefix + 'gclat' + suffix, data={'x': unix_times, 'y': th})
    store_data(prefix + 'gclon' + suffix, data={'x': unix_times, 'y': ph})
    options(prefix + 'geo' + suffix, 'ytitle', 'GEO')
    options(prefix + 'geo' + suffix, 'ysubtitle', '[Re]')
    options(prefix + 'gdlat' + suffix, 'ytitle', 'Geodetic latitude of the magnetic footprint')
    options(prefix + 'gdlat' + suffix, 'ysubtitle', '(120km altitude) [deg]')
    options(prefix + 'gdlon' + suffix, 'ytitle', 'Geodetic longitude of the magnetic footprint')
    options(prefix + 'gdlon' + suffix, 'ysubtitle', '(120km altitude) [deg]')
    options(prefix + 'inv' + suffix, 'ytitle', 'Invariant Latitude of the magnetic footprint')
    options(prefix + 'inv' + suffix, 'ysubtitle', '(120km altitude) [deg]')
    options(prefix + 'fmlat' + suffix , 'ytitle', 'Geomagnetic Latitude of the magnetic footprint')
    options(prefix + 'fmlat' + suffix, 'ysubtitle', '(120km altitude) [deg]')
    options(prefix + 'MLT' + suffix, 'ytitle', 'Magnetic Local Time')
    options(prefix + 'MLT' + suffix, 'ysubtitle', '[hours]')
    options(prefix + 'gcalt' + suffix, 'ytitle', 'Geocentric Altitude')
    options(prefix + 'gcalt' + suffix, 'ysubtitle', '[Re]')
    options(prefix + 'gclat' + suffix, 'ytitle', 'Geocentric Latitude')
    options(prefix + 'gclat' + suffix, 'ysubtitle', '[deg]')
    options(prefix + 'gclon' + suffix, 'ytitle', 'Geocentric Longitude')
    options(prefix + 'gclon' + suffix, 'ysubtitle', '[deg]')

    return [prefix + 'geo' + suffix,
            prefix + 'gdlat' + suffix,
            prefix + 'gdlon' + suffix,
            prefix + 'inv' + suffix,
            prefix + 'fmlat' + suffix,
            prefix + 'MLT' + suffix,
            prefix + 'gcalt' + suffix,
            prefix + 'gclat' + suffix,
            prefix + 'gclon' + suffix]

        
