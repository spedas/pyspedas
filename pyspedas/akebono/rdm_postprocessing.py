from .load import load
import numpy as np
import pandas as pd
from pytplot import store_data, options
from pytplot import time_double
from pyspedas.cotrans.xyz_to_polar import xyz_to_polar


def rdm_postprocessing(files):
    """
    Load the RDM ASCII files into tplot variables
    """
    data = load_csv_file(files)
    values = data.to_numpy()
    unix_times = time_double([ymd + '/' + hms for ymd, hms in zip(values[:, 0], values[:, 1])])

    L = np.float64(values[:, 2])
    INV = np.float64(values[:, 3])
    FMLAT = np.float64(values[:, 4])
    MLAT = np.float64(values[:, 5])
    MLT = np.float64(values[:, 6])
    ALT = np.float64(values[:, 7])
    GLAT = np.float64(values[:, 8])
    GLON = np.float64(values[:, 9])
    RDM_E3 = np.float64(values[:, 10])
    Energy = np.zeros(len(RDM_E3))
    Energy[:] = 2.5

    prefix_project = 'akb_'
    prefix_descriptor = 'rdm_'
    prefix = prefix_project + prefix_descriptor

    store_data(prefix_project+'L', data={'x': unix_times, 'y': L})
    store_data(prefix_project+'INV', data={'x': unix_times, 'y': INV})
    store_data(prefix_project+'FMLAT', data={'x': unix_times, 'y': FMLAT})
    store_data(prefix_project+'MLAT', data={'x': unix_times, 'y': MLAT})
    store_data(prefix_project+'MLT', data={'x': unix_times, 'y': MLT})
    store_data(prefix_project+'ALT', data={'x': unix_times, 'y': ALT})
    store_data(prefix_project+'GLAT', data={'x': unix_times, 'y': GLAT})
    store_data(prefix_project+'GLON', data={'x': unix_times, 'y': GLON})
    store_data(prefix+'FEIO', data={'x': unix_times, 'y': RDM_E3})
    store_data(prefix+'FEIO_Energy', data={'x': unix_times, 'y': Energy})

    options(prefix+'FEIO', 'spec', True)

    options(prefix_project+'L', 'ytitle', 'L-value')
    options(prefix_project+'INV', 'ytitle', 'Invariant Latitude [deg]')
    options(prefix_project+'FMLAT', 'ytitle', 'Footprint Latitude [deg]')
    options(prefix_project+'MLAT', 'ytitle', 'Magnetic Latitude [deg]')
    options(prefix_project+'MLT', 'ytitle', 'Magnetic Local Time [hour]')
    options(prefix_project+'ALT', 'ytitle', 'Altitude [km]')
    options(prefix_project+'GLAT', 'ytitle', 'Geographic Latitude [deg]')
    options(prefix_project+'GLON', 'ytitle', 'Geographic Longitude [deg]')
    options(prefix+'FEIO', 'ytitle', 'Omni-directional Integral Electron Flux')
    options(prefix+'FEIO', 'ysubtitle', '[/cm^22 sec str]')
    options(prefix+'FEIO_Energy', 'ytitle', 'Elctron energy [MeV]')

    return [prefix_project+'L',
            prefix_project+'INV',
            prefix_project+'FMLAT',
            prefix_project+'MLAT',
            prefix_project+'MLT',
            prefix_project+'ALT',
            prefix_project+'GLAT',
            prefix_project+'GLON',
            prefix+'FEIO',
            prefix+'FEIO_Energy']


