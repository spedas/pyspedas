import logging
import numpy as np
from pytplot import get_data, store_data, options, tnames

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def mms_eis_omni(probe, species='proton', datatype='extof', suffix='', data_units='flux', data_rate='srvy', level='l2'):
    """
    This function will calculate the omnidirectional EIS spectrograms, and is automatically called from mms_load_eis
    
    Parameters
    ----------
        probe: str
            probe #, e.g., '4' for MMS4

        species: str
            species for calculation (default: 'proton')

        datatype: str
            'extof' or 'phxtof' (default: 'extof')

        suffix: str
            suffix of the loaded data

        data_units: str
            'flux' or 'cps' (default: 'flux')

        data_rate: str
            instrument data rate, e.g., 'srvy' or 'brst' (default: 'srvy')

        level: str
            data level ['l1a','l1b','l2pre','l2' (default)]

    Returns
    ---------
        Name of tplot variable created.
    """
    
    probe = str(probe)
    species_str = datatype + '_' + species
    prefix = 'mms' + probe + '_epd_eis_' + data_rate + '_' + level + '_'

    if data_units == 'flux':
        units_label = '1/(cm^2-sr-s-keV)'
    elif data_units == 'cps':
        units_label = '1/s'
    elif data_units == 'counts':
        units_label = 'counts'

    telescopes = tnames(pattern=prefix + species_str + '_*' + data_units + '_t?'+suffix)

    if len(telescopes) == 6:
        scope_data = get_data(telescopes[0])
            
        if len(scope_data) <= 2:
            logging.error("Error, couldn't find energy table for the variable: " + telescopes[0])
            return None

        time, data, energies = scope_data

        flux_omni = np.zeros((len(time), len(energies)))
        for t in telescopes:
            time, data, energies = get_data(t)
            flux_omni = flux_omni + data

        store_data(prefix + species_str + '_' + data_units + '_omni' + suffix, data={'x': time, 'y': flux_omni/6., 'v': energies})
        options(prefix + species_str + '_' + data_units + '_omni' + suffix, 'spec', 1)
        options(prefix + species_str + '_' + data_units + '_omni' + suffix, 'ylog', 1)
        options(prefix + species_str + '_' + data_units + '_omni' + suffix, 'zlog', 1)
        options(prefix + species_str + '_' + data_units + '_omni' + suffix, 'ztitle', units_label)
        options(prefix + species_str + '_' + data_units + '_omni' + suffix, 'ytitle', 'MMS' + probe + ' ' + datatype + ' ' + species)
        options(prefix + species_str + '_' + data_units + '_omni' + suffix, 'ysubtitle', 'Energy [keV]')
        options(prefix + species_str + '_' + data_units + '_omni' + suffix, 'yrange', [14, 45])

        # create new variable with omni energy limits
        energy_minus = get_data(prefix + species_str + '_t0_energy_dminus' + suffix)
        energy_gm = get_data(prefix + species_str + '_t0_energy' + suffix)
        energy_plus = get_data(prefix + species_str + '_t0_energy_dplus' + suffix)

        if isinstance(energy_minus, np.ndarray) and isinstance(energy_plus, np.ndarray):
            # transpose is used here to make the variable match the variable in IDL
            store_data(prefix + species_str + '_energy_range' + suffix, data={'y': np.array([energy_gm-energy_minus,energy_gm+energy_plus]).transpose()})

        return prefix + species_str + '_' + data_units + '_omni' + suffix
    else:
        logging.error('Error, problem finding the telescopes to calculate omni-directional spectrograms')
        return None
