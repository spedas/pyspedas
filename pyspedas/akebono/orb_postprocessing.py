import numpy as np
from pytplot import store_data, options
from pytplot import time_double
from pyspedas.cotrans.xyz_to_polar import xyz_to_polar
from .load_csv_file import load_csv_file

def orb_postprocessing(files):
    """
    Load the orbit CSV files and create the tplot variables
    """
    prefix_project = 'akb_'
    prefix_descriptor = 'orb_'
    prefix = prefix_project + prefix_descriptor

    cols = ['pass','ut', 'ksc_azm', 'ksc_elv', 'ksc_dis', 'ksc_ang', 'syo_azm', 'syo_elv', 'syo_dis', 'syo_ang',
            'pra_azm', 'pra_elv', 'pra_dis', 'pra_ang', 'esr_azm', 'esr_elv', 'esr_dis', 'esr_ang', 'gclat','gclon',
            'inv', 'fmlat', 'mlat', 'mlt', 'bmdl_x', 'bmdl_y', 'bmdl_z', 'xxlon_sc', 'xxlat_sc', 'aheight','lsun',
            's_direc_x', 's_direc_y', 's_direc_z', 'sc_pos_x', 'sc_pos_y', 'sc_pos_z', 'sc_vel_x', 'sc_vel_y', 'sc_vel_z']

    data = load_csv_file(files, cols=cols)
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
    store_data(prefix + 'geo', data={'x': unix_times, 'y': xyz_re})
    store_data(prefix + 'gdlat', data={'x': unix_times, 'y': np.float64(data['gclat'])})
    store_data(prefix + 'gdlon', data={'x': unix_times, 'y': np.float64(data['gclon'])})
    store_data(prefix + 'inv', data={'x': unix_times, 'y': np.float64(data['inv'])})
    store_data(prefix + 'fmlat', data={'x': unix_times, 'y': np.float64(data['fmlat'])})
    store_data(prefix + 'MLT', data={'x': unix_times, 'y': np.float64(data['mlt'])})
    store_data(prefix + 'gcalt', data={'x': unix_times, 'y': rr / km_in_re})
    store_data(prefix + 'gclat', data={'x': unix_times, 'y': th})
    store_data(prefix + 'gclon', data={'x': unix_times, 'y': ph})
    options(prefix + 'geo', 'ytitle', 'GEO')
    options(prefix + 'geo', 'ysubtitle', '[Re]')
    options(prefix + 'gdlat', 'ytitle', 'Geodetic latitude of the magnetic footprint')
    options(prefix + 'gdlat', 'ysubtitle', '(120km altitude) [deg]')
    options(prefix + 'gdlon', 'ytitle', 'Geodetic longitude of the magnetic footprint')
    options(prefix + 'gdlon', 'ysubtitle', '(120km altitude) [deg]')
    options(prefix + 'inv', 'ytitle', 'Invariant Latitude of the magnetic footprint')
    options(prefix + 'inv', 'ysubtitle', '(120km altitude) [deg]')
    options(prefix + 'fmlat', 'ytitle', 'Geomagnetic Latitude of the magnetic footprint')
    options(prefix + 'fmlat', 'ysubtitle', '(120km altitude) [deg]')
    options(prefix + 'MLT', 'ytitle', 'Magnetic Local Time')
    options(prefix + 'MLT', 'ysubtitle', '[hours]')
    options(prefix + 'gcalt', 'ytitle', 'Geocentric Altitude')
    options(prefix + 'gcalt', 'ysubtitle', '[Re]')
    options(prefix + 'gclat', 'ytitle', 'Geocentric Latitude')
    options(prefix + 'gclat', 'ysubtitle', '[deg]')
    options(prefix + 'gclon', 'ytitle', 'Geocentric Longitude')
    options(prefix + 'gclon', 'ysubtitle', '[deg]')

    return [prefix + 'geo',
            prefix + 'gdlat',
            prefix + 'gdlon',
            prefix + 'inv',
            prefix + 'fmlat',
            prefix + 'MLT',
            prefix + 'gcalt',
            prefix + 'gclat',
            prefix + 'gclon']

        
