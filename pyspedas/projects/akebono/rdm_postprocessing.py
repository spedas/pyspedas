import numpy as np
from pytplot import store_data, options
from pytplot import time_double
from .load_csv_file import load_csv_file


# This routine was originally in akebono/__init__.py.  If you need to see the history of this routine before
# it was moved to its own file, please check the history for __init__.py.

def rdm_postprocessing(files, prefix='', suffix=''):
    """
    Load the RDM ASCII files into tplot variables

    Parameters
    ----------
    files: list of str
        List of filenames to convert to tplot variables
    prefix: str
        Prefix to be added to tplot variables created. Default: ''
    suffix: str
        Suffix to be added to tplot variables created. Default: ''

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

    try:
        data = load_csv_file(files)
    except UnicodeDecodeError:
        data = load_csv_file(files, gz=True)

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
    prefix = user_prefix + prefix_project + prefix_descriptor

    store_data(user_prefix + prefix_project+'L' + suffix, data={'x': unix_times, 'y': L})
    store_data(user_prefix + prefix_project+'INV' + suffix, data={'x': unix_times, 'y': INV})
    store_data(user_prefix + prefix_project+'FMLAT' + suffix, data={'x': unix_times, 'y': FMLAT})
    store_data(user_prefix + prefix_project+'MLAT' + suffix, data={'x': unix_times, 'y': MLAT})
    store_data(user_prefix + prefix_project+'MLT' + suffix, data={'x': unix_times, 'y': MLT})
    store_data(user_prefix + prefix_project+'ALT' + suffix, data={'x': unix_times, 'y': ALT})
    store_data(user_prefix + prefix_project+'GLAT' + suffix, data={'x': unix_times, 'y': GLAT})
    store_data(user_prefix + prefix_project+'GLON' + suffix, data={'x': unix_times, 'y': GLON})
    store_data(prefix+'FEIO' + suffix, data={'x': unix_times, 'y': RDM_E3})
    store_data(prefix+'FEIO_Energy' + suffix, data={'x': unix_times, 'y': Energy})

    # Not sure why this is here...FEIO is a scalar at each time step
    options(prefix+'FEIO' + suffix, 'spec', True)

    options(user_prefix + prefix_project+'L' + suffix, 'ytitle', 'L-value')
    options(user_prefix + prefix_project+'INV' + suffix, 'ytitle', 'Invariant Latitude [deg]')
    options(user_prefix + prefix_project+'FMLAT' + suffix, 'ytitle', 'Footprint Latitude [deg]')
    options(user_prefix + prefix_project+'MLAT' + suffix, 'ytitle', 'Magnetic Latitude [deg]')
    options(user_prefix + prefix_project+'MLT' + suffix, 'ytitle', 'Magnetic Local Time [hour]')
    options(user_prefix + prefix_project+'ALT' + suffix, 'ytitle', 'Altitude [km]')
    options(user_prefix + prefix_project+'GLAT' + suffix, 'ytitle', 'Geographic Latitude [deg]')
    options(user_prefix + prefix_project+'GLON' + suffix, 'ytitle', 'Geographic Longitude [deg]')
    options(prefix+'FEIO' + suffix, 'ytitle', 'Omni-directional Integral Electron Flux')
    options(prefix+'FEIO' + suffix, 'ysubtitle', '[/cm^22 sec str]')
    options(prefix+'FEIO_Energy' + suffix, 'ytitle', 'Elctron energy [MeV]')

    return [user_prefix + prefix_project+'L' + suffix,
            user_prefix + prefix_project+'INV' + suffix,
            user_prefix + prefix_project+'FMLAT' + suffix,
            user_prefix + prefix_project+'MLAT' + suffix,
            user_prefix + prefix_project+'MLT' + suffix,
            user_prefix + prefix_project+'ALT' + suffix,
            user_prefix + prefix_project+'GLAT' + suffix,
            user_prefix + prefix_project+'GLON' + suffix,
            prefix+'FEIO' + suffix,
            prefix+'FEIO_Energy' + suffix]


