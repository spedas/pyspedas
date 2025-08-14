
import logging
from pyspedas.tplot_tools import store_data, options, set_units, set_coords

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def spd_pgs_moments_tplot(moments, x=None, prefix='', suffix='', coords='DSL', use_mms_sdc_units=False):
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

        coords:str
            Coordinate system to set for non-field-aligned moments that have coordinates
            Default: 'DSL'

        use_mms_sdc_units: bool
            If True, convert pressure tensor and heat flux values and units to nPa and mW/m^2 respectively,
            for compatibility with MMS SDC products.
            Default: False

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
        'ttens': 'eV',
        't3': 'eV',
        'magt3': 'eV',
        'avgtemp': 'eV',
        'sc_pot': 'V',
        'eflux': 'eV/(cm^2-s)',
        'qflux': 'eV/(cm^2-s)',
        'mftens': 'eV/cm^3',
        'ptens': 'eV/cm^3',
        'symm': 'nT',
        'symm_theta': 'degrees',
        'symm_phi': 'degrees',
        'symm_ang': 'degrees',
        'magf': 'nT',
        }

    conversion_dict = {
        'density': 1.0,
        'velocity': 1.0,
        'vthermal': 1.0,
        'flux': 1.0,
        'ttens': 1.0,
        't3': 1.0,
        'magt3': 1.0,
        'avgtemp': 1.0,
        'sc_pot': 1.0,
        'eflux': 1.0,
        'qflux': 1.0,
        'mftens': 1.0,
        'ptens': 1.0,
        'symm': 1.0,
        'symm_theta': 1.0,
        'symm_phi': 1.0,
        'symm_ang': 1.0,
        'magf': 1.0,
        }

    if use_mms_sdc_units:
        # Convert pressure tensor and heat flux to MMS SDC-compatible units
        units_dict['ptens'] = 'nPa'
        conversion_dict['ptens'] = 0.000160217663
        units_dict['qflux'] = 'mW/m^2'
        conversion_dict['qflux'] = 1.6021765974585869e-12

    fa_coords = ['magf', 'magt3', 'symm']
    non_fa_coords = ['velocity','flux', 't3', 'eflux', 'qflux', 'mftens', 'ptens']


    for key in moments.keys():
        # Some moments (qflux, ptens) may have an optional conversion to different units
        conversion = conversion_dict.get(key)
        store_data(prefix + key + suffix, data={'x': x, 'y': conversion*moments[key]})
        units = units_dict.get(key)
        if units is not None:
            set_units(prefix + key + suffix, units)
            options(prefix+key+suffix, 'ysubtitle', '[' + units + ']')
        if key in fa_coords:
            set_coords(prefix + key + suffix, 'FA')
        elif key in non_fa_coords:
            set_coords(prefix + key + suffix, coords)

    options(prefix + 'velocity' + suffix, 'yrange', [-800, 800])
    # Flux is really spiky, so it's hard to set good default limits...
    options(prefix + 'flux' + suffix, 'yrange', [-1e10, 1e10])

    return [prefix + key + suffix for key in moments.keys()]
