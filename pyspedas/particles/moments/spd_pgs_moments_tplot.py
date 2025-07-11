
import logging
from pytplot import store_data, options, set_units

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def spd_pgs_moments_tplot(moments, x=None, prefix='', suffix=''):
    """
    Creates tplot variables from moments dictionaries

    Parameters
    ----------
        moments: dict
            Dictionary containing moments values returned by moments_3d

        x: numpy.ndarray
            The x-axis (time) values

        prefix: str
            Name prefix for the output variables

        suffix: str
            Name suffix for the output variables

    Returns
    -------
    list of str
        List of tplot variables returned
    """

    if x is None:
        logging.error('Error, no x-values specified')
        return None

    if not isinstance(moments, dict):
        logging.error('Error, the "moments" variable must be a hash table containing the moments')
        return None

    units_dict = {
        'density': '1/cm^3',
        'velocity': 'km/s',
        'vthermal': 'km/s',
        'flux': '1/(cm^2-s)',
        't3': 'eV',
        'magt3': 'eV',
        'avgtemp': 'eV',
        'sc_pot': 'V',
        'eflux': 'eV/(cm^2-s)',
        'qflux': 'eV/(cm^2-s)',
        'mftens': 'eV/cm^3',
        'ptens': 'eV/cm^3',
        'symm_theta': 'degrees',
        'symm_phi': 'degrees',
        'symm_ang': 'degrees',
        'magf': 'nT',
        }

    for key in moments.keys():
        store_data(prefix + key + suffix, data={'x': x, 'y': moments[key]})
        units = units_dict.get(key)
        if units is not None:
            set_units(prefix + key + suffix, units)
            options(prefix+key+suffix, 'ysubtitle', '[' + units + ']')

    options(prefix + 'velocity' + suffix, 'yrange', [-800, 800])
    # Flux is really spiky, so it's hard to set good default limits...
    options(prefix + 'flux' + suffix, 'yrange', [-1e10, 1e10])

    return [prefix + key + suffix for key in moments.keys()]
